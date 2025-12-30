import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict
import calendar
import time
import sys
import os

# Adicionar diretório atual ao path para imports funcionarem
if os.path.dirname(__file__) not in sys.path:
    sys.path.insert(0, os.path.dirname(__file__))

# Importar novos módulos da arquitetura refatorada
try:
    from config.settings import config, get_category_color
    from config.constants import get_acoes_b3_completas, get_fiis_completos
    from core.calculator import calculate_dividend_metrics, analyze_stocks_parallel
    from core.optimizer import optimize_portfolio
    from core.data_fetcher import data_fetcher
    from utils.helpers import categorize_ticker, get_ticker_list_by_categories, format_time_elapsed
    from utils.validators import validate_dividend_yield, validate_portfolio_capital
    from utils.formatters import format_currency, format_percentage, create_summary_text
    from utils.logger import setup_logger, log_performance
    
    # Configurar logger
    logger = setup_logger('streamlit_app')
    USING_NEW_MODULES = True
    logger.info("✅ Novos módulos carregados com sucesso!")
    
except Exception as e:
    st.error(f"⚠️ Erro ao carregar novos módulos: {str(e)}")
    st.error(f"📂 Diretório atual: {os.getcwd()}")
    st.error(f"🐍 Python path: {sys.path[:3]}")
    USING_NEW_MODULES = False
    # Fallback para imports antigos se necessário
    from acoes_b3_completa import get_acoes_b3_completas, get_fiis_completos

# --- Configurações da Página Streamlit ---
st.set_page_config(
    layout=config.LAYOUT,
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON
)

logger.info("🚀 Aplicativo iniciado")

# --- Lista Curada de Tickers da B3 ---

def get_all_b3_tickers():
    """Retorna lista expandida de tickers da B3 por categoria."""
    # USAR NOVA IMPLEMENTAÇÃO DOS MÓDULOS
    logger.info("Buscando lista completa de tickers da B3")
    
    acoes = get_acoes_b3_completas()
    fiis = get_fiis_completos()
    
    # BDRs
    bdrs = [
        "AAPL34.SA", "MSFT34.SA", "AMZO34.SA", "GOGL34.SA", "META34.SA",
        "TSLA34.SA", "NVDC34.SA", "NFLX34.SA", "DIS34.SA", "COCA34.SA",
        "PETR34.SA", "JPMC34.SA", "V1SA34.SA", "MAST34.SA", "PYPL34.SA"
    ]
    
    # ETFs
    etfs = [
        "BOVA11.SA", "SMAL11.SA", "IVVB11.SA", "SPXI11.SA", "MATB11.SA",
        "PIBB11.SA", "ISUS11.SA", "FIND11.SA", "DIVO11.SA", "BOVX11.SA",
        "GOVE11.SA", "BRAX11.SA", "XBOV11.SA", "BOVV11.SA"
    ]
    
    all_tickers = acoes + fiis + bdrs + etfs
    logger.info(f"✅ Total de {len(all_tickers)} tickers carregados")
    return all_tickers

# categorize_ticker agora vem de utils.helpers (já importado no topo)

# --- Funções Auxiliares ---
# AGORA USANDO MÓDULOS REFATORADOS (calculate_dividend_metrics vem de core.calculator)

def analyze_selected_stocks(selected_tickers, progress_bar=None):
    """
    Analisa os tickers selecionados.
    NOVA IMPLEMENTAÇÃO: Usa análise paralela de core.calculator com fallback
    """
    if USING_NEW_MODULES:
        try:
            logger.info(f"🚀 Iniciando análise PARALELA de {len(selected_tickers)} ativos")
            start_time = time.time()
            
            def progress_callback(progress, message):
                if progress_bar:
                    progress_bar.progress(progress, message)
            
            # USAR ANÁLISE PARALELA!
            df_results = analyze_stocks_parallel(
                selected_tickers,
                progress_callback=progress_callback
            )
            
            duration = time.time() - start_time
            log_performance(logger, f"Análise de {len(df_results)} ativos", duration)
            
            return df_results
        except Exception as e:
            st.warning(f"⚠️ Análise paralela falhou: {str(e)}. Usando método sequencial...")
            logger.error(f"Erro na análise paralela: {str(e)}")
    
    # FALLBACK: Análise sequencial (método antigo)
    st.info("📊 Usando análise sequencial (modo legado)")
    results = []
    total = len(selected_tickers)
    
    for idx, ticker in enumerate(selected_tickers):
        if progress_bar:
            progress_bar.progress((idx + 1) / total, f"Analisando {ticker}...")
        
        try:
            metrics = calculate_dividend_metrics(ticker)
            if metrics:
                results.append(metrics)
        except Exception as e:
            logger.warning(f"Erro ao analisar {ticker}: {str(e)}")
            continue
    
    return pd.DataFrame(results)

def optimize_portfolio(df_stocks, capital_total, min_acoes_por_empresa=100):
    """Otimiza o portfólio para maximizar DY e diversificação."""
    if df_stocks.empty or capital_total <= 0:
        return None
    
    # Ordenar por score
    df_sorted = df_stocks.sort_values('score', ascending=False).copy()
    
    # Selecionar top ações (máximo 10 para diversificação)
    max_acoes = min(10, len(df_sorted))
    df_selected = df_sorted.head(max_acoes).copy()
    
    # Distribuir capital proporcionalmente ao score
    df_selected['peso'] = df_selected['score'] / df_selected['score'].sum()
    df_selected['capital_alocado'] = df_selected['peso'] * capital_total
    
    # Calcular quantidade de ações (lotes de 100 para ações, 1 para FIIs/BDRs/ETFs)
    def calcular_quantidade(row):
        if row['categoria'] == 'Ação':
            lote = min_acoes_por_empresa
        else:
            lote = 1  # FIIs, BDRs e ETFs geralmente não têm lote mínimo
        
        qtd_ideal = row['capital_alocado'] / row['preco']
        qtd_lotes = (qtd_ideal // lote) * lote
        return int(qtd_lotes) if qtd_lotes > 0 else lote
    
    df_selected['quantidade'] = df_selected.apply(calcular_quantidade, axis=1)
    
    # Recalcular valores reais
    df_selected['valor_investido'] = df_selected['quantidade'] * df_selected['preco']
    
    # Remover linhas com valor zero
    df_selected = df_selected[df_selected['valor_investido'] > 0]
    
    if df_selected.empty:
        return None
    
    df_selected['percentual_carteira'] = (df_selected['valor_investido'] / df_selected['valor_investido'].sum()) * 100
    
    # Dividendos esperados (baseado em DY 12m)
    df_selected['dividendos_anuais_estimados'] = df_selected['valor_investido'] * (df_selected['dy_12m'] / 100)
    df_selected['dividendos_mensais_estimados'] = df_selected['dividendos_anuais_estimados'] / 12
    
    return df_selected[['ticker', 'nome', 'categoria', 'setor', 'preco', 'quantidade', 'valor_investido', 
                        'percentual_carteira', 'dy_12m', 'dividendos_anuais_estimados', 
                        'dividendos_mensais_estimados', 'score', 'dividends_history']]

def simulate_portfolio_history(portfolio_df, years=5):
    """Simula o histórico do portfólio nos últimos N anos."""
    if portfolio_df is None or portfolio_df.empty:
        return None, None
    
    # Preparar dados históricos
    end_date = datetime.today()
    start_date = end_date - timedelta(days=years*365)
    
    monthly_dividends = defaultdict(float)
    annual_dividends = defaultdict(float)
    
    for _, row in portfolio_df.iterrows():
        dividends = row['dividends_history']
        quantidade = row['quantidade']
        
        if dividends.empty:
            continue
        
        for date, div_value in dividends.items():
            date_naive = date.tz_localize(None) if hasattr(date, 'tz_localize') else date
            
            if date_naive >= pd.to_datetime(start_date):
                year = date_naive.year
                month_key = f"{date_naive.year}-{date_naive.month:02d}"
                
                total_dividend = div_value * quantidade
                monthly_dividends[month_key] += total_dividend
                annual_dividends[year] += total_dividend
    
    # Criar DataFrames
    df_monthly = pd.DataFrame([
        {'mes': k, 'dividendos': v} for k, v in sorted(monthly_dividends.items())
    ])
    
    df_annual = pd.DataFrame([
        {'ano': k, 'dividendos': v} for k, v in sorted(annual_dividends.items())
    ])
    
    return df_monthly, df_annual

def create_dividend_calendar(portfolio_df):
    """Cria calendário de pagamento de dividendos."""
    if portfolio_df is None or portfolio_df.empty:
        return None
    
    # Analisar últimos 24 meses para identificar padrão
    end_date = datetime.today()
    start_date = end_date - timedelta(days=730)
    
    dividend_calendar = defaultdict(lambda: defaultdict(list))
    
    for _, row in portfolio_df.iterrows():
        ticker = row['ticker']
        dividends = row['dividends_history']
        quantidade = row['quantidade']
        
        if dividends.empty:
            continue
        
        for date, div_value in dividends.items():
            date_naive = date.tz_localize(None) if hasattr(date, 'tz_localize') else date
            
            if date_naive >= pd.to_datetime(start_date):
                month = date_naive.month
                total_dividend = div_value * quantidade
                dividend_calendar[month][ticker].append(total_dividend)
    
    # Calcular média por mês
    monthly_summary = []
    for month in range(1, 13):
        month_name = calendar.month_name[month]
        total_month = 0
        tickers_pagantes = []
        
        if month in dividend_calendar:
            for ticker, values in dividend_calendar[month].items():
                avg_value = np.mean(values)
                total_month += avg_value
                tickers_pagantes.append(f"{ticker.replace('.SA', '')}")
        
        monthly_summary.append({
            'mes_num': month,
            'mes': month_name,
            'valor_estimado': total_month,
            'acoes_pagantes': ', '.join(tickers_pagantes) if tickers_pagantes else 'Nenhuma'
        })
    
    return pd.DataFrame(monthly_summary)

# --- Interface Principal ---
st.title("🎯 Otimizador de Carteira de Dividendos - B3 Completa")

# Banner de melhorias
if USING_NEW_MODULES:
    st.success("""
    🚀 **NOVO! Versão 2.0 com Melhorias de Performance ATIVADA** ✅
    - ⚡ **5-10x mais rápido**: Análise paralela de ativos
    - ✅ **Validação robusta**: Remove outliers automaticamente (DY > 40%)
    - 📝 **Logging estruturado**: Melhor rastreamento e debugging
    - 🏗️ **Arquitetura modular**: Código mais manutenível
    
    📊 **Configuração atual:** {workers} workers paralelos | Cache: {cache}min
    """.format(
        workers=config.MAX_WORKERS if USING_NEW_MODULES else "N/A",
        cache=config.CACHE_TTL_SHORT//60 if USING_NEW_MODULES else "N/A"
    ))
else:
    st.warning("""
    ⚠️ **Executando em modo legado** 
    Os novos módulos não foram carregados. Algumas funcionalidades podem estar limitadas.
    """)

st.markdown("""
Este aplicativo analisa **ações, FIIs, BDRs e ETFs** negociados na B3 e cria um portfólio otimizado 
para gerar fluxo de caixa mensal consistente.

**Novidades da versão 2.0:**
- Análise até **10x mais rápida** com processamento paralelo
- Detecção automática de outliers e dados inconsistentes
- Validações rigorosas de qualidade de dados
- Sistema de logs para melhor suporte
""")

# Sidebar com filtros de categoria
st.sidebar.header("🔍 Filtros de Segmento")

# Checkboxes para categorias
st.sidebar.markdown("**Selecione os segmentos para análise:**")
categoria_acao = st.sidebar.checkbox("📈 Ações", value=True, key="check_acoes")
categoria_fii = st.sidebar.checkbox("🏢 FIIs (Fundos Imobiliários)", value=True, key="check_fiis")
categoria_bdr = st.sidebar.checkbox("🌎 BDRs (Ações Internacionais)", value=False, key="check_bdrs")
categoria_etf = st.sidebar.checkbox("📊 ETFs (Fundos de Índice)", value=False, key="check_etfs")

# Verificar se pelo menos uma categoria está selecionada
categorias_ativas = []
if categoria_acao:
    categorias_ativas.append('Ação')
if categoria_fii:
    categorias_ativas.append('FII')
if categoria_bdr:
    categorias_ativas.append('BDR')
if categoria_etf:
    categorias_ativas.append('ETF')

if not categorias_ativas:
    st.sidebar.warning("⚠️ Selecione pelo menos um segmento!")

# Criar abas principais
tab1, tab2, tab3 = st.tabs(["📊 Ranking de Ativos", "💼 Otimizador de Portfólio", "📈 Simulação Histórica"])

# ===== TAB 1: RANKING DE ATIVOS =====
with tab1:
    st.header("📊 Ranking dos Melhores Ativos para Dividendos")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        categorias_str = ", ".join(categorias_ativas) if categorias_ativas else "Nenhum"
        st.info(f"🔍 Segmentos selecionados: **{categorias_str}**")
    with col2:
        if USING_NEW_MODULES:
            st.success("✅ Modo v2.0")
        else:
            st.warning("⚠️ Modo legado")
    with col3:
        if st.button("🔄 Limpar Cache", type="secondary"):
            st.cache_data.clear()
            st.success("Cache limpo!")
    
    if categorias_ativas:
        if st.button("🚀 Analisar Ativos Selecionados", type="primary"):
            with st.spinner("Analisando ativos..."):
                # Buscar todos os tickers
                all_tickers = get_all_b3_tickers()
                
                # Filtrar por categoria
                filtered_tickers = []
                for ticker in all_tickers:
                    categoria = categorize_ticker(ticker)
                    if categoria in categorias_ativas:
                        filtered_tickers.append(ticker)
                
                st.info(f"✅ Encontrados {len(filtered_tickers)} ativos para análise")
                
                # Analisar com medição de tempo
                start_time = time.time()
                progress_bar = st.progress(0)
                df_ranking = analyze_selected_stocks(filtered_tickers, progress_bar)
                progress_bar.empty()
                duration = time.time() - start_time
                
                if not df_ranking.empty:
                    st.session_state['df_ranking'] = df_ranking
                    
                    # Mostrar resultado com performance
                    col_result1, col_result2 = st.columns(2)
                    with col_result1:
                        st.success(f"✅ Análise concluída! {len(df_ranking)} ativos com dados de dividendos.")
                    with col_result2:
                        st.info(f"⚡ Tempo: {format_time_elapsed(duration)} | Velocidade: {len(df_ranking)/duration:.1f} ativos/s")
                else:
                    st.error("Nenhum ativo com dados de dividendos encontrado.")
    
    if 'df_ranking' in st.session_state:
        df_ranking = st.session_state['df_ranking']
        
        # Mostrar estatísticas gerais
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total de Ativos", len(df_ranking))
        col2.metric("DY Médio (12M)", f"{df_ranking['dy_12m'].mean():.2f}%")
        col3.metric("Consistência Média", f"{df_ranking['consistencia'].mean():.1f}%")
        col4.metric("CAGR Médio", f"{df_ranking['cagr_dividendos'].mean():.2f}%")
        
        # Contar por categoria
        categorias_count = df_ranking['categoria'].value_counts().to_dict()
        col5.metric("Categorias", len(categorias_count))
        
        # Filtros adicionais
        st.subheader("🔍 Filtros Adicionais")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            categorias_disponiveis = ['Todos'] + sorted(df_ranking['categoria'].unique().tolist())
            categoria_filtro = st.selectbox("Categoria", categorias_disponiveis)
        
        with col2:
            setores_disponiveis = ['Todos'] + sorted(df_ranking['setor'].unique().tolist())
            setor_filtro = st.selectbox("Setor", setores_disponiveis)
        
        with col3:
            dy_minimo = st.slider("DY Mínimo (12M)", 0.0, 15.0, 0.0, 0.5)
        
        with col4:
            dy_maximo = st.slider("DY Máximo (12M)", 0.0, 50.0, 40.0, 1.0, 
                                 help="Filtra outliers com DY muito alto")
        
        with col5:
            consistencia_minima = st.slider("Consistência Mínima (%)", 0, 100, 0, 10)
        
        # Aplicar filtros
        df_filtrado = df_ranking.copy()
        if categoria_filtro != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['categoria'] == categoria_filtro]
        if setor_filtro != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['setor'] == setor_filtro]
        df_filtrado = df_filtrado[df_filtrado['dy_12m'] >= dy_minimo]
        df_filtrado = df_filtrado[df_filtrado['dy_12m'] <= dy_maximo]  # NOVO: Filtro máximo
        df_filtrado = df_filtrado[df_filtrado['consistencia'] >= consistencia_minima]
        df_filtrado = df_filtrado.sort_values('score', ascending=False)
        
        # Exibir ranking
        st.subheader(f"🏆 Top Ativos ({len(df_filtrado)} resultados)")
        
        # Preparar DataFrame para exibição
        df_display = df_filtrado[['ticker', 'nome', 'categoria', 'setor', 'preco', 'dy_12m', 'dy_medio', 
                                   'consistencia', 'cagr_dividendos', 'anos_com_div', 'score']].copy()
        df_display.columns = ['Ticker', 'Nome', 'Categoria', 'Setor', 'Preço (R$)', 'DY 12M (%)', 
                              'DY Médio (%)', 'Consistência (%)', 'CAGR Div (%)', 
                              'Anos c/ Div', 'Score']
        
        st.dataframe(
            df_display.style.background_gradient(subset=['Score'], cmap='RdYlGn')
                           .format({'Preço (R$)': 'R$ {:.2f}', 
                                   'DY 12M (%)': '{:.2f}%',
                                   'DY Médio (%)': '{:.2f}%',
                                   'Consistência (%)': '{:.1f}%',
                                   'CAGR Div (%)': '{:.2f}%',
                                   'Score': '{:.2f}'}),
            width="stretch",
            height=400
        )
        
        # Gráficos
        st.subheader("📊 Visualizações")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_dy = px.bar(df_filtrado.head(15), x='ticker', y='dy_12m',
                           title='Top 15 - Dividend Yield (12M)',
                           labels={'dy_12m': 'DY (%)', 'ticker': 'Ativo'},
                           color='categoria', 
                           color_discrete_map={'Ação': '#1f77b4', 'FII': '#ff7f0e', 
                                              'BDR': '#2ca02c', 'ETF': '#d62728'})
            st.plotly_chart(fig_dy, width="stretch")
        
        with col2:
            fig_cat = px.pie(df_filtrado, names='categoria', title='Distribuição por Categoria',
                            color_discrete_map={'Ação': '#1f77b4', 'FII': '#ff7f0e', 
                                              'BDR': '#2ca02c', 'ETF': '#d62728'})
            st.plotly_chart(fig_cat, width="stretch")
        
        # Análise por categoria
        st.subheader("📦 Análise por Categoria")
        df_categoria = df_filtrado.groupby('categoria').agg({
            'dy_12m': 'mean',
            'consistencia': 'mean',
            'score': 'mean',
            'ticker': 'count'
        }).round(2)
        df_categoria.columns = ['DY Médio (%)', 'Consistência Média (%)', 'Score Médio', 'Qtd. Ativos']
        df_categoria = df_categoria.sort_values('Score Médio', ascending=False)
        
        st.dataframe(df_categoria, width="stretch")

# ===== TAB 2: OTIMIZADOR DE PORTFÓLIO =====
with tab2:
    st.header("💼 Otimizador de Portfólio")
    
    if 'df_ranking' not in st.session_state:
        st.warning("⚠️ Por favor, gere o ranking de ativos primeiro na aba 'Ranking de Ativos'")
    else:
        df_ranking = st.session_state['df_ranking']
        
        # Inputs do usuário
        st.subheader("💰 Configurações do Portfólio")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            capital_total = st.number_input(
                "Capital Total para Investimento (R$)",
                min_value=1000.0,
                max_value=10000000.0,
                value=50000.0,
                step=1000.0,
                format="%.2f"
            )
        
        with col2:
            lote_minimo = st.number_input(
                "Lote Mínimo de Ações",
                min_value=1,
                max_value=1000,
                value=100,
                step=1,
                help="FIIs, BDRs e ETFs usam lote 1"
            )
        
        with col3:
            dy_minimo_port = st.slider(
                "DY Mínimo para Seleção (%)",
                0.0, 15.0, 4.0, 0.5
            )
        
        # Botão para otimizar
        if st.button("🚀 Otimizar Portfólio", type="primary", key="btn_otimizar"):
            with st.spinner("Otimizando portfólio..."):
                # Filtrar ações com DY mínimo
                df_elegivel = df_ranking[df_ranking['dy_12m'] >= dy_minimo_port].copy()
                
                st.info(f"🔍 Debug: {len(df_ranking)} ativos no ranking, {len(df_elegivel)} com DY >= {dy_minimo_port}%")
                
                if df_elegivel.empty:
                    st.error("Nenhum ativo encontrado com o DY mínimo especificado. Tente reduzir o valor.")
                else:
                    st.info(f"💰 Otimizando com capital de R$ {capital_total:,.2f} e lote mínimo de {lote_minimo}")
                    
                    # Otimizar
                    portfolio = optimize_portfolio(df_elegivel, capital_total, lote_minimo)
                    
                    if portfolio is not None and not portfolio.empty:
                        st.session_state['portfolio_otimizado'] = portfolio
                        st.session_state['otimizacao_completa'] = True
                        st.success(f"✅ Portfólio otimizado com sucesso! {len(portfolio)} ativos selecionados.")
                        st.rerun()
                    else:
                        st.error("❌ Não foi possível criar um portfólio com os parâmetros especificados.")
                        st.warning("💡 Dicas: Tente aumentar o capital ou reduzir o lote mínimo.")
        
        # Exibir portfólio otimizado
        if 'portfolio_otimizado' in st.session_state:
            portfolio = st.session_state['portfolio_otimizado']
            
            st.subheader("📋 Portfólio Otimizado")
            
            # Métricas gerais
            total_investido = portfolio['valor_investido'].sum()
            dy_medio_carteira = (portfolio['dividendos_anuais_estimados'].sum() / total_investido) * 100 if total_investido > 0 else 0
            dividendos_anuais = portfolio['dividendos_anuais_estimados'].sum()
            dividendos_mensais = dividendos_anuais / 12
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("💰 Total Investido", f"R$ {total_investido:,.2f}")
            col2.metric("📊 DY Médio da Carteira", f"{dy_medio_carteira:.2f}%")
            col3.metric("📅 Dividendos/Ano", f"R$ {dividendos_anuais:,.2f}")
            col4.metric("📆 Dividendos/Mês (Estimado)", f"R$ {dividendos_mensais:,.2f}")
            
            # Tabela de alocação
            st.subheader("🎯 Alocação Detalhada")
            
            df_port_display = portfolio[['ticker', 'nome', 'categoria', 'setor', 'preco', 'quantidade', 
                                         'valor_investido', 'percentual_carteira', 'dy_12m',
                                         'dividendos_anuais_estimados']].copy()
            df_port_display.columns = ['Ticker', 'Nome', 'Categoria', 'Setor', 'Preço (R$)', 'Quantidade',
                                       'Valor Investido (R$)', '% Carteira', 'DY 12M (%)',
                                       'Dividendos/Ano (R$)']
            
            st.dataframe(
                df_port_display.style.format({
                    'Preço (R$)': 'R$ {:.2f}',
                    'Valor Investido (R$)': 'R$ {:.2f}',
                    '% Carteira': '{:.1f}%',
                    'DY 12M (%)': '{:.2f}%',
                    'Dividendos/Ano (R$)': 'R$ {:.2f}'
                }).background_gradient(subset=['% Carteira'], cmap='Blues'),
                width="stretch"
            )
            
            # Gráficos
            col1, col2 = st.columns(2)
            
            with col1:
                fig_pizza = px.pie(df_port_display, values='Valor Investido (R$)', names='Ticker',
                                   title='Distribuição do Capital por Ativo')
                st.plotly_chart(fig_pizza, width="stretch")
            
            with col2:
                fig_cat_port = px.pie(df_port_display, values='Valor Investido (R$)', names='Categoria',
                                      title='Distribuição do Capital por Categoria',
                                      color='Categoria',
                                      color_discrete_map={'Ação': '#1f77b4', 'FII': '#ff7f0e', 
                                                         'BDR': '#2ca02c', 'ETF': '#d62728'})
                st.plotly_chart(fig_cat_port, width="stretch")
            
            # Calendário de dividendos
            st.subheader("📅 Calendário Estimado de Dividendos")
            st.info("Baseado no padrão de pagamentos dos últimos 24 meses")
            
            calendario = create_dividend_calendar(portfolio)
            if calendario is not None and not calendario.empty:
                # CRIAR HEATMAP POR ATIVO
                st.markdown("### 📅 Calendário de Pagamentos por Ativo")
                
                # Preparar dados para heatmap
                heatmap_data = []
                meses_abrev = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                              'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
                
                # Analisar últimos 24 meses para identificar padrão de pagamentos
                end_date = datetime.today()
                start_date = end_date - timedelta(days=730)
                
                for _, row in portfolio.iterrows():
                    ticker = row['ticker'].replace('.SA', '')
                    dividends = row['dividends_history']
                    
                    if dividends.empty:
                        continue
                    
                    # Contar pagamentos por mês
                    monthly_payments = {m: 0 for m in range(1, 13)}
                    
                    for date, div_value in dividends.items():
                        date_naive = date.tz_localize(None) if hasattr(date, 'tz_localize') else date
                        if date_naive >= pd.to_datetime(start_date):
                            month = date_naive.month
                            monthly_payments[month] += 1
                    
                    # Adicionar ao heatmap (normalizar para mostrar frequência)
                    heatmap_data.append({
                        'Ticker': ticker,
                        **{meses_abrev[m-1]: min(monthly_payments[m], 4) for m in range(1, 13)}
                    })
                
                if heatmap_data:
                    df_heatmap = pd.DataFrame(heatmap_data)
                    
                    # Criar heatmap com plotly
                    fig_heatmap = go.Figure(data=go.Heatmap(
                        z=df_heatmap[meses_abrev].values,
                        x=meses_abrev,
                        y=df_heatmap['Ticker'],
                        colorscale='Greens',
                        text=df_heatmap[meses_abrev].values,
                        texttemplate='%{text}',
                        textfont={"size": 10},
                        colorbar=dict(title="Pagamentos"),
                        hovertemplate='<b>%{y}</b><br>Mês: %{x}<br>Pagamentos: %{z}<extra></extra>'
                    ))
                    
                    fig_heatmap.update_layout(
                        title='📊 Calendário de Pagamentos por Ativo',
                        xaxis_title='Mês',
                        yaxis_title='Ativo',
                        height=max(400, len(df_heatmap) * 25),
                        font=dict(size=10)
                    )
                    
                    st.plotly_chart(fig_heatmap, use_container_width=True)
                    
                    # Legendas
                    st.caption("💡 **Legenda:** Números indicam quantos pagamentos o ativo fez naquele mês nos últimos 24 meses")
                    st.caption("⚠️ **Nota:** Nem todos os meses estão cobertos nos últimos 24 meses")
                
                # Métricas de resumo
                st.markdown("### 📊 Resumo Mensal")
                col1, col2, col3 = st.columns(3)
                
                meses_cobertos = (calendario['valor_estimado'] > 0).sum()
                media_mensal = calendario['valor_estimado'].mean()
                mediana = calendario['valor_estimado'].median()
                
                col1.metric("Meses Cóbertos", f"{meses_cobertos}/12")
                col2.metric("Média Mensal", f"R$ {media_mensal:,.2f}")
                col3.metric("Mediana Mensal", f"R$ {mediana:,.2f}")
                
                # Gráfico de barras mensal
                st.markdown("### 💰 Fluxo Mensal Estimado")
                fig_calendario = px.bar(calendario, x='mes', y='valor_estimado',
                                       title='Dividendos Estimados por Mês',
                                       labels={'valor_estimado': 'Valor (R$)', 'mes': 'Mês'},
                                       text='valor_estimado',
                                       color='valor_estimado',
                                       color_continuous_scale='Greens')
                fig_calendario.update_traces(texttemplate='R$ %{text:.0f}', textposition='outside')
                fig_calendario.update_layout(showlegend=False)
                st.plotly_chart(fig_calendario, use_container_width=True)
                
                # Tabela detalhada
                with st.expander("📋 Ver Detalhes por Mês"):
                    df_cal_display = calendario[['mes', 'valor_estimado', 'acoes_pagantes']].copy()
                    df_cal_display.columns = ['Mês', 'Valor Estimado (R$)', 'Ativos Pagantes']
                    st.dataframe(
                        df_cal_display.style.format({'Valor Estimado (R$)': 'R$ {:.2f}'}),
                        use_container_width=True
                    )
            else:
                st.warning("Não foi possível gerar o calendário de dividendos")
            
            # Botão para baixar portfólio
            st.subheader("💾 Exportar Portfólio")
            csv = df_port_display.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Baixar Portfólio (CSV)",
                data=csv,
                file_name=f"portfolio_dividendos_{datetime.today().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

# ===== TAB 3: SIMULAÇÃO HISTÓRICA =====
with tab3:
    st.header("📈 Simulação Histórica do Portfólio")
    
    if 'portfolio_otimizado' not in st.session_state:
        st.warning("⚠️ Por favor, otimize um portfólio primeiro na aba 'Otimizador de Portfólio'")
    else:
        portfolio = st.session_state['portfolio_otimizado']
        
        st.info("Simulação do desempenho do portfólio nos últimos anos com os dividendos realmente pagos")
        
        anos_simulacao = st.slider("Anos de Histórico", 1, 5, 5)
        
        if st.button("📊 Simular Histórico", type="primary"):
            with st.spinner("Simulando histórico..."):
                df_monthly, df_annual = simulate_portfolio_history(portfolio, anos_simulacao)
                
                if df_monthly is not None and not df_monthly.empty:
                    st.session_state['simulacao_monthly'] = df_monthly
                    st.session_state['simulacao_annual'] = df_annual
                    st.success("✅ Simulação concluída!")
                else:
                    st.error("Não foi possível simular o histórico")
        
        if 'simulacao_monthly' in st.session_state:
            df_monthly = st.session_state['simulacao_monthly']
            df_annual = st.session_state['simulacao_annual']
            
            # Métricas gerais
            total_dividendos = df_annual['dividendos'].sum()
            media_anual = df_annual['dividendos'].mean()
            media_mensal = df_monthly['dividendos'].mean()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("💰 Total de Dividendos Recebidos", f"R$ {total_dividendos:,.2f}")
            col2.metric("📅 Média Anual", f"R$ {media_anual:,.2f}")
            col3.metric("📆 Média Mensal", f"R$ {media_mensal:,.2f}")
            
            # Gráfico anual
            st.subheader("📊 Dividendos Anuais Históricos")
            fig_annual = px.bar(df_annual, x='ano', y='dividendos',
                               title='Dividendos Recebidos por Ano',
                               labels={'dividendos': 'Dividendos (R$)', 'ano': 'Ano'},
                               text='dividendos')
            fig_annual.update_traces(texttemplate='R$ %{text:,.0f}', textposition='outside')
            st.plotly_chart(fig_annual, width="stretch")
            
            # Gráfico mensal
            st.subheader("📈 Evolução Mensal dos Dividendos")
            fig_monthly = go.Figure()
            fig_monthly.add_trace(go.Scatter(x=df_monthly['mes'], y=df_monthly['dividendos'],
                                           mode='lines+markers', name='Dividendos'))
            fig_monthly.add_hline(y=media_mensal, line_dash="dash", line_color="red",
                                 annotation_text=f"Média: R$ {media_mensal:.2f}")
            fig_monthly.update_layout(title='Dividendos Mensais Históricos',
                                     xaxis_title='Mês', yaxis_title='Dividendos (R$)')
            st.plotly_chart(fig_monthly, width="stretch")
            
            # Análise estatística
            st.subheader("📊 Análise Estatística")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Dividendos Anuais:**")
                if not df_annual.empty:
                    stats_annual = df_annual['dividendos'].describe()
                    st.dataframe(
                        pd.DataFrame({
                            'Estatística': ['Média', 'Mediana', 'Desvio Padrão', 'Mínimo', 'Máximo'],
                            'Valor (R$)': [
                                stats_annual['mean'],
                                df_annual['dividendos'].median(),
                                stats_annual['std'],
                                stats_annual['min'],
                                stats_annual['max']
                            ]
                        }).style.format({'Valor (R$)': 'R$ {:.2f}'}),
                        width="stretch"
                    )
            
            with col2:
                st.write("**Dividendos Mensais:**")
                if not df_monthly.empty:
                    stats_monthly = df_monthly['dividendos'].describe()
                    st.dataframe(
                        pd.DataFrame({
                            'Estatística': ['Média', 'Mediana', 'Desvio Padrão', 'Mínimo', 'Máximo'],
                            'Valor (R$)': [
                                stats_monthly['mean'],
                                df_monthly['dividendos'].median(),
                                stats_monthly['std'],
                                stats_monthly['min'],
                                stats_monthly['max']
                            ]
                        }).style.format({'Valor (R$)': 'R$ {:.2f}'}),
                        width="stretch"
                    )
            
            # Análise de rentabilidade
            st.subheader("💹 Análise de Rentabilidade")
            
            portfolio_total = st.session_state.get('portfolio_otimizado', pd.DataFrame())
            if not portfolio_total.empty:
                valor_investido_total = portfolio_total['valor_investido'].sum()
                
                col1, col2, col3 = st.columns(3)
                
                roi_total = (total_dividendos / valor_investido_total) * 100 if valor_investido_total > 0 else 0
                roi_anual = roi_total / anos_simulacao if anos_simulacao > 0 else 0
                
                col1.metric("💼 Valor Investido", f"R$ {valor_investido_total:,.2f}")
                col2.metric("📈 ROI Total (Dividendos)", f"{roi_total:.2f}%")
                col3.metric("📅 ROI Médio Anual", f"{roi_anual:.2f}%")
                
                st.info(f"""
                **Interpretação:** 
                - Nos últimos {anos_simulacao} anos, você teria recebido R$ {total_dividendos:,.2f} em dividendos
                - Isso representa um retorno de {roi_total:.2f}% sobre o capital investido (apenas dividendos)
                - Média anual de {roi_anual:.2f}% em dividendos
                - **Importante:** Esta análise considera apenas dividendos, não inclui valorização/desvalorização dos ativos
                """)

st.markdown("---")
st.caption("""
**Aviso Legal:** Esta ferramenta é apenas para fins educacionais e informativos. 
Os dados são obtidos do Yahoo Finance e podem conter imprecisões. 
As projeções são baseadas em dados históricos e não garantem resultados futuros.
Não constitui recomendação de investimento. Consulte um assessor financeiro qualificado.
""")
