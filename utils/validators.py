"""
Validadores para dados financeiros e inputs do usuário.
"""

import pandas as pd
from datetime import datetime, timedelta
from config.settings import config
import logging

logger = logging.getLogger(__name__)


def validate_ticker(ticker: str) -> bool:
    """
    Valida formato do ticker.
    
    Args:
        ticker: Ticker a validar (ex: 'ITUB4.SA')
        
    Returns:
        True se válido, False caso contrário
    """
    if not ticker or not isinstance(ticker, str):
        return False
    
    # Ticker deve terminar com .SA para B3
    if not ticker.endswith('.SA'):
        logger.warning(f"Ticker inválido (não termina com .SA): {ticker}")
        return False
    
    # Remover .SA e validar
    ticker_clean = ticker.replace('.SA', '')
    
    # Deve ter pelo menos 4 caracteres
    if len(ticker_clean) < 4:
        logger.warning(f"Ticker muito curto: {ticker}")
        return False
    
    return True


def validate_dividend_yield(dy: float, ticker: str = None) -> tuple[bool, str]:
    """
    Valida Dividend Yield.
    
    Args:
        dy: Dividend Yield (%)
        ticker: Ticker para logging (opcional)
        
    Returns:
        Tupla (válido: bool, mensagem: str)
    """
    ticker_info = f" ({ticker})" if ticker else ""
    
    # DY negativo
    if dy < 0:
        msg = f"DY negativo{ticker_info}: {dy:.2f}%"
        logger.warning(msg)
        return False, msg
    
    # DY muito baixo
    if dy < config.MIN_DY_THRESHOLD:
        msg = f"DY muito baixo{ticker_info}: {dy:.2f}%"
        logger.info(msg)
        return False, msg
    
    # DY muito alto (possível outlier)
    if dy > config.MAX_DY_THRESHOLD:
        msg = f"DY muito alto (possível outlier){ticker_info}: {dy:.2f}%"
        logger.warning(msg)
        return False, msg
    
    return True, "DY válido"


def validate_price(price: float, ticker: str = None) -> tuple[bool, str]:
    """
    Valida preço do ativo.
    
    Args:
        price: Preço do ativo
        ticker: Ticker para logging (opcional)
        
    Returns:
        Tupla (válido: bool, mensagem: str)
    """
    ticker_info = f" ({ticker})" if ticker else ""
    
    # Preço negativo ou zero
    if price <= 0:
        msg = f"Preço inválido{ticker_info}: R$ {price:.2f}"
        logger.warning(msg)
        return False, msg
    
    # Preço muito baixo (possível erro)
    if price < config.MIN_PRICE:
        msg = f"Preço muito baixo{ticker_info}: R$ {price:.2f}"
        logger.warning(msg)
        return False, msg
    
    return True, "Preço válido"


def validate_portfolio_capital(capital: float) -> tuple[bool, str]:
    """
    Valida capital para montagem de portfólio.
    
    Args:
        capital: Capital total disponível
        
    Returns:
        Tupla (válido: bool, mensagem: str)
    """
    if capital <= 0:
        return False, "Capital deve ser maior que zero"
    
    if capital < 1000:
        return False, "Capital mínimo recomendado: R$ 1.000"
    
    if capital > 100_000_000:
        return False, "Capital muito alto (acima de R$ 100 milhões)"
    
    return True, "Capital válido"


def validate_date_range(start_date: datetime, end_date: datetime) -> tuple[bool, str]:
    """
    Valida intervalo de datas.
    
    Args:
        start_date: Data inicial
        end_date: Data final
        
    Returns:
        Tupla (válido: bool, mensagem: str)
    """
    if start_date >= end_date:
        return False, "Data inicial deve ser anterior à data final"
    
    # Verificar se o período não é muito longo
    max_days = config.MAX_SIMULATION_YEARS * 365
    if (end_date - start_date).days > max_days:
        return False, f"Período muito longo (máximo {config.MAX_SIMULATION_YEARS} anos)"
    
    # Verificar se o período não é muito curto
    min_days = config.MIN_SIMULATION_YEARS * 365
    if (end_date - start_date).days < min_days:
        return False, f"Período muito curto (mínimo {config.MIN_SIMULATION_YEARS} ano)"
    
    return True, "Período válido"


def validate_dividends_data(dividends: pd.Series) -> tuple[bool, str]:
    """
    Valida dados de dividendos.
    
    Args:
        dividends: Série de dividendos do yfinance
        
    Returns:
        Tupla (válido: bool, mensagem: str)
    """
    if dividends is None:
        return False, "Dados de dividendos não fornecidos"
    
    if not isinstance(dividends, pd.Series):
        return False, "Formato de dados inválido"
    
    if dividends.empty:
        return False, "Sem histórico de dividendos"
    
    # Verificar se tem dividendos recentes (último ano)
    if len(dividends) > 0:
        last_dividend_date = dividends.index[-1]
        if isinstance(last_dividend_date, pd.Timestamp):
            last_dividend_date = last_dividend_date.to_pydatetime()
        
        one_year_ago = datetime.now() - timedelta(days=365)
        if last_dividend_date < one_year_ago:
            return False, "Último dividendo muito antigo (mais de 1 ano)"
    
    return True, "Dados de dividendos válidos"


def validate_stock_info(info: dict) -> tuple[bool, str]:
    """
    Valida informações básicas da ação.
    
    Args:
        info: Dicionário com informações da ação
        
    Returns:
        Tupla (válido: bool, mensagem: str)
    """
    if not info:
        return False, "Informações da ação não disponíveis"
    
    # Verificar campos essenciais
    required_fields = ['ticker', 'preco_atual']
    missing_fields = [field for field in required_fields if field not in info]
    
    if missing_fields:
        return False, f"Campos obrigatórios ausentes: {', '.join(missing_fields)}"
    
    # Validar preço
    is_valid, msg = validate_price(info['preco_atual'], info.get('ticker'))
    if not is_valid:
        return False, msg
    
    return True, "Informações válidas"


def validate_score(score: float) -> tuple[bool, str]:
    """
    Valida score calculado.
    
    Args:
        score: Score calculado
        
    Returns:
        Tupla (válido: bool, mensagem: str)
    """
    if score < 0:
        return False, "Score não pode ser negativo"
    
    # Score muito alto indica possível erro de cálculo
    if score > 100:
        return False, f"Score muito alto (possível erro): {score:.2f}"
    
    return True, "Score válido"


def validate_consistency(consistency: float) -> tuple[bool, str]:
    """
    Valida consistência de pagamento.
    
    Args:
        consistency: Consistência (%)
        
    Returns:
        Tupla (válido: bool, mensagem: str)
    """
    if not 0 <= consistency <= 100:
        return False, f"Consistência fora do intervalo 0-100: {consistency:.1f}%"
    
    return True, "Consistência válida"


def validate_cagr(cagr: float, ticker: str = None) -> tuple[bool, str]:
    """
    Valida CAGR (taxa de crescimento).
    
    Args:
        cagr: CAGR (%)
        ticker: Ticker para logging (opcional)
        
    Returns:
        Tupla (válido: bool, mensagem: str)
    """
    ticker_info = f" ({ticker})" if ticker else ""
    
    # CAGR muito negativo indica problemas
    if cagr < -50:
        msg = f"CAGR muito negativo{ticker_info}: {cagr:.2f}%"
        logger.warning(msg)
        return False, msg
    
    # CAGR muito positivo pode ser outlier
    if cagr > 100:
        msg = f"CAGR muito alto (possível outlier){ticker_info}: {cagr:.2f}%"
        logger.warning(msg)
        return False, msg
    
    return True, "CAGR válido"


def sanitize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sanitiza DataFrame removendo valores inválidos.
    
    Args:
        df: DataFrame a sanitizar
        
    Returns:
        DataFrame sanitizado
    """
    if df is None or df.empty:
        return df
    
    # Remover linhas com valores infinitos
    df = df.replace([float('inf'), float('-inf')], pd.NA)
    
    # Remover linhas com valores NaN em colunas críticas
    critical_columns = ['ticker', 'preco', 'dy_12m']
    existing_critical = [col for col in critical_columns if col in df.columns]
    if existing_critical:
        df = df.dropna(subset=existing_critical)
    
    return df
