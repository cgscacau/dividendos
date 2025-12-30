"""
Configurações centralizadas do aplicativo de análise de dividendos.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class AppConfig:
    """Configurações principais do aplicativo."""
    
    # ===== CACHE =====
    CACHE_TTL_SHORT: int = 1800  # 30 minutos
    CACHE_TTL_LONG: int = 86400  # 24 horas (1 dia)
    
    # ===== ANÁLISE =====
    MAX_TICKERS_ANALYSIS: int = 200  # Máximo de tickers para análise simultânea
    DEFAULT_YEARS_HISTORY: int = 5  # Anos de histórico padrão
    MAX_DY_THRESHOLD: float = 40.0  # DY máximo aceitável (outliers)
    MIN_DY_THRESHOLD: float = 0.1  # DY mínimo para considerar
    MIN_PRICE: float = 0.01  # Preço mínimo válido
    
    # ===== OTIMIZAÇÃO DE PORTFÓLIO =====
    MAX_ASSETS_PORTFOLIO: int = 15  # Número máximo de ativos no portfólio
    DEFAULT_LOT_SIZE_ACOES: int = 100  # Lote padrão para ações
    DEFAULT_LOT_SIZE_OUTROS: int = 1  # Lote padrão para FIIs, BDRs, ETFs
    MIN_DY_FILTER: float = 4.0  # DY mínimo padrão para filtro
    
    # ===== SCORE WEIGHTS (Pesos do Score Composto) =====
    SCORE_WEIGHTS: Dict[str, float] = field(default_factory=lambda: {
        'dy': 0.4,  # 40% - Dividend Yield
        'consistencia': 0.3,  # 30% - Consistência de pagamento
        'cagr': 0.3  # 30% - Crescimento dos dividendos
    })
    
    # ===== CATEGORIAS =====
    CATEGORIES: List[str] = field(default_factory=lambda: ['Ação', 'FII', 'BDR', 'ETF'])
    
    # Cores por categoria (para gráficos)
    CATEGORY_COLORS: Dict[str, str] = field(default_factory=lambda: {
        'Ação': '#1f77b4',  # Azul
        'FII': '#ff7f0e',  # Laranja
        'BDR': '#2ca02c',  # Verde
        'ETF': '#d62728'  # Vermelho
    })
    
    # ===== PARALELIZAÇÃO =====
    MAX_WORKERS: int = 10  # Número máximo de processos paralelos
    ENABLE_PARALLEL: bool = True  # Ativar/desativar processamento paralelo
    
    # ===== RATE LIMITING =====
    MAX_REQUESTS_PER_SECOND: int = 5  # Limite de requisições por segundo
    REQUEST_TIMEOUT: int = 10  # Timeout para requisições em segundos
    MAX_RETRIES: int = 3  # Número máximo de tentativas em caso de erro
    RETRY_DELAY: float = 1.0  # Delay entre tentativas (segundos)
    
    # ===== VALIDAÇÃO DE LIQUIDEZ =====
    MIN_DAYS_TRADING: int = 60  # Dias mínimos de negociação
    MIN_VOLUME: float = 1000.0  # Volume mínimo médio diário
    
    # ===== LOGGING =====
    LOG_LEVEL: str = 'INFO'  # Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_DATE_FORMAT: str = '%Y-%m-%d %H:%M:%S'
    LOG_FILE_MAX_BYTES: int = 10485760  # 10MB
    LOG_FILE_BACKUP_COUNT: int = 5
    
    # ===== BENCHMARK TICKERS =====
    BENCHMARKS: Dict[str, str] = field(default_factory=lambda: {
        'Ibovespa': '^BVSP',
        'IFIX': 'IFIX.SA',
        'S&P 500': '^GSPC',
        'Small Caps': 'SMAL11.SA',
        'Dividendos': 'DIVO11.SA'
    })
    
    # ===== UI/UX =====
    PAGE_TITLE: str = '🎯 Otimizador de Carteira de Dividendos'
    PAGE_ICON: str = '💰'
    LAYOUT: str = 'wide'
    
    # ===== EXPORTAÇÃO =====
    EXPORT_FORMATS: List[str] = field(default_factory=lambda: ['CSV', 'Excel', 'JSON'])
    EXCEL_SHEET_NAME: str = 'Portfolio'
    
    # ===== SIMULAÇÃO =====
    MAX_SIMULATION_YEARS: int = 10
    MIN_SIMULATION_YEARS: int = 1
    
    # ===== ALERTAS =====
    ALERT_DY_DROP_THRESHOLD: float = 0.7  # 30% de queda no DY
    ALERT_PRICE_DROP_THRESHOLD: float = -15.0  # 15% de queda no preço
    ALERT_DIVIDEND_DAYS_AHEAD: int = 7  # Alertar dividendos X dias antes


# Instância global de configuração
config = AppConfig()


# ===== FUNÇÕES AUXILIARES =====

def get_lot_size(categoria: str) -> int:
    """Retorna o tamanho do lote baseado na categoria."""
    if categoria == 'Ação':
        return config.DEFAULT_LOT_SIZE_ACOES
    return config.DEFAULT_LOT_SIZE_OUTROS


def get_category_color(categoria: str) -> str:
    """Retorna a cor da categoria."""
    return config.CATEGORY_COLORS.get(categoria, '#808080')


def is_valid_dy(dy: float) -> bool:
    """Valida se o DY está dentro dos limites aceitáveis."""
    return config.MIN_DY_THRESHOLD <= dy <= config.MAX_DY_THRESHOLD


def is_valid_price(price: float) -> bool:
    """Valida se o preço é válido."""
    return price >= config.MIN_PRICE


# ===== CONSTANTES =====

# ETFs conhecidos (terminam em 11 mas não são FIIs)
KNOWN_ETFS = [
    "BOVA11", "SMAL11", "IVVB11", "SPXI11", "MATB11", "PIBB11",
    "ISUS11", "FIND11", "DIVO11", "BOVX11", "GOVE11", "BRAX11",
    "XBOV11", "BOVV11", "WRLD11", "ACWI11", "DEFI11", "HASH11"
]

# Setores importantes
IMPORTANT_SECTORS = [
    'Financeiro', 'Energia', 'Utilities', 'Consumo', 'Imobiliário',
    'Mineração', 'Petróleo', 'Telecomunicações', 'Saúde', 'Varejo'
]
