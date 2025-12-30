"""
Otimização de portfólio de dividendos.
"""

import pandas as pd
from typing import Optional
from config.settings import config, get_lot_size
from utils.logger import setup_logger

logger = setup_logger(__name__)


def optimize_portfolio(df_stocks: pd.DataFrame, 
                       capital_total: float,
                       min_dy: float = None) -> Optional[pd.DataFrame]:
    """
    Otimiza portfólio para maximizar DY e diversificação.
    
    Args:
        df_stocks: DataFrame com análise de ações
        capital_total: Capital total disponível
        min_dy: DY mínimo para filtro
        
    Returns:
        DataFrame otimizado ou None
    """
    if df_stocks.empty or capital_total <= 0:
        return None
    
    # Filtrar por DY mínimo
    if min_dy is None:
        min_dy = config.MIN_DY_FILTER
    
    df_filtered = df_stocks[df_stocks['dy_12m'] >= min_dy].copy()
    
    if df_filtered.empty:
        logger.warning(f"Nenhum ativo com DY >= {min_dy}%")
        return None
    
    # Selecionar top ativos
    df_sorted = df_filtered.sort_values('score', ascending=False)
    max_assets = min(config.MAX_ASSETS_PORTFOLIO, len(df_sorted))
    df_selected = df_sorted.head(max_assets).copy()
    
    # Distribuir capital proporcionalmente ao score
    df_selected['peso'] = df_selected['score'] / df_selected['score'].sum()
    df_selected['capital_alocado'] = df_selected['peso'] * capital_total
    
    # Calcular quantidades
    def calc_quantidade(row):
        lote = get_lot_size(row['categoria'])
        qtd_ideal = row['capital_alocado'] / row['preco']
        qtd_lotes = (qtd_ideal // lote) * lote
        return int(qtd_lotes) if qtd_lotes > 0 else lote
    
    df_selected['quantidade'] = df_selected.apply(calc_quantidade, axis=1)
    df_selected['valor_investido'] = df_selected['quantidade'] * df_selected['preco']
    
    # Remover ativos sem alocação
    df_selected = df_selected[df_selected['valor_investido'] > 0]
    
    if df_selected.empty:
        return None
    
    # Recalcular percentuais
    total_real = df_selected['valor_investido'].sum()
    df_selected['percentual_carteira'] = (df_selected['valor_investido'] / total_real) * 100
    
    # Estimar dividendos
    df_selected['dividendos_anuais_estimados'] = df_selected['valor_investido'] * (df_selected['dy_12m'] / 100)
    df_selected['dividendos_mensais_estimados'] = df_selected['dividendos_anuais_estimados'] / 12
    
    logger.info(f"Portfólio otimizado: {len(df_selected)} ativos, R$ {total_real:,.2f} investidos")
    
    return df_selected[['ticker', 'nome', 'categoria', 'setor', 'preco', 'quantidade', 
                        'valor_investido', 'percentual_carteira', 'dy_12m', 
                        'dividendos_anuais_estimados', 'dividendos_mensais_estimados', 
                        'score', 'dividends_history']]
