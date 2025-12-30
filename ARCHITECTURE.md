# 🏗️ Arquitetura do Projeto - Otimizador de Dividendos

## 📁 Estrutura de Diretórios

```
webapp/
├── app.py                          # [TODO] Nova versão refatorada do aplicativo
├── analise_dividendos_app.py       # Versão atual em produção
├── analise_dividendos_app_old.py   # Backup
├── analise_dividendos_otimizado.py # Versão anterior otimizada
├── acoes_b3_completa.py            # [DEPRECATED] Movido para config/constants.py
│
├── config/                         # ✅ Configurações
│   ├── __init__.py
│   ├── settings.py                 # Configurações centralizadas
│   └── constants.py                # Listas de tickers (ações, FIIs, BDRs, ETFs)
│
├── core/                           # ✅ Lógica de negócio
│   ├── __init__.py
│   ├── data_fetcher.py             # Busca de dados (yfinance) com cache/retry/rate-limit
│   ├── calculator.py               # Cálculo de métricas (DY, CAGR, Score, etc.)
│   └── optimizer.py                # Otimização de portfólio
│
├── utils/                          # ✅ Utilitários
│   ├── __init__.py
│   ├── validators.py               # Validação de dados (DY, preço, consistência)
│   ├── formatters.py               # Formatação (moeda, %, números, datas)
│   ├── helpers.py                  # Helpers (rate_limit, retry, categorize, etc.)
│   └── logger.py                   # Sistema de logging
│
├── ui/                             # [TODO] Componentes de UI
│   ├── __init__.py
│   ├── components.py               # Componentes reutilizáveis
│   ├── charts.py                   # Gráficos Plotly
│   └── tables.py                   # Tabelas formatadas
│
├── tests/                          # [TODO] Testes automatizados
│   ├── __init__.py
│   ├── test_calculator.py
│   ├── test_optimizer.py
│   └── test_validators.py
│
├── logs/                           # Logs da aplicação (gerados automaticamente)
│
├── requirements.txt                # Dependências Python
├── README.md                       # Documentação principal
├── README_MELHORIAS.md             # Documentação de melhorias
└── ARCHITECTURE.md                 # Este arquivo
```

## 🎯 Melhorias Implementadas

### ✅ Sprint 1 - Críticas (COMPLETADO)

1. **Análise Paralela** (`core/calculator.py`)
   - Implementado `ProcessPoolExecutor` para análise de múltiplos ativos
   - Suporta até 10 workers paralelos
   - Fallback para processamento sequencial em lotes pequenos

2. **Validação de DY Máximo** (`utils/validators.py`)
   - Validação de DY entre 0.1% e 40%
   - Detecção de outliers (DY > 40%)
   - Validação de preços, consistência e CAGR

3. **Sistema de Logging** (`utils/logger.py`)
   - Logging estruturado com níveis (DEBUG, INFO, WARNING, ERROR)
   - Rotação de arquivos (10MB, 5 backups)
   - Logs separados por dia
   - Funções auxiliares (log_performance, log_error_with_context, etc.)

4. **Rate Limiting** (`utils/helpers.py`)
   - Decorator `@rate_limit` para limitar requisições/segundo
   - Decorator `@retry` para retry automático
   - Configurável via `config/settings.py`

### ✅ Sprint 2 - Importantes (EM PROGRESSO)

5. **Estrutura Modular**
   - Separação de responsabilidades em módulos distintos
   - Configurações centralizadas
   - Código mais testável e manutenível

6. **Exportação Excel/JSON** [PENDENTE]
   - [TODO] Implementar em `utils/exporters.py`

7. **Configurações Externas** (`config/settings.py`)
   - Classe `AppConfig` com todas as configurações
   - Pesos do score configuráveis
   - Thresholds configuráveis
   - Facilita ajustes sem modificar código

8. **Testes Automatizados** [PENDENTE]
   - [TODO] Implementar em `tests/`

### 🔄 Sprint 3 - Desejáveis (PENDENTE)

9. **Dashboard de Monitoramento** [PENDENTE]
10. **Alertas Inteligentes** [PENDENTE]
11. **Análise Fundamentalista** [PENDENTE]
12. **Comparação com Benchmarks** [PENDENTE]

## 🔧 Principais Configurações

```python
# config/settings.py

# Cache
CACHE_TTL_SHORT = 1800  # 30 min
CACHE_TTL_LONG = 86400  # 24 horas

# Análise
MAX_TICKERS_ANALYSIS = 200
MAX_DY_THRESHOLD = 40.0
MIN_DY_THRESHOLD = 0.1

# Otimização
MAX_ASSETS_PORTFOLIO = 15
DEFAULT_LOT_SIZE_ACOES = 100
DEFAULT_LOT_SIZE_OUTROS = 1

# Score (ponderação)
SCORE_WEIGHTS = {
    'dy': 0.4,           # 40% - Dividend Yield
    'consistencia': 0.3, # 30% - Consistência
    'cagr': 0.3          # 30% - Crescimento
}

# Paralelização
MAX_WORKERS = 10
ENABLE_PARALLEL = True

# Rate Limiting
MAX_REQUESTS_PER_SECOND = 5
MAX_RETRIES = 3
RETRY_DELAY = 1.0
```

## 📊 Fluxo de Dados

```
1. Usuário seleciona segmentos (Ações, FIIs, BDRs, ETFs)
   ↓
2. helpers.get_ticker_list_by_categories() → Lista de tickers
   ↓
3. calculator.analyze_stocks_parallel() → Análise paralela
   ├─ data_fetcher.get_stock_info() → Busca dados básicos (com cache/retry)
   ├─ data_fetcher.get_dividends_history() → Busca histórico de dividendos
   ├─ calculator.calculate_dividend_metrics() → Calcula métricas
   ├─ validators.validate_dividend_yield() → Valida DY
   └─ helpers.calculate_score() → Calcula score
   ↓
4. DataFrame com todos os ativos analisados
   ↓
5. optimizer.optimize_portfolio() → Otimiza carteira
   ├─ Filtra por DY mínimo
   ├─ Seleciona top N ativos por score
   ├─ Distribui capital proporcionalmente
   └─ Calcula quantidades (respeitando lotes)
   ↓
6. DataFrame otimizado com portfólio final
   ↓
7. Apresentação na UI (Streamlit)
```

## 🚀 Como Usar os Novos Módulos

### Exemplo 1: Buscar Dados de um Ativo

```python
from core.data_fetcher import data_fetcher

# Buscar informações básicas
info = data_fetcher.get_stock_info('ITUB4.SA')
print(f"Preço: R$ {info['preco_atual']:.2f}")

# Buscar dividendos
dividends = data_fetcher.get_dividends_history('ITUB4.SA', years=5)
print(f"Total de dividendos: R$ {dividends.sum():.2f}")

# Verificar liquidez
has_liquidity = data_fetcher.check_liquidity('ITUB4.SA')
```

### Exemplo 2: Calcular Métricas

```python
from core.calculator import calculate_dividend_metrics

metrics = calculate_dividend_metrics('ITUB4.SA', years=5)
print(f"DY 12M: {metrics['dy_12m']:.2f}%")
print(f"Consistência: {metrics['consistencia']:.1f}%")
print(f"Score: {metrics['score']:.2f}")
```

### Exemplo 3: Análise Paralela

```python
from core.calculator import analyze_stocks_parallel

tickers = ['ITUB4.SA', 'BBDC4.SA', 'VALE3.SA', 'PETR4.SA']
df_results = analyze_stocks_parallel(tickers)
print(df_results[['ticker', 'dy_12m', 'score']])
```

### Exemplo 4: Otimizar Portfólio

```python
from core.optimizer import optimize_portfolio

portfolio = optimize_portfolio(
    df_stocks=df_results,
    capital_total=50000,
    min_dy=5.0
)
print(portfolio[['ticker', 'quantidade', 'valor_investido', 'dy_12m']])
```

### Exemplo 5: Validações

```python
from utils.validators import validate_dividend_yield, validate_price

# Validar DY
is_valid, msg = validate_dividend_yield(8.5, 'ITUB4.SA')
print(f"DY válido: {is_valid} - {msg}")

# Validar preço
is_valid, msg = validate_price(25.50, 'ITUB4.SA')
print(f"Preço válido: {is_valid} - {msg}")
```

### Exemplo 6: Formatação

```python
from utils.formatters import format_currency, format_percentage

print(format_currency(1234.56))  # R$ 1.234,56
print(format_percentage(8.75))    # 8,75%
```

## 📝 TODOs Prioritários

1. ✅ Refatorar `analise_dividendos_app.py` para usar novos módulos
2. ✅ Implementar exportação Excel/JSON
3. ✅ Criar testes automatizados básicos
4. ✅ Implementar dashboard de monitoramento
5. ✅ Adicionar análise fundamentalista
6. ✅ Implementar comparação com benchmarks
7. ✅ Melhorar UI com componentes reutilizáveis

## 🔄 Migração Gradual

Para não quebrar a versão em produção:

1. **Fase 1** (ATUAL): Criar novos módulos sem tocar no app principal
2. **Fase 2**: Criar `app.py` usando novos módulos em paralelo
3. **Fase 3**: Testar `app.py` extensivamente
4. **Fase 4**: Trocar `analise_dividendos_app.py` por `app.py`
5. **Fase 5**: Remover código legado

## 📚 Referências

- yfinance: https://pypi.org/project/yfinance/
- Streamlit: https://docs.streamlit.io/
- Plotly: https://plotly.com/python/
- pandas: https://pandas.pydata.org/
