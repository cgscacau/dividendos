"""
Módulo para busca de dados financeiros do yfinance com cache e rate limiting.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
from typing import Optional, Dict, Any
import time

from config.settings import config
from utils.helpers import rate_limit, retry, timer
from utils.validators import (
    validate_ticker, validate_price, validate_dividends_data
)
from utils.logger import setup_logger, log_api_request, log_data_quality_issue

logger = setup_logger(__name__)


class DataFetcher:
    """Classe para buscar dados financeiros com cache e validação."""
    
    def __init__(self):
        self.cache_enabled = True
    
    @st.cache_resource(ttl=config.CACHE_TTL_LONG)
    def _get_stock_object(ticker: str) -> Optional[yf.Ticker]:
        """
        Retorna objeto Ticker do yfinance (cached).
        
        Args:
            ticker: Ticker do ativo
            
        Returns:
            Objeto Ticker ou None
        """
        try:
            stock = yf.Ticker(ticker)
            # Validar se tem dados
            if hasattr(stock, 'info') and stock.info:
                return stock
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar ticker {ticker}: {str(e)}")
            return None
    
    @rate_limit(max_per_second=5)
    @retry(max_attempts=3, delay=1.0, exceptions=(Exception,))
    def get_stock_object(self, ticker: str) -> Optional[yf.Ticker]:
        """
        Busca objeto Ticker com rate limiting e retry.
        
        Args:
            ticker: Ticker do ativo
            
        Returns:
            Objeto Ticker ou None
        """
        start_time = time.time()
        
        # Validar ticker
        if not validate_ticker(ticker):
            log_api_request(logger, ticker, success=False)
            return None
        
        try:
            stock = self._get_stock_object(ticker)
            duration = time.time() - start_time
            
            if stock:
                log_api_request(logger, ticker, success=True, duration=duration)
            else:
                log_api_request(logger, ticker, success=False, duration=duration)
            
            return stock
        except Exception as e:
            logger.error(f"Erro ao buscar {ticker}: {str(e)}")
            log_api_request(logger, ticker, success=False)
            return None
    
    @st.cache_data(ttl=config.CACHE_TTL_SHORT)
    def get_stock_info(_self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Busca informações gerais do ativo (cached).
        
        Args:
            ticker: Ticker do ativo
            
        Returns:
            Dicionário com informações ou None
        """
        stock = _self.get_stock_object(ticker)
        if not stock:
            return None
        
        try:
            info = stock.info
            if not info:
                return None
            
            # Extrair preço
            preco_atual = info.get('regularMarketPrice') or \
                         info.get('currentPrice') or \
                         info.get('previousClose', 0)
            
            # Validar preço
            is_valid, msg = validate_price(preco_atual, ticker)
            if not is_valid:
                log_data_quality_issue(logger, ticker, msg, 'warning')
                return None
            
            data = {
                "ticker": ticker,
                "nome_longo": info.get('longName') or info.get('shortName', ticker),
                "setor": info.get('sector', 'N/A'),
                "preco_atual": preco_atual,
                "pl_atual": info.get('trailingPE', 0),
                "payout_ratio": info.get('payoutRatio', 0) * 100 if info.get('payoutRatio') else 0,
                "market_cap": info.get('marketCap', 0),
                "beta": info.get('beta', 0),
                "roe": info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0,
                "debt_to_equity": info.get('debtToEquity', 0),
                "profit_margin": info.get('profitMargins', 0) * 100 if info.get('profitMargins') else 0,
                "price_to_book": info.get('priceToBook', 0)
            }
            
            return data
            
        except Exception as e:
            logger.error(f"Erro ao buscar info de {ticker}: {str(e)}")
            return None
    
    @st.cache_data(ttl=config.CACHE_TTL_SHORT)
    def get_dividends_history(_self, ticker: str, years: int = 5) -> pd.Series:
        """
        Busca histórico de dividendos (cached).
        
        Args:
            ticker: Ticker do ativo
            years: Anos de histórico
            
        Returns:
            Série com dividendos ou Series vazio
        """
        stock = _self.get_stock_object(ticker)
        if not stock:
            return pd.Series(dtype=float)
        
        try:
            end_date = datetime.today()
            start_date = end_date - timedelta(days=years * 365 + 100)
            
            dividends = stock.dividends
            
            if dividends.empty:
                log_data_quality_issue(logger, ticker, "Sem histórico de dividendos", 'info')
                return pd.Series(dtype=float)
            
            # Filtrar período
            dividends_index = dividends.index.tz_localize(None) if dividends.index.tz else dividends.index
            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date)
            
            dividends_filtered = dividends[
                (dividends_index >= start_dt) & (dividends_index <= end_dt)
            ]
            
            # Validar dados
            is_valid, msg = validate_dividends_data(dividends_filtered)
            if not is_valid:
                log_data_quality_issue(logger, ticker, msg, 'warning')
                return pd.Series(dtype=float)
            
            return dividends_filtered
            
        except Exception as e:
            logger.error(f"Erro ao buscar dividendos de {ticker}: {str(e)}")
            return pd.Series(dtype=float)
    
    @st.cache_data(ttl=config.CACHE_TTL_SHORT)
    def get_price_history(_self, ticker: str, period: str = "1y") -> pd.DataFrame:
        """
        Busca histórico de preços (cached).
        
        Args:
            ticker: Ticker do ativo
            period: Período (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            
        Returns:
            DataFrame com histórico ou DataFrame vazio
        """
        stock = _self.get_stock_object(ticker)
        if not stock:
            return pd.DataFrame()
        
        try:
            history = stock.history(period=period)
            
            if history.empty:
                log_data_quality_issue(logger, ticker, "Sem histórico de preços", 'warning')
                return pd.DataFrame()
            
            return history
            
        except Exception as e:
            logger.error(f"Erro ao buscar histórico de {ticker}: {str(e)}")
            return pd.DataFrame()
    
    def get_current_price(self, ticker: str) -> float:
        """
        Busca preço atual do ativo.
        
        Args:
            ticker: Ticker do ativo
            
        Returns:
            Preço atual ou 0
        """
        info = self.get_stock_info(ticker)
        if info:
            return info.get('preco_atual', 0)
        return 0
    
    def check_liquidity(self, ticker: str) -> bool:
        """
        Verifica se o ativo tem liquidez adequada.
        
        Args:
            ticker: Ticker do ativo
            
        Returns:
            True se tem liquidez, False caso contrário
        """
        try:
            # Buscar histórico recente
            history = self.get_price_history(ticker, period="60d")
            
            if history.empty:
                return False
            
            # Verificar se tem negociação nos últimos 60 dias
            days_with_trades = len(history)
            if days_with_trades < config.MIN_DAYS_TRADING:
                log_data_quality_issue(
                    logger, ticker,
                    f"Poucos dias de negociação: {days_with_trades}",
                    'info'
                )
                return False
            
            # Verificar volume médio
            avg_volume = history['Volume'].mean()
            if avg_volume < config.MIN_VOLUME:
                log_data_quality_issue(
                    logger, ticker,
                    f"Volume baixo: {avg_volume:.0f}",
                    'info'
                )
                return False
            
            return True
            
        except Exception as e:
            logger.warning(f"Erro ao verificar liquidez de {ticker}: {str(e)}")
            return False
    
    @st.cache_data(ttl=config.CACHE_TTL_LONG)
    def get_benchmark_data(_self, ticker: str, years: int = 1) -> Optional[pd.DataFrame]:
        """
        Busca dados de benchmark (cached por longo tempo).
        
        Args:
            ticker: Ticker do benchmark
            years: Anos de histórico
            
        Returns:
            DataFrame com dados ou None
        """
        try:
            benchmark = yf.Ticker(ticker)
            history = benchmark.history(period=f"{years}y")
            
            if history.empty:
                logger.warning(f"Benchmark {ticker} sem dados")
                return None
            
            return history
            
        except Exception as e:
            logger.error(f"Erro ao buscar benchmark {ticker}: {str(e)}")
            return None


# Instância global
data_fetcher = DataFetcher()
