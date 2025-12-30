"""
Funções auxiliares e decoradores.
"""

import time
import functools
from typing import Callable, Any
from config.settings import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


def rate_limit(max_per_second: int = None):
    """
    Decorator para limitar taxa de requisições.
    
    Args:
        max_per_second: Requisições máximas por segundo (usa config se None)
        
    Usage:
        @rate_limit(max_per_second=5)
        def my_function():
            pass
    """
    if max_per_second is None:
        max_per_second = config.MAX_REQUESTS_PER_SECOND
    
    min_interval = 1.0 / max_per_second if max_per_second > 0 else 0
    last_called = [0.0]
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if min_interval > 0:
                elapsed = time.time() - last_called[0]
                wait_time = min_interval - elapsed
                if wait_time > 0:
                    time.sleep(wait_time)
            
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator


def retry(max_attempts: int = None, delay: float = None, exceptions: tuple = (Exception,)):
    """
    Decorator para retry automático em caso de erro.
    
    Args:
        max_attempts: Tentativas máximas (usa config se None)
        delay: Delay entre tentativas em segundos (usa config se None)
        exceptions: Tupla de exceções para capturar
        
    Usage:
        @retry(max_attempts=3, delay=1.0)
        def my_function():
            pass
    """
    if max_attempts is None:
        max_attempts = config.MAX_RETRIES
    if delay is None:
        delay = config.RETRY_DELAY
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt < max_attempts:
                        logger.warning(
                            f"Tentativa {attempt}/{max_attempts} falhou para {func.__name__}: {str(e)}"
                        )
                        time.sleep(delay)
                    else:
                        logger.error(
                            f"Todas as {max_attempts} tentativas falharam para {func.__name__}"
                        )
            
            # Se chegou aqui, todas as tentativas falharam
            raise last_exception
        return wrapper
    return decorator


def timer(func: Callable) -> Callable:
    """
    Decorator para medir tempo de execução.
    
    Usage:
        @timer
        def my_function():
            pass
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        
        logger.info(f"⏱️  {func.__name__} executado em {duration:.2f}s")
        return result
    return wrapper


def categorize_ticker(ticker: str) -> str:
    """
    Categoriza o ticker em: Ação, FII, BDR ou ETF.
    
    Args:
        ticker: Ticker a categorizar (ex: 'ITUB4.SA')
        
    Returns:
        Categoria ('Ação', 'FII', 'BDR', 'ETF')
    """
    from config.settings import KNOWN_ETFS
    
    ticker_clean = ticker.replace(".SA", "").upper()
    
    # ETFs específicos conhecidos
    if ticker_clean in KNOWN_ETFS:
        return "ETF"
    
    # FIIs terminam em 11 (mas não são ETFs)
    if ticker_clean.endswith("11"):
        return "FII"
    
    # BDRs terminam em 34 ou 35
    if ticker_clean.endswith("34") or ticker_clean.endswith("35"):
        return "BDR"
    
    # Default: Ação
    return "Ação"


def calculate_score(dy: float, consistency: float, cagr: float) -> float:
    """
    Calcula score composto baseado nas métricas.
    
    Args:
        dy: Dividend Yield (%)
        consistency: Consistência de pagamento (%)
        cagr: Taxa de crescimento composta (%)
        
    Returns:
        Score calculado
    """
    weights = config.SCORE_WEIGHTS
    
    # Limitar CAGR para evitar outliers
    cagr_limited = max(0, min(cagr, 20))
    
    score = (dy * weights['dy']) + \
            (consistency * weights['consistencia']) + \
            (cagr_limited * weights['cagr'])
    
    return round(score, 2)


def chunk_list(lst: list, chunk_size: int) -> list:
    """
    Divide lista em chunks menores.
    
    Args:
        lst: Lista a dividir
        chunk_size: Tamanho de cada chunk
        
    Returns:
        Lista de chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def safe_division(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Divisão segura que retorna default se denominador for zero.
    
    Args:
        numerator: Numerador
        denominator: Denominador
        default: Valor padrão se denominador for zero
        
    Returns:
        Resultado da divisão ou default
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except:
        return default


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Limita valor entre min e max.
    
    Args:
        value: Valor a limitar
        min_value: Valor mínimo
        max_value: Valor máximo
        
    Returns:
        Valor limitado
    """
    return max(min_value, min(value, max_value))


def percentage_change(old_value: float, new_value: float) -> float:
    """
    Calcula variação percentual.
    
    Args:
        old_value: Valor antigo
        new_value: Valor novo
        
    Returns:
        Variação percentual
    """
    if old_value == 0:
        return 0.0
    return ((new_value - old_value) / old_value) * 100


def is_recent_trading(last_trade_date: Any, days_threshold: int = None) -> bool:
    """
    Verifica se o ativo tem negociação recente.
    
    Args:
        last_trade_date: Data da última negociação
        days_threshold: Threshold em dias (usa config se None)
        
    Returns:
        True se tem negociação recente
    """
    if days_threshold is None:
        days_threshold = config.MIN_DAYS_TRADING
    
    from datetime import datetime, timedelta
    import pandas as pd
    
    if last_trade_date is None:
        return False
    
    # Converter para datetime se necessário
    if isinstance(last_trade_date, pd.Timestamp):
        last_trade_date = last_trade_date.to_pydatetime()
    elif isinstance(last_trade_date, str):
        last_trade_date = pd.to_datetime(last_trade_date)
    
    threshold_date = datetime.now() - timedelta(days=days_threshold)
    return last_trade_date >= threshold_date


def get_ticker_list_by_categories(categories: list) -> list:
    """
    Retorna lista de tickers filtrada por categorias.
    
    Args:
        categories: Lista de categorias ('Ação', 'FII', 'BDR', 'ETF')
        
    Returns:
        Lista de tickers
    """
    from config.constants import get_acoes_b3_completas, get_fiis_completos
    
    all_tickers = []
    
    # Ações
    if 'Ação' in categories:
        all_tickers.extend(get_acoes_b3_completas())
    
    # FIIs
    if 'FII' in categories:
        all_tickers.extend(get_fiis_completos())
    
    # BDRs
    if 'BDR' in categories:
        bdrs = [
            "AAPL34.SA", "MSFT34.SA", "AMZO34.SA", "GOGL34.SA", "META34.SA",
            "TSLA34.SA", "NVDC34.SA", "NFLX34.SA", "DIS34.SA", "COCA34.SA",
            "PETR34.SA", "JPMC34.SA", "V1SA34.SA", "MAST34.SA", "PYPL34.SA",
            "NIKE34.SA", "STBUCKS34.SA", "UBER34.SA", "AIRB34.SA", "SPOT34.SA"
        ]
        all_tickers.extend(bdrs)
    
    # ETFs
    if 'ETF' in categories:
        etfs = [
            "BOVA11.SA", "SMAL11.SA", "IVVB11.SA", "SPXI11.SA", "MATB11.SA",
            "PIBB11.SA", "ISUS11.SA", "FIND11.SA", "DIVO11.SA", "BOVX11.SA",
            "GOVE11.SA", "BRAX11.SA", "XBOV11.SA", "BOVV11.SA"
        ]
        all_tickers.extend(etfs)
    
    # Remover duplicatas e retornar
    return list(set(all_tickers))


def format_time_elapsed(seconds: float) -> str:
    """
    Formata tempo decorrido em formato legível.
    
    Args:
        seconds: Segundos
        
    Returns:
        String formatada (ex: "2min 30s")
    """
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    else:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}min {secs}s"
