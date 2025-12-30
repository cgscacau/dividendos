# 🎯 Otimizador de Carteira de Dividendos - Melhorias Implementadas

## 🌟 Visão Geral

Este é um aplicativo completo para análise e otimização de carteiras de dividendos, desenvolvido com Streamlit e yfinance. O sistema analisa automaticamente as melhores ações brasileiras pagadoras de dividendos e cria portfólios otimizados para gerar fluxo de caixa mensal consistente.

## 📊 Acesso ao Aplicativo

**URL do Aplicativo:** https://8501-itf3xysvgh1hx79t5ys0g-c81df28e.sandbox.novita.ai

## ✨ Principais Funcionalidades

### 1. 📊 Ranking Inteligente de Ações

**O que faz:**
- Analisa automaticamente 30+ ações brasileiras conhecidas por pagamento de dividendos
- Calcula métricas avançadas para cada ação:
  - **DY (Dividend Yield) dos últimos 12 meses**
  - **DY médio histórico**
  - **Consistência**: % de anos com pagamento de dividendos
  - **CAGR dos dividendos**: Taxa de crescimento composta anual
  - **Score Geral**: Métrica ponderada que considera DY (40%), Consistência (30%) e Crescimento (30%)

**Recursos:**
- Filtros por setor, DY mínimo e consistência
- Visualizações interativas (gráficos de barras, scatter plots)
- Análise comparativa por setor
- Ranking atualizado em tempo real

**Setores Cobertos:**
- Bancos (ITUB4, BBDC4, BBAS3, SANB11)
- Energia (TAEE11, EGIE3, CPLE6, CMIG4, ENBR3)
- Saneamento (SAPR11, SBSP3, CSMG3)
- Telecomunicações (TIMS3, VIVT3)
- Seguros (BBSE3, PSSA3)
- Petróleo (PETR4, PRIO3)
- Imobiliário (TRPL4, MULT3)
- Varejo (LREN3)
- Holdings (ITSA4)

### 2. 💼 Otimizador de Portfólio

**O que faz:**
- Recebe o capital disponível do usuário
- Calcula automaticamente a melhor distribuição entre as ações
- Considera diversificação por setor
- Trabalha com lotes mínimos configuráveis

**Algoritmo de Otimização:**
1. Filtra ações pelo DY mínimo desejado
2. Seleciona top 10 ações por score
3. Distribui capital proporcionalmente ao score
4. Ajusta para lotes fechados (ex: 100 ações)
5. Recalcula valores reais investidos

**Saídas:**
- Quantidade exata de ações de cada empresa
- Valor investido por ação
- Percentual da carteira
- Dividendos estimados (anual e mensal)
- DY médio da carteira
- Gráficos de distribuição (por ação e por setor)

### 3. 📅 Calendário de Dividendos

**O que faz:**
- Analisa os últimos 24 meses de pagamentos
- Identifica em quais meses cada empresa costuma pagar
- Projeta o fluxo mensal de dividendos

**Visualizações:**
- Gráfico de barras com valores mensais estimados
- Tabela detalhada mostrando quais ações pagam em cada mês
- Identifica meses com maior e menor fluxo

**Benefício:**
- O usuário pode visualizar se terá fluxo de caixa todos os meses
- Identifica "buracos" no calendário
- Ajuda a planejar melhor o fluxo de caixa pessoal

### 4. 📈 Simulação Histórica (Últimos 5 Anos)

**O que faz:**
- Simula quanto o usuário **REALMENTE** teria recebido em dividendos
- Usa dados históricos reais dos últimos 1 a 5 anos
- Considera as quantidades exatas do portfólio otimizado

**Análises Incluídas:**
- **Total de dividendos recebidos** no período
- **Média anual** e **média mensal** de dividendos
- **Gráfico anual**: Evolução dos dividendos ano a ano
- **Gráfico mensal**: Fluxo de caixa mês a mês com linha de média
- **Análise estatística**: Média, mediana, desvio padrão, mínimo, máximo
- **ROI (Return on Investment)**: Retorno percentual apenas em dividendos

**Exemplo de Interpretação:**
```
Capital Investido: R$ 50.000,00
Total de Dividendos (5 anos): R$ 15.234,50
ROI Total: 30,47%
ROI Médio Anual: 6,09%
Média Mensal: R$ 253,91
```

### 5. 💹 Análise de Fluxo de Caixa

**Integrado em múltiplas áreas:**
- **Projeção**: Baseada no DY dos últimos 12 meses
- **Realizado**: Baseado em dados históricos reais
- **Comparação**: Mostra diferença entre projeção e realização

**Métricas Calculadas:**
- Dividendos anuais esperados
- Dividendos mensais médios (projeção e realização)
- Volatilidade mensal (desvio padrão)
- Meses com maior e menor pagamento

## 🎯 Como Usar o Aplicativo

### Passo 1: Ranking de Ações
1. Acesse a aba **"📊 Ranking de Ações"**
2. Clique em **"🔄 Atualizar Ranking"** (aguarde 2-3 minutos)
3. Explore os resultados:
   - Use filtros para refinar (setor, DY mínimo, consistência)
   - Analise gráficos e tabelas
   - Identifique as melhores oportunidades

### Passo 2: Otimizar Portfólio
1. Acesse a aba **"💼 Otimizador de Portfólio"**
2. Configure:
   - **Capital Total**: Quanto você tem para investir (ex: R$ 50.000)
   - **Lote Mínimo**: Geralmente 100 ações (padrão da B3)
   - **DY Mínimo**: Filtro para eliminar ações com DY muito baixo
3. Clique em **"🚀 Otimizar Portfólio"**
4. Analise o resultado:
   - Veja quantas ações comprar de cada empresa
   - Confira o DY médio da carteira
   - Analise o calendário de pagamentos mensais
5. Baixe o portfólio em CSV para referência

### Passo 3: Simular Histórico
1. Acesse a aba **"📈 Simulação Histórica"**
2. Escolha quantos anos simular (1 a 5)
3. Clique em **"📊 Simular Histórico"**
4. Analise:
   - Quanto você teria recebido em dividendos
   - Como foi a evolução ano a ano
   - Volatilidade mensal
   - ROI apenas em dividendos

## 💡 Casos de Uso Práticos

### Caso 1: Aposentadoria Complementar
**Objetivo:** Gerar R$ 3.000/mês em dividendos

**Como usar:**
1. No otimizador, calcule: R$ 3.000/mês × 12 = R$ 36.000/ano
2. Se DY médio for 6%, precisa investir: R$ 36.000 ÷ 0,06 = R$ 600.000
3. Configure capital de R$ 600.000 e otimize
4. Veja no calendário se o fluxo mensal atende à necessidade
5. Na simulação histórica, valide se funcionaria nos últimos anos

### Caso 2: Diversificação de Carteira
**Objetivo:** Alocar 30% do patrimônio em dividendos

**Como usar:**
1. Se tem R$ 200.000, aloque R$ 60.000 em dividendos
2. Use o ranking para entender o mercado
3. Otimize o portfólio com R$ 60.000
4. Confira a diversificação por setor no gráfico de pizza
5. Valide a consistência histórica na simulação

### Caso 3: Investidor Iniciante
**Objetivo:** Começar com R$ 5.000 focando em qualidade

**Como usar:**
1. Configure DY mínimo alto (ex: 6%)
2. Configure capital de R$ 5.000
3. O sistema recomendará poucas ações de alta qualidade
4. Veja no ranking a consistência histórica
5. Use a simulação para entender volatilidade

## 📊 Diferenças do Aplicativo Original

| Funcionalidade | Aplicativo Original | Aplicativo Otimizado |
|---|---|---|
| Análise | Manual, uma ação por vez | Automática, 30+ ações |
| Ranking | Não tinha | ✅ Score inteligente |
| Portfólio | Usuário decidia manualmente | ✅ Otimização automática |
| Quantidade de ações | Manual | ✅ Calcula automaticamente |
| Calendário mensal | Não tinha | ✅ Fluxo mensal projetado |
| Simulação histórica | Não tinha | ✅ Performance real 5 anos |
| ROI | Não calculava | ✅ ROI detalhado |
| Exportação | Não tinha | ✅ Download CSV |
| Diversificação | Manual | ✅ Automática por setor |

## 🧮 Metodologia de Cálculo

### Score de Qualidade
```
Score = (DY_12m × 0.4) + (Consistência × 0.3) + (CAGR × 0.3)
```

**Exemplo:**
- DY 12M: 8% → 8 × 0.4 = 3.2
- Consistência: 100% → 100 × 0.3 = 30.0
- CAGR: 10% → 10 × 0.3 = 3.0
- **Score Total: 36.2**

### Otimização de Portfólio
```
Peso da Ação = Score da Ação / Soma de Todos os Scores
Capital Alocado = Peso × Capital Total
Quantidade = (Capital Alocado / Preço) ajustado para lotes
```

### DY (Dividend Yield)
```
DY = (Soma dos Dividendos dos Últimos 12 Meses / Preço Atual) × 100
```

### CAGR (Taxa de Crescimento Composta)
```
CAGR = ((Valor Final / Valor Inicial)^(1/Anos) - 1) × 100
```

## ⚠️ Limitações e Avisos

1. **Dados do Yahoo Finance**: Podem conter atrasos ou imprecisões
2. **Projeções**: Baseadas em histórico, não garantem futuro
3. **Não considera**:
   - Impostos (15% sobre dividendos no Brasil)
   - Custos de corretagem
   - Valorização/desvalorização das ações
   - Eventos extraordinários (bonificações, splits)
4. **Apenas educacional**: Não é recomendação de investimento

## 🔧 Tecnologias Utilizadas

- **Streamlit**: Interface web interativa
- **yfinance**: Dados financeiros do Yahoo Finance
- **Pandas**: Manipulação de dados
- **NumPy**: Cálculos numéricos
- **Plotly**: Gráficos interativos
- **Python 3.8+**: Linguagem base

## 📦 Arquivos do Projeto

- `analise_dividendos_otimizado.py`: Aplicativo principal otimizado
- `analise_dividendos_app.py`: Aplicativo original (análise individual)
- `requirements.txt`: Dependências do Python
- `README_MELHORIAS.md`: Esta documentação

## 🚀 Como Executar Localmente

```bash
# 1. Clone ou navegue até o diretório
cd /home/user/webapp

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o aplicativo otimizado
streamlit run analise_dividendos_otimizado.py

# Ou execute o aplicativo original
streamlit run analise_dividendos_app.py
```

## 💻 Requisitos do Sistema

- Python 3.8 ou superior
- Conexão com internet (para buscar dados do Yahoo Finance)
- 4GB RAM mínimo (8GB recomendado)
- Navegador moderno (Chrome, Firefox, Safari, Edge)

## 🎓 Próximas Melhorias Sugeridas

1. **Rebalanceamento automático**: Sugerir quando ajustar o portfólio
2. **Alertas de pagamento**: Notificar quando dividendos serão pagos
3. **Integração com IR**: Calcular impostos automaticamente
4. **Comparação com CDI/IPCA**: Benchmark de rentabilidade
5. **Análise fundamentalista**: ROE, Dívida/EBITDA, etc.
6. **Backtesting**: Testar estratégias em períodos customizados
7. **API para integração**: Permitir uso em outras aplicações
8. **Multi-moeda**: Suportar ações internacionais (REITs, etc.)

## 📞 Suporte

Para questões técnicas ou sugestões de melhorias:
- Verifique a documentação completa
- Consulte os comentários no código
- Teste com diferentes cenários de capital

## 📜 Licença

Este projeto é para fins educacionais. Use por sua conta e risco.

---

**Desenvolvido com ❤️ para investidores focados em dividendos**

*Última atualização: 30/12/2025*
