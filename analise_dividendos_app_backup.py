import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import traceback # Para debug de erros

# --- Configurações da Página Streamlit ---
st.set_page_config(layout="wide", page_title="Análise Aprofundada de Ações para Dividendos")

# --- Funções Auxiliares ---

@st.cache_resource(ttl=1800) # Cache de 30 minutos para o objeto Ticker
def get_stock_object_yf(ticker_symbol):
    """Retorna o objeto Ticker do yfinance. Cacheado como recurso."""
    # st.write(f"DEBUG: Criando/Buscando objeto Ticker para: {ticker_symbol}") # Para debug
    try:
        stock = yf.Ticker(ticker_symbol)
        if hasattr(stock, 'info') and stock.info and stock.info.get('regularMarketPrice') is not None:
            return stock
        elif hasattr(stock, '_history') and stock._history is not None and len(stock._history) > 0:
             return stock
        else:
            return None
    except Exception as e:
        return None

@st.cache_data(ttl=1800) # Cache para os dados extraídos
def get_stock_info_yf(_stock_obj, ticker_symbol_arg_for_error_msg):
    """Busca informações gerais e métricas de valuation atuais da ação via yfinance, usando o objeto Ticker."""
    if _stock_obj is None: return None
    try:
        info = _stock_obj.info
        if not info:
             return { "nome_longo": ticker_symbol_arg_for_error_msg, "setor": "N/A", "industria": "N/A", "resumo_negocio": "N/A",
                     "pl_atual": "N/A", "pvp_atual": "N/A", "payout_ratio": "N/A", "beta": "N/A",
                     "market_cap": 0, "preco_atual": "N/A", "website": "#"}
        
        data = {
            "nome_longo": info.get('longName', info.get('shortName', ticker_symbol_arg_for_error_msg)),
            "setor": info.get('sector', 'N/A'),
            "industria": info.get('industry', 'N/A'),
            "resumo_negocio": info.get('longBusinessSummary', 'N/A'),
            "pl_atual": round(info.get('trailingPE'), 2) if isinstance(info.get('trailingPE'), (int, float)) else "N/A",
            "pvp_atual": round(info.get('priceToBook'), 2) if isinstance(info.get('priceToBook'), (int, float)) else "N/A",
            "payout_ratio": round(info.get('payoutRatio', 0) * 100, 2) if isinstance(info.get('payoutRatio'), (int, float)) and info.get('payoutRatio') >= 0 else "N/A",
            "beta": round(info.get('beta'), 2) if isinstance(info.get('beta'), (int, float)) else "N/A",
            "market_cap": info.get('marketCap', 0),
            "preco_atual": info.get('regularMarketPrice', info.get('currentPrice', "N/A")),
            "website": info.get('website', "#")
        }
        return data
    except Exception as e:
        st.error(f"Erro crítico ao buscar informações detalhadas para {ticker_symbol_arg_for_error_msg} via yfinance: {e}")
        return None

@st.cache_data(ttl=1800)
def calculate_dy_last_12_months(_stock_obj, current_price_arg, ticker_symbol_arg_for_error_msg):
    if _stock_obj is None: return "N/A"
    if not isinstance(current_price_arg, (int, float)) or current_price_arg <= 0: return 0.0

    try:
        end_date_dy = datetime.today().date()
        start_date_dy = end_date_dy - timedelta(days=365)
        dividends_all = _stock_obj.dividends
        if dividends_all.empty: return 0.0

        dividends_index_naive = dividends_all.index.tz_localize(None)
        start_dt_naive = pd.to_datetime(start_date_dy)
        end_dt_naive = pd.to_datetime(end_date_dy)
        dividends_l12m = dividends_all[(dividends_index_naive >= start_dt_naive) & (dividends_index_naive <= end_dt_naive)]
        
        if dividends_l12m.empty: return 0.0
        sum_dividends_l12m = dividends_l12m.sum()
        if sum_dividends_l12m <= 0: return 0.0
            
        dy_l12m = (sum_dividends_l12m / current_price_arg) * 100
        return round(dy_l12m, 2)
    except Exception: return "N/A"

@st.cache_data(ttl=3600)
def get_historical_prices_yf(_stock_obj, start_date, end_date, ticker_symbol_arg_for_error_msg):
    if _stock_obj is None: return None
    try:
        hist_data = _stock_obj.history(start=datetime(start_date.year, start_date.month, start_date.day), 
                                       end=datetime(end_date.year, end_date.month, end_date.day) + timedelta(days=1))
        if hist_data.empty: return None
        return hist_data[['Close', 'Volume']]
    except Exception: return None

@st.cache_data(ttl=3600)
def get_dividend_data_yf(_stock_obj, start_date_period, end_date_period, ticker_symbol_arg_for_error_msg):
    if _stock_obj is None: return pd.DataFrame(columns=['Ano', 'Dividendos Anuais (R$)'])
    try:
        dividends = _stock_obj.dividends
        if dividends.empty: return pd.DataFrame(columns=['Ano', 'Dividendos Anuais (R$)'])

        start_dt_naive = pd.to_datetime(start_date_period)
        end_dt_naive = pd.to_datetime(end_date_period)
        dividends_index_naive = dividends.index.tz_localize(None)
        dividends_in_period = dividends[(dividends_index_naive >= start_dt_naive) & (dividends_index_naive <= end_dt_naive)]
        
        if dividends_in_period.empty: return pd.DataFrame(columns=['Ano', 'Dividendos Anuais (R$)'])

        annual_dividends_list = []
        for year, group_df in dividends_in_period.groupby(dividends_in_period.index.year):
            annual_dividends_list.append({'Ano': year, 'Dividendos Anuais (R$)': group_df.sum()})
        
        return pd.DataFrame(annual_dividends_list).sort_values(by='Ano') if annual_dividends_list else pd.DataFrame(columns=['Ano', 'Dividendos Anuais (R$)'])
    except Exception: return pd.DataFrame(columns=['Ano', 'Dividendos Anuais (R$)'])

def calculate_cagr(series_values):
    numeric_series = pd.to_numeric(series_values, errors='coerce').dropna()
    positive_series = numeric_series[numeric_series > 0]
    if len(positive_series) < 2: return "N/A"
    start_value, end_value = positive_series.iloc[0], positive_series.iloc[-1]
    num_years = positive_series.index.max() - positive_series.index.min()
    if isinstance(series_values.index, pd.RangeIndex) or num_years == 0 :
         num_years = len(positive_series) -1
    if num_years <= 0 : return "N/A (período insuficiente)"
    if start_value <= 0: return "N/A (valor inicial <=0)"
    cagr = ((end_value / start_value) ** (1 / num_years)) - 1
    return round(cagr * 100, 2)

def calculate_historical_dy(annual_dividends_df, historical_prices_df):
    if annual_dividends_df.empty or historical_prices_df is None or historical_prices_df.empty:
        return pd.DataFrame(columns=['Ano', 'Preço Base (R$)', 'DY Anual (%)']), "N/A", "N/A"
    
    historical_dys_calc = []
    prices_df_naive_index = historical_prices_df.copy()
    if prices_df_naive_index.index.tz is not None:
        prices_df_naive_index.index = prices_df_naive_index.index.tz_localize(None)

    for _, row in annual_dividends_df.iterrows():
        year, annual_dividend_value = int(row['Ano']), row['Dividendos Anuais (R$)']
        if not isinstance(annual_dividend_value, (int, float)) or annual_dividend_value <= 0:
            historical_dys_calc.append({'Ano': year, 'Preço Base (R$)': 'N/A', 'DY Anual (%)': 'N/A (Div Inválido)'})
            continue
        
        price_target_date_end_prev_year = pd.to_datetime(datetime(year - 1, 12, 31))
        price_target_date_start_prev_year = pd.to_datetime(datetime(year - 1, 12, 1))
        prices_prev_year = prices_df_naive_index[(prices_df_naive_index.index >= price_target_date_start_prev_year) & (prices_df_naive_index.index <= price_target_date_end_prev_year)]
        base_price = prices_prev_year['Close'].iloc[-1] if not prices_prev_year.empty else np.nan

        if pd.notna(base_price) and base_price > 0:
            historical_dys_calc.append({'Ano': year, 'Preço Base (R$)': round(base_price,2), 'DY Anual (%)': round((annual_dividend_value / base_price) * 100, 2)})
        else:
            historical_dys_calc.append({'Ano': year, 'Preço Base (R$)': 'N/D (Preço)', 'DY Anual (%)': 'N/D (Preço)'})
    
    df_historical_dys_final = pd.DataFrame(historical_dys_calc)
    valid_dys = pd.to_numeric(df_historical_dys_final['DY Anual (%)'], errors='coerce').dropna()
    avg_dy_value = round(valid_dys.mean(), 2) if not valid_dys.empty else "N/A"
    
    divs_for_cagr = annual_dividends_df.set_index('Ano')['Dividendos Anuais (R$)']
    cagr_dividends_value = calculate_cagr(divs_for_cagr)
    return df_historical_dys_final, avg_dy_value, cagr_dividends_value

def calculate_fibonacci_levels(price_series_period):
    if price_series_period is None or len(price_series_period) < 2: return None, None
    max_price, min_price = price_series_period.max(), price_series_period.min()
    price_range = max_price - min_price
    if price_range == 0: return None, None

    fib_retracement_levels = {
        "0.0% (Mín)": min_price, "23.6%": max_price - (price_range * 0.236),
        "38.2%": max_price - (price_range * 0.382), "50.0%": max_price - (price_range * 0.5),
        "61.8%": max_price - (price_range * 0.618), "78.6%": max_price - (price_range * 0.786),
        "100.0% (Máx)": max_price
    }
    fib_projection_levels = {
        "127.2%": max_price + (price_range * 0.272), "161.8%": max_price + (price_range * 0.618),
        "200.0%": max_price + price_range, "261.8%": max_price + (price_range * 1.618)
    }
    return fib_retracement_levels, fib_projection_levels

# --- Interface Principal ---
st.title("🔎 Análise Aprofundada de Ações para Carteira de Dividendos")

st.sidebar.header("⚙️ Configurações da Análise")
ticker_input_sb = st.sidebar.text_input("Ticker da Ação (ex: ITSA4.SA)", value=st.session_state.get("last_ticker", "ITSA4.SA"), key="ticker_input_widget").upper()
default_end_date = datetime.today().date()
default_start_date = default_end_date - timedelta(days=5*365 + 2)
col_date1, col_date2 = st.sidebar.columns(2)
start_date_input_sb = col_date1.date_input("Data Inicial Histórico", value=st.session_state.get("last_start_date", default_start_date), min_value=datetime(1990,1,1).date(), max_value=default_end_date - timedelta(days=1), key="start_date_widget")
end_date_input_sb = col_date2.date_input("Data Final Histórico", value=st.session_state.get("last_end_date", default_end_date), min_value=start_date_input_sb + timedelta(days=1) if start_date_input_sb else datetime(1990,1,2).date(), max_value=default_end_date, key="end_date_widget")

with st.sidebar.form(key="analysis_form"):
    analyze_button_form = st.form_submit_button(label="🚀 Analisar Ação")

if analyze_button_form:
    st.session_state.last_ticker = ticker_input_sb
    st.session_state.last_start_date = start_date_input_sb
    st.session_state.last_end_date = end_date_input_sb

active_ticker = st.session_state.get("last_ticker", None)
active_start_date = st.session_state.get("last_start_date", None)
active_end_date = st.session_state.get("last_end_date", None)

if active_ticker and active_start_date and active_end_date:
    if active_start_date >= active_end_date:
        st.error("A data inicial deve ser anterior à data final.")
    else:
        with st.spinner(f"Buscando e processando dados para {active_ticker}..."):
            stock_obj = get_stock_object_yf(active_ticker)
            if stock_obj is None:
                st.error(f"Não foi possível obter informações para o ticker {active_ticker}. Verifique se o ticker é válido ou tente mais tarde.")
            else:
                info_data = get_stock_info_yf(stock_obj, active_ticker)
                dy_l12m = "N/A"
                if info_data and info_data.get('preco_atual') != "N/A" and isinstance(info_data.get('preco_atual'), (int,float)):
                    dy_l12m = calculate_dy_last_12_months(stock_obj, info_data['preco_atual'], active_ticker)
                
                hist_prices_start_for_dy_calc = active_start_date - timedelta(days=400)
                historical_prices_df = get_historical_prices_yf(stock_obj, hist_prices_start_for_dy_calc, active_end_date, active_ticker)
                annual_dividends_df = get_dividend_data_yf(stock_obj, active_start_date, active_end_date, active_ticker)
                df_historical_dys, avg_dy_hist, cagr_divs = calculate_historical_dy(annual_dividends_df, historical_prices_df)

                if info_data:
                    st.header(f"{info_data.get('nome_longo', active_ticker)} ({active_ticker})")
                    st.caption(f"Setor: {info_data.get('setor', 'N/A')} | Indústria: {info_data.get('industria', 'N/A')} | [Website]({info_data.get('website', '#')})")
                    if info_data.get('resumo_negocio') not in ['N/A', None, ""]:
                        with st.expander("Resumo do Negócio"): st.write(info_data['resumo_negocio'])

                    st.subheader("📈 Métricas de Valuation e Mercado (Atuais)")
                    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                    preco_fmt = f"R$ {info_data.get('preco_atual', 'N/A')}" if isinstance(info_data.get('preco_atual'), (int, float)) else "N/A"
                    col_m1.metric("Preço Atual", preco_fmt)
                    col_m2.metric("DY (Últimos 12M)", f"{dy_l12m}%" if dy_l12m != "N/A" else "N/A")
                    col_m3.metric("P/L (Trailing)", f"{info_data.get('pl_atual', 'N/A')}")
                    col_m4.metric("P/VP", f"{info_data.get('pvp_atual', 'N/A')}")
                    col_m5, col_m6, col_m7 = st.columns(3)
                    p_fmt = f"{info_data.get('payout_ratio', 'N/A')}%" if info_data.get('payout_ratio') != "N/A" else "N/A"
                    if info_data.get('payout_ratio') != "N/A":
                        try:
                            p_val = float(info_data['payout_ratio']);
                            if p_val > 100 or p_val < 0 : p_fmt += " ⚠️"
                        except ValueError: pass
                    col_m5.metric("Payout Ratio", p_fmt)
                    col_m6.metric("Beta (vs Ibov)", f"{info_data.get('beta', 'N/A')}")
                    mc_val = info_data.get('market_cap', 0)
                    mc_fmt = f"R$ {mc_val:,.0f}" if isinstance(mc_val, (int, float)) and mc_val > 0 else "N/A"
                    col_m7.metric("Market Cap", mc_fmt)

                    st.subheader("🚦 Avaliação de Indicadores Chave (Heurísticas)")
                    alerts = []
                    if dy_l12m != "N/A" and avg_dy_hist != "N/A":
                        try:
                            dy_a, dy_h, thr = float(dy_l12m), float(avg_dy_hist), 0.20
                            if dy_a < 2.0: alerts.append(f"🔸 **DY Atual ({dy_a:.2f}%) baixo.**")
                            elif dy_a > dy_h * (1 + thr): alerts.append(f"✅ **DY Atual ({dy_a:.2f}%) > Média Hist. ({dy_h:.2f}%).**")
                            elif dy_a < dy_h * (1 - thr): alerts.append(f"⚠️ **DY Atual ({dy_a:.2f}%) < Média Hist. ({dy_h:.2f}%).**")
                        except ValueError: pass
                    if info_data.get('payout_ratio') != "N/A":
                        try:
                            p = float(info_data['payout_ratio'])
                            if p > 85 and p <=100: alerts.append(f"🔸 **Payout ({p:.0f}%) elevado.**")
                            elif p > 100: alerts.append(f"🔥 **Payout ({p:.0f}%) > 100%!**")
                            elif p < 0: alerts.append(f"🔥 **Payout ({p:.0f}%) negativo!**")
                        except ValueError: pass
                    if info_data.get('pl_atual') != "N/A":
                        try:
                            pl_v = float(info_data['pl_atual'])
                            if pl_v < 0: alerts.append(f"🔥 **P/L Negativo ({pl_v:.2f}).**")
                            elif pl_v < 5 and pl_v > 0: alerts.append(f"✅ **P/L Baixo ({pl_v:.2f}).**")
                            elif pl_v > 20: alerts.append(f"🔸 **P/L Elevado ({pl_v:.2f}).**")
                        except ValueError: pass
                    if not alerts: st.info("Nenhum alerta específico dos indicadores chave. Faça sua análise completa.")
                    else:
                        for m in alerts:
                            if "🔥" in m: st.error(m)
                            elif "⚠️" in m: st.warning(m)
                            elif "🔸" in m: st.warning(m)
                            else: st.success(m)
                    st.caption("*Heurísticas são simplificações e não substituem análise aprofundada.*")

                    st.subheader("📜 Análise de Dividendos, Preços e Fibonacci")
                    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dividendos", "💹 DY Histórico", "📈 Preços", "📉 Fibonacci"])
                    with tab1:
                        if annual_dividends_df is not None and not annual_dividends_df.empty:
                            valid_div_y = annual_dividends_df[pd.to_numeric(annual_dividends_df['Dividendos Anuais (R$)'], errors='coerce').fillna(0) > 0]
                            st.metric(f"CAGR dos Dividendos Anuais ({len(valid_div_y)} anos com div > 0)", f"{cagr_divs}%" if cagr_divs != "N/A" else "N/A")
                            fig_ad = px.bar(annual_dividends_df, x='Ano', y='Dividendos Anuais (R$)', title=f"Dividendos Anuais Pagos por {active_ticker}")
                            st.plotly_chart(fig_ad, use_container_width=True)
                            with st.expander("Dados de Dividendos Anuais"): st.dataframe(annual_dividends_df.set_index('Ano'))
                        else: st.info(f"Sem dados de dividendos para {active_ticker} no período.")
                    with tab2:
                        if df_historical_dys is not None and not df_historical_dys.empty:
                            n_v_dy = len(df_historical_dys[pd.to_numeric(df_historical_dys['DY Anual (%)'], errors='coerce').notna()])
                            st.metric(f"DY Médio Histórico ({n_v_dy} anos)", f"{avg_dy_hist}%" if avg_dy_hist != "N/A" else "N/A")
                            df_p_dy = df_historical_dys[pd.to_numeric(df_historical_dys['DY Anual (%)'], errors='coerce').notna()].copy()
                            if not df_p_dy.empty:
                                df_p_dy['DY Anual (%)'] = pd.to_numeric(df_p_dy['DY Anual (%)'])
                                fig_dy_h = px.bar(df_p_dy, x='Ano', y='DY Anual (%)', title=f"DY Anual Histórico de {active_ticker}", text='DY Anual (%)')
                                fig_dy_h.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
                                if avg_dy_hist != "N/A": fig_dy_h.add_hline(y=float(avg_dy_hist), line_dash="dash", line_color="red", annotation_text=f"Média Hist: {avg_dy_hist}%")
                                st.plotly_chart(fig_dy_h, use_container_width=True)
                            with st.expander("Dados de DY Histórico Detalhado"): st.dataframe(df_historical_dys.set_index('Ano'))
                        else: st.info(f"Não foi possível calcular DY histórico para {active_ticker}.")
                    with tab3:
                        if historical_prices_df is not None and not historical_prices_df.empty:
                            prices_idx_tz = historical_prices_df.index.tz
                            start_dt_plot = pd.to_datetime(active_start_date).tz_localize(prices_idx_tz if prices_idx_tz else None)
                            end_dt_plot = pd.to_datetime(active_end_date).tz_localize(prices_idx_tz if prices_idx_tz else None)
                            prices_plot = historical_prices_df[(historical_prices_df.index >= start_dt_plot) & (historical_prices_df.index <= end_dt_plot)]
                            if not prices_plot.empty:
                                fig_p = go.Figure(data=[go.Scatter(x=prices_plot.index, y=prices_plot['Close'], name='Preço')])
                                fig_p.update_layout(title=f"Preço de Fechamento de {active_ticker}", xaxis_rangeslider_visible=True)
                                st.plotly_chart(fig_p, use_container_width=True)
                            else: st.info("Sem dados de preço para o período de visualização.")
                        else: st.info(f"Sem dados de preço para {active_ticker} no período histórico.")
                    with tab4: # Fibonacci
                        st.subheader(f"Análise de Fibonacci para {active_ticker}")
                        if historical_prices_df is not None and not historical_prices_df.empty:
                            prices_idx_tz_fib = historical_prices_df.index.tz
                            start_dt_fib = pd.to_datetime(active_start_date).tz_localize(prices_idx_tz_fib if prices_idx_tz_fib else None)
                            end_dt_fib = pd.to_datetime(active_end_date).tz_localize(prices_idx_tz_fib if prices_idx_tz_fib else None)
                            prices_fib_calc = historical_prices_df[(historical_prices_df.index >= start_dt_fib) & (historical_prices_df.index <= end_dt_fib)]['Close']
                            if not prices_fib_calc.empty and len(prices_fib_calc) > 1:
                                retracements, projections = calculate_fibonacci_levels(prices_fib_calc)
                                fig_f = go.Figure()
                                fig_f.add_trace(go.Scatter(x=prices_fib_calc.index, y=prices_fib_calc, mode='lines', name='Preço', line=dict(color='blue')))
                                current_p_fib = info_data.get('preco_atual', prices_fib_calc.iloc[-1])
                                if retracements:
                                    st.write("**Níveis de Retração Fibonacci (Suporte/Resistência):**")
                                    cols_r = st.columns(len(retracements))
                                    for i, (lvl_n, lvl_p) in enumerate(retracements.items()):
                                        fig_f.add_hline(y=lvl_p, line_dash="dash", annotation_text=f"{lvl_n}: {lvl_p:.2f}", line_color='rgba(255,165,0,0.7)')
                                        cols_r[i].metric(f"Ret. {lvl_n}", f"R$ {lvl_p:.2f}", f"{((current_p_fib / lvl_p) - 1)*100 if lvl_p > 0 else 0:.1f}% vs Atual", delta_color="off" if "Mín" in lvl_n or "Máx" in lvl_n else ("normal" if current_p_fib >= lvl_p else "inverse"))
                                if projections:
                                    st.write("**Níveis de Projeção Fibonacci (Alvos Potenciais em Alta):**")
                                    cols_p = st.columns(len(projections))
                                    for i, (lvl_n, lvl_p) in enumerate(projections.items()):
                                        if lvl_p > prices_fib_calc.max(): fig_f.add_hline(y=lvl_p, line_dash="dot", annotation_text=f"Proj. {lvl_n}: {lvl_p:.2f}", line_color='rgba(0,128,0,0.7)')
                                        cols_p[i].metric(f"Proj. {lvl_n}", f"R$ {lvl_p:.2f}", f"{((lvl_p / current_p_fib) - 1)*100 if current_p_fib > 0 else 0:.1f}% Potencial", delta_color="normal")
                                fig_f.update_layout(title=f"Preço de {active_ticker} com Níveis Fibonacci", xaxis_rangeslider_visible=True, height=600)
                                st.plotly_chart(fig_f, use_container_width=True)
                                st.caption("Fibonacci traçado com base no máx/mín do período selecionado. Interprete com cautela.")
                            else: st.info("Dados insuficientes para Fibonacci no período.")
                        else: st.info(f"Sem dados de preço para Fibonacci para {active_ticker}.")

                    st.subheader("📝 Minhas Anotações e Avaliação (Simulação)")
                    form_key_notes = f"form_anotacoes_{active_ticker}"
                    with st.form(key=form_key_notes):
                        notes_key = f"notes_text_area_{active_ticker}"
                        decision_key = f"decision_selectbox_{active_ticker}"
                        user_notes = st.text_area("Observações:", value=st.session_state.get(notes_key, ""), height=100, key=notes_key + "_widget")
                        options = ["Não Avaliado", "Monitorar", "Potencial Compra", "Manter Posição", "Potencial Venda", "Evitar"]
                        idx = options.index(st.session_state.get(decision_key, "Não Avaliado")) if st.session_state.get(decision_key, "Não Avaliado") in options else 0
                        user_decision = st.selectbox("Minha Avaliação:", options=options, index=idx, key=decision_key + "_widget")
                        if st.form_submit_button(f"Salvar para {active_ticker}"):
                            st.session_state[notes_key], st.session_state[decision_key] = user_notes, user_decision
                            if 'portfolio_simulado' not in st.session_state: st.session_state.portfolio_simulado = {}
                            st.session_state.portfolio_simulado[active_ticker] = {'nome': info_data.get('nome_longo', active_ticker), 'avaliacao': user_decision, 'notas': user_notes}
                            st.success(f"Anotações para {active_ticker} salvas!")
                else: # if info_data
                    st.error(f"Não foi possível carregar informações de base para {active_ticker}. Verifique o ticker ou a conexão.")
elif not active_ticker and st.session_state.get("analyze_button_form"): # Se botão foi clicado mas ticker está vazio
    st.warning("Por favor, insira um ticker para análise.")
elif "last_ticker" not in st.session_state : # Estado inicial absoluto
    st.info("⬅️ Utilize a barra lateral para inserir um ticker, ajustar o período e clique em 'Analisar Ação'.")

st.sidebar.markdown("---")
st.sidebar.header("📋 Resumo do Portfólio Avaliado")
if 'portfolio_simulado' in st.session_state and st.session_state.portfolio_simulado:
    for t_sb, d_sb in st.session_state.portfolio_simulado.items():
        st.sidebar.markdown(f"**{d_sb.get('nome', t_sb)}:** {d_sb.get('avaliacao', 'N/A')}")
    if st.sidebar.button("Limpar Portfólio Avaliado", key="clear_portfolio_sb_btn_widget"):
        st.session_state.portfolio_simulado = {}
        keys_del = [k for k in st.session_state.keys() if "_notes_area_" in k or "_decision_selectbox_" in k or "last_" in k]
        for k_del_item in keys_del: del st.session_state[k_del_item]
        st.rerun()
else:
    st.sidebar.info("Nenhuma ação avaliada e salva na sessão ainda.")

st.markdown("---")
st.caption("Desenvolvido como ferramenta educacional. Dados via Yahoo Finance. Não constitui recomendação de investimento.")