import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict
import calendar

# --- Configurações da Página Streamlit ---
st.set_page_config(layout="wide", page_title="🎯 Otimizador de Carteira de Dividendos")

# --- Lista Curada de Tickers da B3 ---

def get_all_b3_tickers():
    """Retorna lista curada de tickers da B3 por categoria."""
    
    # AÇÕES - tickers reais mais negociados
    acoes = [
        # Bancos
        "ITUB4.SA", "BBDC4.SA", "BBAS3.SA", "SANB11.SA", "BPAC11.SA",
        # Petróleo/Energia
        "PETR3.SA", "PETR4.SA", "PRIO3.SA", "RECV3.SA", "RRRP3.SA",
        # Mineração
        "VALE3.SA", "BRAP4.SA", "GOAU4.SA", "CMIN3.SA", "GGBR4.SA", "USIM5.SA", "CSNA3.SA",
        # Elétricas
        "TAEE11.SA", "EGIE3.SA", "CPLE6.SA", "CMIG4.SA", "ENBR3.SA", "NEOE3.SA", "ENEV3.SA",
        # Saneamento
        "SAPR11.SA", "SBSP3.SA", "CSMG3.SA",
        # Telecom
        "TIMS3.SA", "VIVT3.SA",
        # Seguradoras
        "BBSE3.SA", "PSSA3.SA",
        # Varejo
        "LREN3.SA", "MGLU3.SA", "VVAR3.SA", "PETZ3.SA", "SOMA3.SA", "GUAR3.SA", "VIIA3.SA",
        # Consumo
        "ABEV3.SA", "BRFS3.SA", "MRFG3.SA", "JBSS3.SA", "BEEF3.SA", "SMTO3.SA",
        # Industrial
        "WEGE3.SA", "KLBN11.SA", "SUZB3.SA", "RAIL3.SA",
        # Construção
        "CYRE3.SA", "MRVE3.SA", "EZTC3.SA", "TEND3.SA", "JHSF3.SA",
        # Saúde
        "RDOR3.SA", "FLRY3.SA", "HAPV3.SA", "QUAL3.SA",
        # Educação
        "COGN3.SA", "YDUQ3.SA", "ANIM3.SA",
        # Logística
        "CCRO3.SA", "ECOR3.SA", "RADL3.SA",
        # Holdings
        "ITSA4.SA", "TRPL4.SA", "MULT3.SA",
        # Outras
        "B3SA3.SA", "CIEL3.SA", "LWSA3.SA", "POSI3.SA", "AZUL4.SA", "EMBR3.SA",
        "UGPA3.SA", "TOTS3.SA", "RENT3.SA", "ALSO3.SA", "ALPA4.SA", "CSAN3.SA",
        "EQTL3.SA", "CVCB3.SA", "POMO4.SA", "IRBR3.SA",
    ]
    
    # FIIs - principais fundos imobiliários  
    fiis = [
        # Lajes Corporativas
        "HGLG11.SA", "BTLG11.SA", "XPLG11.SA", "KNCR11.SA", "GGRC11.SA",
        # Shoppings
        "MALL11.SA", "XPML11.SA", "VISC11.SA", "HSML11.SA", "HSLG11.SA",
        # Logística
        "HGRU11.SA", "HGRE11.SA", "VILG11.SA", "TRXF11.SA", "TGAR11.SA",
        # Híbridos
        "MXRF11.SA", "KNRI11.SA", "HGPO11.SA", "KNHY11.SA", "KNIP11.SA",
        # Recebíveis
        "RZTR11.SA", "BCFF11.SA", "RBRR11.SA", "RBRF11.SA", "KFOF11.SA",
        # Títulos
        "PVBI11.SA", "IRDM11.SA", "BCRI11.SA", "CVBI11.SA", "RECT11.SA",
        # Residencial
        "HABT11.SA", "VINO11.SA", "RBVA11.SA", "VCJR11.SA", "RBRY11.SA",
        # Outros
        "JSRE11.SA", "ALZR11.SA", "MCHY11.SA", "DEVA11.SA", "CPTS11.SA",
        "HTMX11.SA", "BRCR11.SA", "XPCI11.SA", "GAME11.SA", "BTAL11.SA",
        "GALG11.SA", "GARE11.SA", "TRBL11.SA", "PATL11.SA", "PORD11.SA",
        "PLRI11.SA", "BPFF11.SA", "SARE11.SA", "VRTA11.SA",
    ]
    
    # BDRs - ações internacionais
    bdrs = [
        # Tech Giants
        "AAPL34.SA", "MSFT34.SA", "AMZO34.SA", "GOGL34.SA", "META34.SA",
        "NVDC34.SA", "TSLA34.SA",
        # Streaming/Media
        "NFLX34.SA", "DISB34.SA", "SPOT34.SA",
        # Finance/Payments
        "V1SA34.SA", "PYPL34.SA", "M1STR34.SA",
        # E-commerce/Apps
        "UBER34.SA", "AIRB34.SA",
        # Consumer Brands
        "NIKE34.SA", "COCA34.SA", "PEPB34.SA", "S1BX34.SA",
        # Industrial
        "BOEI34.SA", "C1AT34.SA",
        # Healthcare/Pharma
        "PFIZ34.SA", "JNJ34.SA", "ABBV34.SA",
        # Retail
        "W1MT34.SA", "HOME34.SA", "COST34.SA",
        # Asian Tech
        "BABA34.SA", "BIDU34.SA", "TCEHY34.SA",
        # European
        "ASML34.SA", "NESN34.SA", "LVMH34.SA", "SAP34.SA",
        # Others
        "INTC34.SA", "CSCO34.SA", "ADBE34.SA", "UPS34.SA",
    ]
    
    # ETFs - fundos de índice
    etfs = [
        "BOVA11.SA",  # Ibovespa
        "SMAL11.SA",  # Small Caps
        "IVVB11.SA",  # S&P 500
        "SPXI11.SA",  # S&P 500
        "DIVO11.SA",  # Dividendos
        "MATB11.SA",  # Materiais Básicos
        "PIBB11.SA",  # IBrX-50
        "ISUS11.SA",  # Sustentabilidade
        "FIND11.SA",  # Financeiro
        "BOVX11.SA",  # Ibovespa
        "GOVE11.SA",  # Governança
        "BRAX11.SA",  # Brasil
        "XBOV11.SA",  # Ibovespa
        "BOVV11.SA",  # Ibovespa Value
    ]
    
    return acoes + fiis + bdrs + etfs

def categorize_ticker(ticker):
    """Categoriza o ticker em: Ação, FII, BDR ou ETF."""
    ticker_clean = ticker.replace(".SA", "").upper()
    
    # ETFs específicos
    etfs_list = ["BOVA11", "SMAL11", "IVVB11", "SPXI11", "MATB11", "PIBB11", 
                 "ISUS11", "FIND11", "DIVO11", "BOVX11", "GOVE11", "BRAX11", 
                 "XBOV11", "BOVV11"]
    if ticker_clean in etfs_list:
        return "ETF"
    
    # FIIs terminam em 11 (mas não são ETFs)
    if ticker_clean.endswith("11"):
        return "FII"
    
    # BDRs terminam em 34 ou 35
    if ticker_clean.endswith("34") or ticker_clean.endswith("35"):
        return "BDR"
    
    # Default: Ação
    return "Ação"

# --- Funções Auxiliares ---

@st.cache_resource(ttl=1800)
def get_stock_object_yf(ticker_symbol):
    """Retorna o objeto Ticker do yfinance."""
    try:
        stock = yf.Ticker(ticker_symbol)
        if hasattr(stock, 'info') and stock.info:
            return stock
        return None
    except Exception:
        return None

@st.cache_data(ttl=1800)
def get_stock_info_yf(_stock_obj, ticker_symbol):
    """Busca informações gerais da ação."""
    if _stock_obj is None:
        return None
    try:
        info = _stock_obj.info
        if not info:
            return None
        
        data = {
            "ticker": ticker_symbol,
            "nome_longo": info.get('longName', info.get('shortName', ticker_symbol)),
            "setor": info.get('sector', 'N/A'),
            "preco_atual": info.get('regularMarketPrice', info.get('currentPrice', 0)),
            "pl_atual": info.get('trailingPE', 0),
            "payout_ratio": info.get('payoutRatio', 0) * 100 if info.get('payoutRatio') else 0
        }
        return data
    except Exception:
        return None

@st.cache_data(ttl=1800)
def get_dividends_history(_stock_obj, years=5):
    """Busca histórico de dividendos."""
    if _stock_obj is None:
        return pd.DataFrame()
    
    try:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=years*365 + 100)
        dividends = _stock_obj.dividends
        
        if dividends.empty:
            return pd.DataFrame()
        
        # Filtrar período
        dividends_index = dividends.index.tz_localize(None) if dividends.index.tz else dividends.index
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        
        dividends_filtered = dividends[(dividends_index >= start_dt) & (dividends_index <= end_dt)]
        
        return dividends_filtered
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=1800)
def calculate_dividend_metrics(ticker_symbol, years=5):
    """Calcula métricas de dividendos para uma ação."""
    stock = get_stock_object_yf(ticker_symbol)
    if stock is None:
        return None
    
    info = get_stock_info_yf(stock, ticker_symbol)
    if info is None or info['preco_atual'] == 0:
        return None
    
    dividends = get_dividends_history(stock, years)
    if dividends.empty:
        return None
    
    # Calcular métricas
    preco_atual = info['preco_atual']
    
    # DY dos últimos 12 meses
    end_date = datetime.today()
    start_12m = end_date - timedelta(days=365)
    dividends_index = dividends.index.tz_localize(None) if dividends.index.tz else dividends.index
    dividends_12m = dividends[dividends_index >= pd.to_datetime(start_12m)]
    dy_12m = (dividends_12m.sum() / preco_atual * 100) if not dividends_12m.empty and preco_atual > 0 else 0
    
    # Dividendos anuais
    dividends_by_year = dividends.groupby(dividends.index.year).sum()
    dy_medio = dividends_by_year.mean() / preco_atual * 100 if preco_atual > 0 else 0
    
    # Consistência (% de anos com dividendos)
    anos_com_dividendos = len(dividends_by_year)
    consistencia = (anos_com_dividendos / years) * 100
    
    # Crescimento (CAGR)
    if len(dividends_by_year) >= 2:
        start_val = dividends_by_year.iloc[0]
        end_val = dividends_by_year.iloc[-1]
        num_years = len(dividends_by_year) - 1
        if start_val > 0 and num_years > 0:
            cagr = ((end_val / start_val) ** (1 / num_years) - 1) * 100
        else:
            cagr = 0
    else:
        cagr = 0
    
    # Categoria
    categoria = categorize_ticker(ticker_symbol)
    
    # Score composto (ponderação: DY 40%, Consistência 30%, Crescimento 30%)
    score = (dy_12m * 0.4) + (consistencia * 0.3) + (max(0, min(cagr, 20)) * 0.3)
    
    return {
        'ticker': ticker_symbol,
        'nome': info['nome_longo'],
        'categoria': categoria,
        'setor': info['setor'],
        'preco': preco_atual,
        'dy_12m': round(dy_12m, 2),
        'dy_medio': round(dy_medio, 2),
        'consistencia': round(consistencia, 1),
        'cagr_dividendos': round(cagr, 2),
        'anos_com_div': anos_com_dividendos,
        'score': round(score, 2),
        'dividends_history': dividends
    }

def analyze_selected_stocks(selected_tickers, progress_bar=None):
    """Analisa os tickers selecionados."""
    results = []
    total = len(selected_tickers)
    
    for idx, ticker in enumerate(selected_tickers):
        if progress_bar:
            progress_bar.progress((idx + 1) / total, f"Analisando {ticker}...")
        
        metrics = calculate_dividend_metrics(ticker)
        if metrics:
            results.append(metrics)
    
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
st.markdown("""
Este aplicativo analisa **ações, FIIs, BDRs e ETFs** negociados na B3 e cria um portfólio otimizado 
para gerar fluxo de caixa mensal consistente.
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
    
    col1, col2 = st.columns([3, 1])
    with col1:
        categorias_str = ", ".join(categorias_ativas) if categorias_ativas else "Nenhum"
        st.info(f"🔍 Segmentos selecionados: **{categorias_str}**")
    with col2:
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
                
                # Analisar
                progress_bar = st.progress(0)
                df_ranking = analyze_selected_stocks(filtered_tickers, progress_bar)
                progress_bar.empty()
                
                if not df_ranking.empty:
                    st.session_state['df_ranking'] = df_ranking
                    st.success(f"✅ Análise concluída! {len(df_ranking)} ativos com dados de dividendos.")
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
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            categorias_disponiveis = ['Todos'] + sorted(df_ranking['categoria'].unique().tolist())
            categoria_filtro = st.selectbox("Categoria", categorias_disponiveis)
        
        with col2:
            setores_disponiveis = ['Todos'] + sorted(df_ranking['setor'].unique().tolist())
            setor_filtro = st.selectbox("Setor", setores_disponiveis)
        
        with col3:
            dy_minimo = st.slider("DY Mínimo (12M)", 0.0, 15.0, 0.0, 0.5)
        
        with col4:
            consistencia_minima = st.slider("Consistência Mínima (%)", 0, 100, 0, 10)
        
        # Aplicar filtros
        df_filtrado = df_ranking.copy()
        if categoria_filtro != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['categoria'] == categoria_filtro]
        if setor_filtro != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['setor'] == setor_filtro]
        df_filtrado = df_filtrado[df_filtrado['dy_12m'] >= dy_minimo]
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
            width=None,
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
            st.plotly_chart(fig_dy, use_container_width=True)
        
        with col2:
            fig_cat = px.pie(df_filtrado, names='categoria', title='Distribuição por Categoria',
                            color_discrete_map={'Ação': '#1f77b4', 'FII': '#ff7f0e', 
                                              'BDR': '#2ca02c', 'ETF': '#d62728'})
            st.plotly_chart(fig_cat, use_container_width=True)
        
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
        
        st.dataframe(df_categoria, width=None)

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
        if st.button("🚀 Otimizar Portfólio", type="primary"):
            with st.spinner("Otimizando portfólio..."):
                # Filtrar ações com DY mínimo
                df_elegivel = df_ranking[df_ranking['dy_12m'] >= dy_minimo_port].copy()
                
                if df_elegivel.empty:
                    st.error("Nenhum ativo encontrado com o DY mínimo especificado. Tente reduzir o valor.")
                else:
                    # Otimizar
                    portfolio = optimize_portfolio(df_elegivel, capital_total, lote_minimo)
                    
                    if portfolio is not None and not portfolio.empty:
                        st.session_state['portfolio_otimizado'] = portfolio
                        st.success("✅ Portfólio otimizado com sucesso!")
                    else:
                        st.error("Não foi possível criar um portfólio com os parâmetros especificados. Tente aumentar o capital ou reduzir o lote mínimo.")
        
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
                width=None
            )
            
            # Gráficos
            col1, col2 = st.columns(2)
            
            with col1:
                fig_pizza = px.pie(df_port_display, values='Valor Investido (R$)', names='Ticker',
                                   title='Distribuição do Capital por Ativo')
                st.plotly_chart(fig_pizza, use_container_width=True)
            
            with col2:
                fig_cat_port = px.pie(df_port_display, values='Valor Investido (R$)', names='Categoria',
                                      title='Distribuição do Capital por Categoria',
                                      color='Categoria',
                                      color_discrete_map={'Ação': '#1f77b4', 'FII': '#ff7f0e', 
                                                         'BDR': '#2ca02c', 'ETF': '#d62728'})
                st.plotly_chart(fig_cat_port, use_container_width=True)
            
            # Calendário de dividendos
            st.subheader("📅 Calendário Estimado de Dividendos")
            st.info("Baseado no padrão de pagamentos dos últimos 24 meses")
            
            calendario = create_dividend_calendar(portfolio)
            if calendario is not None and not calendario.empty:
                # Gráfico mensal
                fig_calendario = px.bar(calendario, x='mes', y='valor_estimado',
                                       title='Fluxo Mensal Estimado de Dividendos',
                                       labels={'valor_estimado': 'Valor (R$)', 'mes': 'Mês'},
                                       text='valor_estimado')
                fig_calendario.update_traces(texttemplate='R$ %{text:.0f}', textposition='outside')
                st.plotly_chart(fig_calendario, use_container_width=True)
                
                # Tabela detalhada
                with st.expander("📊 Detalhes Mensais"):
                    df_cal_display = calendario[['mes', 'valor_estimado', 'acoes_pagantes']].copy()
                    df_cal_display.columns = ['Mês', 'Valor Estimado (R$)', 'Ativos Pagantes']
                    st.dataframe(
                        df_cal_display.style.format({'Valor Estimado (R$)': 'R$ {:.2f}'}),
                        width=None
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
            st.plotly_chart(fig_annual, use_container_width=True)
            
            # Gráfico mensal
            st.subheader("📈 Evolução Mensal dos Dividendos")
            fig_monthly = go.Figure()
            fig_monthly.add_trace(go.Scatter(x=df_monthly['mes'], y=df_monthly['dividendos'],
                                           mode='lines+markers', name='Dividendos'))
            fig_monthly.add_hline(y=media_mensal, line_dash="dash", line_color="red",
                                 annotation_text=f"Média: R$ {media_mensal:.2f}")
            fig_monthly.update_layout(title='Dividendos Mensais Históricos',
                                     xaxis_title='Mês', yaxis_title='Dividendos (R$)')
            st.plotly_chart(fig_monthly, use_container_width=True)
            
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
                        width=None
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
                        width=None
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
