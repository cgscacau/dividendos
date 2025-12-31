# 🎯 Otimizador de Carteira de Dividendos - B3 Completa

## 🚀 Acesso Rápido

**📱 Como Acessar o Aplicativo Online:**

### Opção 1: Streamlit Cloud (Recomendado)
1. Acesse: [Streamlit Cloud](https://share.streamlit.io/)
2. Faça deploy do repositório: `https://github.com/cgscacau/dividendos`
3. Arquivo principal: `analise_dividendos_app.py`

### Opção 2: Executar Localmente
```bash
git clone https://github.com/cgscacau/dividendos.git
cd dividendos
pip install -r requirements.txt
streamlit run analise_dividendos_app.py
```

**🔥 Última Atualização:** Deploy configurado - pronto para Streamlit Cloud!

## ✨ O Que Este Aplicativo Faz?

Este é um **otimizador completo de carteira de dividendos** que analisa **TODA a B3** - incluindo **Ações, FIIs, BDRs e ETFs** - e ajuda investidores brasileiros a:

1. **🏆 Descobrir os Melhores Ativos** - Ranking automático com filtros por segmento
2. **💼 Criar Portfólio Otimizado** - Define quantos ativos comprar baseado no seu capital
3. **📅 Planejar Fluxo de Caixa** - Mostra quanto você receberá por mês em dividendos
4. **📈 Validar Estratégia** - Simula o desempenho real do portfólio nos últimos 5 anos

## 🔧 Melhorias Mais Recentes

### ✅ Correção Crítica Aplicada (Commit 6616f6b)
- **Problema resolvido:** Erro `TypeError: 'NoneType' object is not iterable` corrigido
- **Solução:** Adicionado `return` statement na função `get_all_b3_tickers()`
- **Melhoria:** Agora inclui automaticamente BDRs e ETFs na lista de análise
- **Status:** ✅ Aplicativo 100% funcional

### 🆕 Lista Expandida de Ativos (350+ tickers)
- **200+ Ações** - Todos os setores da B3
- **100+ FIIs** - Diferentes tipos (lajes, shoppings, logística, recebíveis)
- **30+ BDRs** - Empresas internacionais (Tech, Financeiro, Consumo)
- **14 ETFs** - Índices diversos

### 🎯 Filtro de DY Máximo
- **Novo controle:** DY Máximo (padrão 40%)
- **Objetivo:** Remover outliers e dividendos não recorrentes
- **Benefício:** Evita ações com DY > 40% que podem ter problemas (ex: dívida, dados incorretos)

## 🆕 NOVIDADE: Análise Completa da B3

### 📊 Segmentos Disponíveis

Agora você pode analisar **TODOS os tipos de ativos**:

- **📈 Ações** - Empresas brasileiras (PETR4, VALE3, ITUB4, etc.)
- **🏢 FIIs** - Fundos Imobiliários (HGLG11, VISC11, MXRF11, etc.)
- **🌎 BDRs** - Ações Internacionais (AAPL34, MSFT34, AMZO34, etc.)
- **📊 ETFs** - Fundos de Índice (BOVA11, SMAL11, IVVB11, etc.)

### 🎯 Filtros Inteligentes por Segmento

**Na barra lateral**, você pode selecionar quais segmentos deseja analisar:

```
☑️ Ações (empresas brasileiras)
☑️ FIIs (fundos imobiliários)
☐ BDRs (ações internacionais)
☐ ETFs (fundos de índice)
```

**Exemplos de uso:**
- ✅ Quer apenas FIIs? Desmarque os outros
- ✅ Quer mix de Ações + FIIs? Marque ambos
- ✅ Quer diversificação global com BDRs? Inclua BDRs

### 🔍 Verificação de Liquidez

O sistema verifica automaticamente:
- ✅ Ativos com negociação nos **últimos 60 dias**
- ✅ Volume médio mínimo de negociação
- ✅ Dados disponíveis de dividendos

## 📊 Ativos Incluídos

### 📈 Ações (100+)
Setores completos:
- **Bancos**: ITUB4, BBDC4, BBAS3, SANB11, BPAC11
- **Energia**: TAEE11, EGIE3, CPLE6, CMIG4, ENBR3, NEOE3
- **Petróleo/Gás**: PETR3, PETR4, PRIO3, RECV3
- **Mineração**: VALE3, BRAP4, GOAU4, CMIN3, GGBR4
- **Saneamento**: SAPR11, SBSP3, CSMG3
- **Telecom**: TIMS3, VIVT3
- **Varejo**: LREN3, MGLU3, VVAR3, PETZ3, SOMA3
- **Alimentação**: ABEV3, BRFS3, JBSS3, BEEF3, MRFG3
- **Construção**: CYRE3, MRVE3, EZTC3, TEND3
- **Papel/Celulose**: KLBN11, SUZB3
- **Saúde**: RDOR3, FLRY3, HAPV3, QUAL3
- **Educação**: COGN3, YDUQ3, ANIM3
- **Logística**: CCRO3, RAIL3, ECOR3
- **E muito mais!**

### 🏢 FIIs (50+)
Tipos diversos:
- **Lajes Corporativas**: HGLG11, BTLG11, XPLG11, KNCR11
- **Shoppings**: MALL11, XPML11, VISC11, HSML11
- **Logística**: HGRU11, HGRE11, VILG11, TRXF11
- **Híbridos**: MXRF11, KNRI11, HGPO11
- **Recebíveis**: RZTR11, BCFF11, RBRR11, KFOF11
- **Títulos**: PVBI11, IRDM11, BCRI11
- **E mais!**

### 🌎 BDRs (40+)
Empresas globais:
- **Tech**: AAPL34, MSFT34, GOGL34, AMZO34, META34, NVDC34
- **Streaming**: NFLX34, SPOT34, DISB34
- **E-commerce**: UBER34, AIRB34
- **Financeiro**: V1SA34, PYPL34
- **Consumo**: NIKE34, COCA34, PEP34, STARBUCKS34
- **Industrial**: BOEI34, UPS34
- **Asiáticas**: BABA34, BIDU34, TCEHY34
- **Europeias**: ASML34, NESN34, LVMH34

### 📊 ETFs (15+)
Índices diversos:
- **Ibovespa**: BOVA11, BOVX11
- **Small Caps**: SMAL11
- **Internacional**: IVVB11, SPXI11, ISUS11
- **Dividendos**: DIVO11
- **Setoriais**: MATB11, FIND11, PIBB11

## 🎯 Como Usar o Aplicativo

### Passo 1️⃣: Selecionar Segmentos

**Na barra lateral esquerda:**
1. Marque os segmentos que deseja analisar:
   - ☑️ Ações
   - ☑️ FIIs  
   - ☑️ BDRs
   - ☑️ ETFs

### Passo 2️⃣: Ranking de Ativos

**Na aba "📊 Ranking de Ativos":**
1. Clique em **"🚀 Analisar Ativos Selecionados"**
2. Aguarde a análise (pode levar alguns minutos)
3. Explore os resultados:
   - Use filtros adicionais (categoria, setor, DY, consistência)
   - Veja gráficos comparativos
   - Identifique as melhores oportunidades

### Passo 3️⃣: Otimizar Portfólio

**Na aba "💼 Otimizador de Portfólio":**
1. Configure:
   - **Capital Total**: Quanto você tem (ex: R$ 50.000)
   - **Lote Mínimo**: Geralmente 100 (ações) ou 1 (FIIs)
   - **DY Mínimo**: Filtro de qualidade (sugestão: 4%)
2. Clique em **"🚀 Otimizar Portfólio"**
3. Veja:
   - Quantos ativos comprar de cada tipo
   - Calendário mensal de dividendos
   - Gráficos de distribuição

### Passo 4️⃣: Simular Histórico

**Na aba "📈 Simulação Histórica":**
1. Escolha período (1 a 5 anos)
2. Clique em **"📊 Simular Histórico"**
3. Analise:
   - Quanto você teria recebido
   - Evolução ano a ano
   - ROI apenas em dividendos

## 💡 Exemplos Práticos

### Exemplo 1: Carteira Conservadora (Ações + FIIs)

**Configuração:**
- ☑️ Ações
- ☑️ FIIs
- ☐ BDRs
- ☐ ETFs
- Capital: R$ 100.000
- DY Mínimo: 6%

**Resultado esperado:**
- 60% em Ações de alta dividendo (ITSA4, TAEE11, BBDC4)
- 40% em FIIs (HGLG11, MXRF11, VISC11)
- DY Médio: ~7.5%
- Dividendos mensais: ~R$ 625

### Exemplo 2: Carteira Agressiva (Ações Growth + BDRs)

**Configuração:**
- ☑️ Ações
- ☐ FIIs
- ☑️ BDRs
- ☐ ETFs
- Capital: R$ 50.000
- DY Mínimo: 2%

**Resultado esperado:**
- Mix de ações brasileiras de tecnologia
- BDRs de empresas americanas (AAPL34, MSFT34)
- Foco em crescimento + dividendos
- Diversificação geográfica

### Exemplo 3: Renda Passiva Pura (FIIs)

**Configuração:**
- ☐ Ações
- ☑️ FIIs
- ☐ BDRs
- ☐ ETFs
- Capital: R$ 200.000
- DY Mínimo: 8%

**Resultado esperado:**
- 100% FIIs de alta distribuição
- Dividendos mensais consistentes
- DY Médio: ~9%
- Dividendos mensais: ~R$ 1.500

### Exemplo 4: Estratégia Passiva (ETFs)

**Configuração:**
- ☐ Ações
- ☐ FIIs
- ☐ BDRs
- ☑️ ETFs
- Capital: R$ 30.000

**Resultado esperado:**
- BOVA11 (Ibovespa)
- SMAL11 (Small Caps)
- DIVO11 (Dividendos)
- Diversificação automática
- Baixo custo de gestão

## 📊 Funcionalidades Principais

### 🏆 Ranking Inteligente
- ✅ Analisa automaticamente centenas de ativos
- ✅ Calcula **Score Composto**: DY (40%) + Consistência (30%) + CAGR (30%)
- ✅ Filtros por categoria, setor, DY, consistência
- ✅ Visualizações interativas coloridas por segmento
- ✅ Análise comparativa por categoria

### 💼 Otimizador de Portfólio
- ✅ Distribui capital automaticamente
- ✅ Considera diversificação por setor e categoria
- ✅ Trabalha com lotes adequados (100 para ações, 1 para FIIs)
- ✅ Maximiza DY mantendo qualidade
- ✅ Gráficos de alocação por ativo e categoria

### 📅 Calendário de Dividendos
- ✅ Identifica meses de pagamento de cada ativo
- ✅ Estima fluxo mensal baseado em histórico
- ✅ Mostra quais ativos pagam em cada mês
- ✅ Ajuda a planejar fluxo de caixa

### 📈 Simulação Histórica Real
- ✅ Usa dados reais dos últimos 5 anos
- ✅ Calcula dividendos efetivamente recebidos
- ✅ ROI detalhado por ano e mês
- ✅ Análise estatística completa

## 🎨 Interface Melhorada

### Cores por Categoria
- 🔵 **Ações** - Azul
- 🟠 **FIIs** - Laranja
- 🟢 **BDRs** - Verde
- 🔴 **ETFs** - Vermelho

### Sidebar Interativa
```
🔍 Filtros de Segmento
┌─────────────────────────┐
│ ☑️ Ações                │
│ ☑️ FIIs                 │
│ ☐ BDRs                  │
│ ☐ ETFs                  │
└─────────────────────────┘
```

## 🔧 Melhorias Técnicas

### Performance
- ✅ Cache inteligente (24h para lista de tickers)
- ✅ Cache de 30min para dados de mercado
- ✅ Limitação a 100 ativos por análise (performance)
- ✅ Verificação paralela de liquidez

### Validação
- ✅ Verifica negociação nos últimos 60 dias
- ✅ Valida volume mínimo de negociação
- ✅ Exclui ativos sem dados de dividendos
- ✅ Categorização automática precisa

## 🆚 Comparação com Versão Anterior

| Funcionalidade | Versão Antiga | Versão Nova |
|---|---|---|
| Tipos de ativos | Apenas ~30 ações | 200+ (Ações, FIIs, BDRs, ETFs) |
| Seleção | Lista fixa | ✅ Filtros por segmento |
| Categorização | Manual | ✅ Automática |
| Validação liquidez | Não tinha | ✅ Últimos 60 dias |
| Gráficos | Uma cor | ✅ Cores por categoria |
| Análise setorial | Limitada | ✅ Completa por segmento |

## 📖 Glossário

- **DY (Dividend Yield)**: % de retorno em dividendos sobre o preço
- **FII**: Fundo de Investimento Imobiliário
- **BDR**: Brazilian Depositary Receipt (ações internacionais)
- **ETF**: Exchange Traded Fund (fundo de índice)
- **CAGR**: Taxa de crescimento composta anual
- **Consistência**: % de anos com pagamento de dividendos
- **Score**: Métrica que combina DY, Consistência e CAGR
- **Lote**: Quantidade mínima para negociação

## 🔧 Instalação e Deploy

### 🏠 Instalação Local

```bash
# Clone o repositório
git clone https://github.com/cgscacau/dividendos.git
cd dividendos

# Instale as dependências
pip install -r requirements.txt

# Execute o aplicativo
streamlit run analise_dividendos_app.py
```

### ☁️ Deploy no Streamlit Cloud (GRÁTIS!)

**Passo a Passo:**

1. **Criar conta no Streamlit Cloud**
   - Acesse: https://share.streamlit.io/
   - Faça login com sua conta GitHub

2. **Fazer Deploy**
   - Clique em "New app"
   - Selecione o repositório: `cgscacau/dividendos`
   - Branch: `main`
   - Arquivo principal: `analise_dividendos_app.py`
   - Clique em "Deploy!"

3. **Pronto!**
   - Seu app estará online em poucos minutos
   - URL no formato: `https://seu-app.streamlit.app`
   - Atualiza automaticamente a cada commit no GitHub

**Arquivos de Configuração Incluídos:**
- ✅ `.streamlit/config.toml` - Configurações de tema e servidor
- ✅ `requirements.txt` - Todas as dependências necessárias
- ✅ `.gitignore` - Arquivos que não devem ir para o repositório

## 📦 Dependências

```
streamlit
pandas
numpy
yfinance
plotly
requests
beautifulsoup4
lxml
```

## ⚠️ Avisos Importantes

1. **Dados**: Yahoo Finance pode ter atrasos ou imprecisões
2. **Projeções**: Baseadas em histórico, não garantem futuro
3. **Não Considera**:
   - Impostos (15% sobre dividendos, IR BDR diferente)
   - Corretagem e taxas
   - Valorização/desvalorização dos ativos
   - Eventos extraordinários
4. **Performance**: Análise limitada a 100 ativos por vez
5. **Uso**: Apenas educacional, não é recomendação

## 🎓 Casos de Uso

### 1. Aposentadoria - Renda Mensal
**Meta:** R$ 5.000/mês em dividendos
- Selecione: Ações + FIIs
- DY alvo: 7%
- Capital necessário: ~R$ 857.000
- Use calendário para ver distribuição mensal

### 2. Diversificação Global
**Meta:** Exposição internacional + renda local
- Selecione: Ações + FIIs + BDRs
- Mix 40% Ações BR / 30% FIIs / 30% BDRs
- Proteção cambial via BDRs
- Dividendos em múltiplas moedas

### 3. Estratégia Passiva
**Meta:** Investir sem gestão ativa
- Selecione: ETFs
- BOVA11 (mercado geral)
- DIVO11 (dividendos)
- Rebalanceamento automático

### 4. Renda Mensal Alta
**Meta:** Maximizar fluxo de caixa mensal
- Selecione: FIIs
- Foco em DY > 10%
- Diversificação por tipo (lajes, shoppings, logística)
- Pagamentos mensais garantidos

## 🚀 Próximas Melhorias

- [ ] Integração com API da B3 (dados oficiais)
- [ ] Notificações de pagamento de dividendos
- [ ] Cálculo automático de impostos
- [ ] Comparação com benchmarks (CDI, IPCA, Ibovespa)
- [ ] Análise fundamentalista (ROE, Dívida, etc.)
- [ ] Rebalanceamento automático sugerido
- [ ] Exportação para Excel com fórmulas
- [ ] Integração com corretoras (CEI)

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas! Abra uma issue no GitHub.

## 📞 Repositório

**GitHub:** https://github.com/cgscacau/dividendos

## 📄 Licença

Projeto educacional. Use por sua conta e risco.

---

**Desenvolvido para investidores que buscam renda passiva através de dividendos na B3** 💰

*Última atualização: 30/12/2025*

---

## 🎯 Comece Agora!

1. **Acesse:** https://8501-itf3xysvgh1hx79t5ys0g-c81df28e.sandbox.novita.ai
2. **Selecione** seus segmentos na barra lateral
3. **Clique** em "Analisar Ativos"
4. **Explore** os melhores ativos da B3!
