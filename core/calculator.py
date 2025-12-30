"""
Cálculos de métricas de dividendos e análises financeiras.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from concurrent.futures import ProcessPoolExecutor, as_completed
import streamlit as st

from config.settings import config
from core.data_fetcher import data_fetcher
from utils.helpers import categorize_ticker, calculate_score
from utils.validators import validate_dividend_yield, validate_cagr
from utils.logger import setup_logger, log_performance
import time

logger = setup_logger(__name__)


def calculate_dividend_metrics(ticker: str, years: int = 5) -> Optional[Dict[str, Any]]:
    """
    Calcula métricas de dividendos para um ativo.
    
    Args:
        ticker: Ticker do ativo
        years: Anos de histórico
        
    Returns:
        Dicionário com métricas ou None
    """
    try:
        # Buscar informações básicas
        info = data_fetcher.get_stock_info(ticker)
        if not info or info['preco_atual'] == 0:
            return None
        
        # Buscar dividendos
        dividends = data_fetcher.get_dividends_history(ticker, years)
        if dividends.empty:
            return None
        
        preco_atual = info['preco_atual']
        
        # DY dos últimos 12 meses
        end_date = datetime.today()
        start_12m = end_date - timedelta(days=365)
        dividends_index = dividends.index.tz_localize(None) if dividends.index.tz else dividends.index
        dividends_12m = dividends[dividends_index >= pd.to_datetime(start_12m)]
        dy_12m = (dividends_12m.sum() / preco_atual * 100) if not dividends_12m.empty else 0
        
        # Validar DY
        is_valid_dy, msg = validate_dividend_yield(dy_12m, ticker)
        if not is_valid_dy:
            return None
        
        # Dividendos anuais
        dividends_by_year = dividends.groupby(dividends.index.year).sum()
        dy_medio = dividends_by_year.mean() / preco_atual * 100 if preco_atual > 0 else 0
        
        # Consistência
        anos_com_dividendos = len(dividends_by_year)
        consistencia = (anos_com_dividendos / years) * 100
        
        # CAGR
        cagr = 0
        if len(dividends_by_year) >= 2:
            start_val = dividends_by_year.iloc[0]
            end_val = dividends_by_year.iloc[-1]
            num_years = len(dividends_by_year) - 1
            if start_val > 0 and num_years > 0:
                cagr = ((end_val / start_val) ** (1 / num_years) - 1) * 100
        
        # Validar CAGR
        is_valid_cagr, _ = validate_cagr(cagr, ticker)
        if not is_valid_cagr:
            cagr = 0
        
        # Categoria
        categoria = categorize_ticker(ticker)
        
        # Score composto
        score = calculate_score(dy_12m, consistencia, cagr)
        
        return {
            'ticker': ticker,
            'nome': info['nome_longo'],
            'categoria': categoria,
            'setor': info['setor'],
            'preco': preco_atual,
            'dy_12m': round(dy_12m, 2),
            'dy_medio': round(dy_medio, 2),
            'consistencia': round(consistencia, 1),
            'cagr_dividendos': round(cagr, 2),
            'anos_com_div': anos_com_dividendos,
            'score': score,
            'dividends_history': dividends,
            # Fundamentalista
            'pl': info.get('pl_atual', 0),
            'payout': info.get('payout_ratio', 0),
            'market_cap': info.get('market_cap', 0),
            'beta': info.get('beta', 0),
            'roe': info.get('roe', 0),
            'debt_to_equity': info.get('debt_to_equity', 0)
        }
        
    except Exception as e:
        logger.error(f"Erro ao calcular métricas para {ticker}: {str(e)}")
        return None


def analyze_stocks_parallel(tickers: list, progress_callback=None) -> pd.DataFrame:
    """
    Analisa múltiplos tickers em paralelo.
    
    Args:
        tickers: Lista de tickers
        progress_callback: Função de callback para progresso
        
    Returns:
        DataFrame com resultados
    """
    start_time = time.time()
    results = []
    total = len(tickers)
    
    if config.ENABLE_PARALLEL and total > 10:
        # Processamento paralelo
        logger.info(f"Iniciando análise paralela de {total} ativos")
        
        with ProcessPoolExecutor(max_workers=config.MAX_WORKERS) as executor:
            future_to_ticker = {
                executor.submit(calculate_dividend_metrics, ticker): ticker 
                for ticker in tickers
            }
            
            for idx, future in enumerate(as_completed(future_to_ticker)):
                if progress_callback:
                    progress_callback((idx + 1) / total, f"Analisando... {idx+1}/{total}")
                
                try:
                    result = future.result(timeout=30)
                    if result:
                        results.append(result)
                except Exception as e:
                    ticker = future_to_ticker[future]
                    logger.error(f"Erro ao processar {ticker}: {str(e)}")
    else:
        # Processamento sequencial
        logger.info(f"Iniciando análise sequencial de {total} ativos")
        for idx, ticker in enumerate(tickers):
            if progress_callback:
                progress_callback((idx + 1) / total, f"Analisando {ticker}...")
            
            result = calculate_dividend_metrics(ticker)
            if result:
                results.append(result)
    
    duration = time.time() - start_time
    log_performance(logger, f"Análise de {len(results)} ativos", duration)
    
    return pd.DataFrame(results)


def calculate_portfolio_metrics(portfolio_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcula métricas agregadas do portfólio.
    
    Args:
        portfolio_df: DataFrame do portfólio
        
    Returns:
        Dicionário com métricas
    """
    if portfolio_df is None or portfolio_df.empty:
        return {}
    
    total_investido = portfolio_df['valor_investido'].sum()
    total_anual = portfolio_df['dividendos_anuais_estimados'].sum()
    dy_medio = (total_anual / total_investido * 100) if total_investido > 0 else 0
    
    return {
        'num_ativos': len(portfolio_df),
        'valor_total': total_investido,
        'dy_medio': dy_medio,
        'dividendos_anuais': total_anual,
        'dividendos_mensais': total_anual / 12,
        'categorias': portfolio_df['categoria'].value_counts().to_dict(),
        'setores': portfolio_df['setor'].value_counts().to_dict()
    }


def calculate_historical_return(ticker: str, years: int = 1) -> float:
    """
    Calcula retorno histórico do preço.
    
    Args:
        ticker: Ticker do ativo
        years: Anos atrás
        
    Returns:
        Retorno percentual
    """
    try:
        history = data_fetcher.get_price_history(ticker, period=f"{years}y")
        if history.empty or len(history) < 2:
            return 0
        
        start_price = history['Close'].iloc[0]
        end_price = history['Close'].iloc[-1]
        
        if start_price > 0:
            return ((end_price - start_price) / start_price) * 100
        return 0
    except:
        return 0
