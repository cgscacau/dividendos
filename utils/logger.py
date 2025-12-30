"""
Sistema de logging centralizado para o aplicativo.
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from config.settings import config


def setup_logger(name: str = None, log_to_file: bool = True) -> logging.Logger:
    """
    Configura e retorna um logger.
    
    Args:
        name: Nome do logger (usa __name__ se None)
        log_to_file: Se deve gravar logs em arquivo
        
    Returns:
        Logger configurado
    """
    # Usar nome root se não especificado
    logger_name = name if name else 'dividendos_app'
    logger = logging.getLogger(logger_name)
    
    # Se já foi configurado, retornar
    if logger.handlers:
        return logger
    
    # Configurar nível
    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Formato
    formatter = logging.Formatter(
        fmt=config.LOG_FORMAT,
        datefmt=config.LOG_DATE_FORMAT
    )
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para arquivo (se habilitado)
    if log_to_file:
        # Criar diretório de logs se não existir
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)
        
        # Nome do arquivo com data
        log_filename = os.path.join(
            log_dir,
            f'dividendos_b3_{datetime.now().strftime("%Y%m%d")}.log'
        )
        
        # Handler rotativo
        file_handler = RotatingFileHandler(
            log_filename,
            maxBytes=config.LOG_FILE_MAX_BYTES,
            backupCount=config.LOG_FILE_BACKUP_COUNT,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Evitar propagação para o root logger
    logger.propagate = False
    
    return logger


def log_performance(logger: logging.Logger, operation: str, duration: float):
    """
    Loga informação de performance.
    
    Args:
        logger: Logger a usar
        operation: Nome da operação
        duration: Duração em segundos
    """
    if duration < 1:
        logger.info(f"⚡ {operation} completado em {duration*1000:.0f}ms")
    elif duration < 60:
        logger.info(f"✅ {operation} completado em {duration:.2f}s")
    else:
        minutes = int(duration // 60)
        seconds = duration % 60
        logger.info(f"✅ {operation} completado em {minutes}min {seconds:.0f}s")


def log_error_with_context(logger: logging.Logger, error: Exception, context: dict = None):
    """
    Loga erro com contexto adicional.
    
    Args:
        logger: Logger a usar
        error: Exceção capturada
        context: Dicionário com contexto adicional
    """
    error_msg = f"❌ Erro: {str(error)}"
    
    if context:
        context_str = ", ".join([f"{k}={v}" for k, v in context.items()])
        error_msg += f" | Contexto: {context_str}"
    
    logger.error(error_msg, exc_info=True)


def log_data_quality_issue(logger: logging.Logger, ticker: str, issue: str, severity: str = 'warning'):
    """
    Loga problema de qualidade de dados.
    
    Args:
        logger: Logger a usar
        ticker: Ticker do ativo
        issue: Descrição do problema
        severity: Severidade (warning, error, info)
    """
    msg = f"📊 Qualidade de dados - {ticker}: {issue}"
    
    if severity == 'error':
        logger.error(msg)
    elif severity == 'warning':
        logger.warning(msg)
    else:
        logger.info(msg)


def log_cache_hit(logger: logging.Logger, key: str):
    """
    Loga cache hit.
    
    Args:
        logger: Logger a usar
        key: Chave do cache
    """
    logger.debug(f"💾 Cache HIT: {key}")


def log_cache_miss(logger: logging.Logger, key: str):
    """
    Loga cache miss.
    
    Args:
        logger: Logger a usar
        key: Chave do cache
    """
    logger.debug(f"❌ Cache MISS: {key}")


def log_api_request(logger: logging.Logger, ticker: str, success: bool, duration: float = None):
    """
    Loga requisição à API.
    
    Args:
        logger: Logger a usar
        ticker: Ticker consultado
        success: Se a requisição foi bem-sucedida
        duration: Duração da requisição em segundos
    """
    status = "✅" if success else "❌"
    msg = f"{status} API Request: {ticker}"
    
    if duration is not None:
        msg += f" ({duration*1000:.0f}ms)"
    
    if success:
        logger.debug(msg)
    else:
        logger.warning(msg)


# Logger global da aplicação
app_logger = setup_logger('dividendos_app')
