"""
Formatadores para dados financeiros e saídas do aplicativo.
"""

import pandas as pd
from datetime import datetime
from typing import Union, List, Dict, Any


def format_currency(value: float, prefix: str = "R$", decimals: int = 2) -> str:
    """
    Formata valor monetário.
    
    Args:
        value: Valor numérico
        prefix: Prefixo da moeda (padrão: R$)
        decimals: Casas decimais
        
    Returns:
        String formatada (ex: "R$ 1.234,56")
    """
    if value is None or pd.isna(value):
        return f"{prefix} 0,00"
    
    try:
        # Formatar com separadores
        formatted = f"{abs(value):,.{decimals}f}"
        # Trocar , por . e . por ,
        formatted = formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
        
        # Adicionar sinal de negativo se necessário
        if value < 0:
            return f"-{prefix} {formatted}"
        return f"{prefix} {formatted}"
    except:
        return f"{prefix} 0,00"


def format_percentage(value: float, decimals: int = 2, show_sign: bool = False) -> str:
    """
    Formata percentual.
    
    Args:
        value: Valor percentual
        decimals: Casas decimais
        show_sign: Mostrar sinal + para valores positivos
        
    Returns:
        String formatada (ex: "12,34%")
    """
    if value is None or pd.isna(value):
        return "0,00%"
    
    try:
        formatted = f"{value:.{decimals}f}".replace('.', ',')
        
        if show_sign and value > 0:
            return f"+{formatted}%"
        return f"{formatted}%"
    except:
        return "0,00%"


def format_number(value: float, decimals: int = 2, thousands_sep: bool = True) -> str:
    """
    Formata número.
    
    Args:
        value: Valor numérico
        decimals: Casas decimais
        thousands_sep: Usar separador de milhares
        
    Returns:
        String formatada
    """
    if value is None or pd.isna(value):
        return "0"
    
    try:
        if thousands_sep:
            formatted = f"{value:,.{decimals}f}"
            # Trocar , por . e . por ,
            return formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
        else:
            return f"{value:.{decimals}f}".replace('.', ',')
    except:
        return "0"


def format_date(date: Union[datetime, pd.Timestamp, str], format_str: str = "%d/%m/%Y") -> str:
    """
    Formata data.
    
    Args:
        date: Data a formatar
        format_str: String de formato
        
    Returns:
        String formatada (ex: "31/12/2024")
    """
    if date is None:
        return "-"
    
    try:
        if isinstance(date, str):
            date = pd.to_datetime(date)
        elif isinstance(date, pd.Timestamp):
            date = date.to_pydatetime()
        
        return date.strftime(format_str)
    except:
        return str(date)


def format_ticker(ticker: str, remove_sa: bool = True) -> str:
    """
    Formata ticker removendo .SA se necessário.
    
    Args:
        ticker: Ticker a formatar
        remove_sa: Remover sufixo .SA
        
    Returns:
        Ticker formatado
    """
    if not ticker:
        return ""
    
    if remove_sa and ticker.endswith('.SA'):
        return ticker.replace('.SA', '')
    
    return ticker


def format_large_number(value: float, precision: int = 1) -> str:
    """
    Formata números grandes com sufixos (K, M, B).
    
    Args:
        value: Valor numérico
        precision: Casas decimais
        
    Returns:
        String formatada (ex: "1,5M")
    """
    if value is None or pd.isna(value):
        return "0"
    
    abs_value = abs(value)
    
    try:
        if abs_value >= 1_000_000_000:  # Bilhões
            formatted = f"{value / 1_000_000_000:.{precision}f}B"
        elif abs_value >= 1_000_000:  # Milhões
            formatted = f"{value / 1_000_000:.{precision}f}M"
        elif abs_value >= 1_000:  # Milhares
            formatted = f"{value / 1_000:.{precision}f}K"
        else:
            formatted = f"{value:.{precision}f}"
        
        return formatted.replace('.', ',')
    except:
        return str(value)


def format_score(score: float) -> str:
    """
    Formata score com emoji baseado no valor.
    
    Args:
        score: Score a formatar
        
    Returns:
        String formatada com emoji
    """
    if score is None or pd.isna(score):
        return "❓ 0,00"
    
    formatted_score = format_number(score, decimals=2)
    
    if score >= 20:
        emoji = "🏆"  # Excelente
    elif score >= 15:
        emoji = "🥇"  # Muito bom
    elif score >= 10:
        emoji = "🥈"  # Bom
    elif score >= 5:
        emoji = "🥉"  # Regular
    else:
        emoji = "⚠️"  # Baixo
    
    return f"{emoji} {formatted_score}"


def format_consistency(consistency: float) -> str:
    """
    Formata consistência com emoji.
    
    Args:
        consistency: Consistência (%)
        
    Returns:
        String formatada com emoji
    """
    if consistency is None or pd.isna(consistency):
        return "❓ 0%"
    
    formatted_consistency = format_percentage(consistency, decimals=1)
    
    if consistency >= 90:
        emoji = "💎"  # Excelente
    elif consistency >= 70:
        emoji = "✨"  # Bom
    elif consistency >= 50:
        emoji = "⭐"  # Regular
    else:
        emoji = "⚠️"  # Baixo
    
    return f"{emoji} {formatted_consistency}"


def format_category_badge(categoria: str) -> str:
    """
    Formata categoria com emoji.
    
    Args:
        categoria: Categoria do ativo
        
    Returns:
        String formatada com emoji
    """
    emojis = {
        'Ação': '📈',
        'FII': '🏢',
        'BDR': '🌎',
        'ETF': '📊'
    }
    
    emoji = emojis.get(categoria, '❓')
    return f"{emoji} {categoria}"


def format_month_name(month: int, short: bool = False) -> str:
    """
    Formata nome do mês em português.
    
    Args:
        month: Número do mês (1-12)
        short: Usar formato curto (Jan, Fev, ...)
        
    Returns:
        Nome do mês em português
    """
    if short:
        months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                  'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    else:
        months = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                  'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    
    if 1 <= month <= 12:
        return months[month - 1]
    return str(month)


def format_roi(roi: float, period_years: int = 1) -> str:
    """
    Formata ROI (Return on Investment).
    
    Args:
        roi: ROI percentual
        period_years: Período em anos
        
    Returns:
        String formatada
    """
    if roi is None or pd.isna(roi):
        return "0,00% ao ano"
    
    formatted = format_percentage(roi, decimals=2, show_sign=True)
    
    if period_years == 1:
        return f"{formatted} ao ano"
    else:
        return f"{formatted} em {period_years} anos"


def format_dataframe_for_display(df: pd.DataFrame, 
                                   currency_cols: List[str] = None,
                                   percentage_cols: List[str] = None,
                                   number_cols: List[str] = None) -> pd.DataFrame:
    """
    Formata DataFrame para exibição no Streamlit.
    
    Args:
        df: DataFrame a formatar
        currency_cols: Colunas monetárias
        percentage_cols: Colunas percentuais
        number_cols: Colunas numéricas
        
    Returns:
        DataFrame formatado
    """
    if df is None or df.empty:
        return df
    
    df_display = df.copy()
    
    # Formatar colunas monetárias
    if currency_cols:
        for col in currency_cols:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(format_currency)
    
    # Formatar colunas percentuais
    if percentage_cols:
        for col in percentage_cols:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(format_percentage)
    
    # Formatar colunas numéricas
    if number_cols:
        for col in number_cols:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(format_number)
    
    return df_display


def create_summary_text(portfolio_df: pd.DataFrame) -> str:
    """
    Cria texto resumo do portfólio.
    
    Args:
        portfolio_df: DataFrame do portfólio
        
    Returns:
        Texto formatado
    """
    if portfolio_df is None or portfolio_df.empty:
        return "Portfólio vazio"
    
    total_investido = portfolio_df['valor_investido'].sum()
    total_anual = portfolio_df['dividendos_anuais_estimados'].sum()
    total_mensal = total_anual / 12
    dy_medio = (total_anual / total_investido * 100) if total_investido > 0 else 0
    num_ativos = len(portfolio_df)
    
    summary = f"""
    **📊 Resumo do Portfólio**
    
    - **Ativos:** {num_ativos}
    - **Investimento Total:** {format_currency(total_investido)}
    - **DY Médio:** {format_percentage(dy_medio)}
    - **Dividendos Anuais:** {format_currency(total_anual)}
    - **Dividendos Mensais:** {format_currency(total_mensal)}
    """
    
    return summary


def export_to_dict(obj: Any) -> Dict:
    """
    Converte objeto para dicionário serializável.
    
    Args:
        obj: Objeto a converter
        
    Returns:
        Dicionário
    """
    if isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient='records')
    elif isinstance(obj, pd.Series):
        return obj.to_dict()
    elif isinstance(obj, (datetime, pd.Timestamp)):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: export_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [export_to_dict(item) for item in obj]
    else:
        return obj
