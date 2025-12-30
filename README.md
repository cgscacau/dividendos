# 🎯 Otimizador de Carteira de Dividendos

## 🚀 Acesso Rápido

**📱 Aplicativo Online:** https://8501-itf3xysvgh1hx79t5ys0g-c81df28e.sandbox.novita.ai

## ✨ O Que Este Aplicativo Faz?

Este é um **otimizador completo de carteira de dividendos** que ajuda investidores brasileiros a:

1. **🏆 Descobrir as Melhores Ações** - Ranking automático de 30+ ações com melhor histórico de dividendos
2. **💼 Criar Portfólio Otimizado** - Define quantas ações comprar de cada empresa baseado no seu capital
3. **📅 Planejar Fluxo de Caixa** - Mostra quanto você receberá por mês em dividendos
4. **📈 Validar Estratégia** - Simula o desempenho real do portfólio nos últimos 5 anos

## 🎯 Como Usar (Passo a Passo)

### Passo 1️⃣: Ranking de Ações
1. Abra o aplicativo
2. Vá para a aba **"📊 Ranking de Ações"**
3. Clique em **"🔄 Atualizar Ranking"**
4. Aguarde 2-3 minutos enquanto analisa 30+ ações
5. Explore os resultados:
   - Use filtros (setor, DY mínimo, consistência)
   - Veja gráficos comparativos
   - Identifique as melhores oportunidades

### Passo 2️⃣: Otimizar Portfólio
1. Vá para a aba **"💼 Otimizador de Portfólio"**
2. Configure:
   - **Capital Total**: Quanto você tem para investir (ex: R$ 50.000)
   - **Lote Mínimo**: Geralmente 100 ações
   - **DY Mínimo**: Filtro de qualidade (sugestão: 4%)
3. Clique em **"🚀 Otimizar Portfólio"**
4. Veja os resultados:
   - Quantas ações comprar de cada empresa
   - Quanto investir em cada uma
   - DY médio da sua carteira
   - Calendário mensal de dividendos
5. Baixe o portfólio em CSV

### Passo 3️⃣: Simular Histórico
1. Vá para a aba **"📈 Simulação Histórica"**
2. Escolha quantos anos simular (1 a 5)
3. Clique em **"📊 Simular Histórico"**
4. Analise:
   - Quanto você REALMENTE teria recebido
   - Evolução ano a ano
   - Volatilidade mensal
   - ROI apenas em dividendos

## 💡 Exemplo Prático

**Cenário:** Você tem R$ 50.000 e quer renda passiva mensal

**No Aplicativo:**

1. **Ranking** mostra as melhores ações:
   - ITSA4: Score 8.5, DY 7.2%
   - TAEE11: Score 8.2, DY 8.1%
   - BBDC4: Score 7.9, DY 6.5%
   - ... e mais

2. **Otimizador** calcula:
   - Comprar 500 ITSA4 = R$ 5.000
   - Comprar 300 TAEE11 = R$ 8.000
   - Comprar 400 BBDC4 = R$ 6.500
   - ... (total 10 empresas)
   - **DY Médio da Carteira: 7.1%**
   - **Dividendos Mensais: ~R$ 295**

3. **Simulação Histórica** mostra:
   - Últimos 5 anos: R$ 17.850 recebidos
   - ROI: 35.7% (apenas dividendos)
   - Média mensal real: R$ 297

## 📊 Principais Funcionalidades

### 🏆 Ranking Inteligente
- Analisa 30+ ações automaticamente
- Calcula **Score Composto**:
  - 40% DY (Dividend Yield)
  - 30% Consistência de pagamento
  - 30% CAGR (crescimento dos dividendos)
- Filtros por setor, DY mínimo, consistência
- Visualizações interativas

### 💼 Otimizador de Portfólio
- Distribui capital automaticamente
- Considera diversificação por setor
- Trabalha com lotes fechados (100 ações)
- Maximiza DY mantendo qualidade
- Gráficos de alocação

### 📅 Calendário de Dividendos
- Mostra em quais meses você receberá pagamentos
- Identifica quais empresas pagam em cada mês
- Estima valor mensal baseado em histórico
- Ajuda a planejar fluxo de caixa

### 📈 Simulação Histórica Real
- Usa dados reais dos últimos 5 anos
- Calcula quanto você TERIA recebido
- Análise estatística completa
- ROI detalhado
- Gráficos de evolução

## 🏢 Ações Analisadas

**Setores Cobertos:**
- 🏦 **Bancos**: ITUB4, BBDC4, BBAS3, SANB11
- ⚡ **Energia**: TAEE11, EGIE3, CPLE6, CMIG4, ENBR3
- 💧 **Saneamento**: SAPR11, SBSP3, CSMG3
- 📱 **Telecom**: TIMS3, VIVT3
- 🛡️ **Seguros**: BBSE3, PSSA3
- 🛢️ **Petróleo**: PETR4, PRIO3
- 🏢 **Imobiliário**: TRPL4, MULT3
- 🛒 **Varejo**: LREN3
- 📊 **Holdings**: ITSA4

## 📖 Glossário

- **DY (Dividend Yield)**: % de retorno em dividendos sobre o preço da ação
- **Consistência**: % de anos em que a empresa pagou dividendos
- **CAGR**: Taxa de crescimento composta anual dos dividendos
- **Score**: Métrica que combina DY, Consistência e CAGR
- **Lote**: Quantidade mínima para negociação (geralmente 100 ações)
- **ROI**: Retorno sobre investimento

## 🔧 Instalação Local

```bash
# Clone o repositório
git clone https://github.com/cgscacau/dividendos.git
cd dividendos

# Instale as dependências
pip install -r requirements.txt

# Execute o aplicativo
streamlit run analise_dividendos_app.py
```

## 📦 Dependências

- streamlit
- pandas
- numpy
- yfinance
- plotly

## ⚠️ Avisos Importantes

1. **Dados do Yahoo Finance**: Podem ter atrasos ou imprecisões
2. **Projeções**: Baseadas em histórico, não garantem resultados futuros
3. **Não Considera**:
   - Impostos (15% sobre dividendos)
   - Corretagem
   - Valorização/desvalorização das ações
4. **Uso**: Apenas para fins educacionais
5. **Não é**: Recomendação de investimento

## 🆚 Diferença das Versões

| Arquivo | Descrição |
|---------|-----------|
| `analise_dividendos_app.py` | ✅ **Versão Otimizada** (atual) |
| `analise_dividendos_app_backup.py` | Versão original (análise individual) |
| `analise_dividendos_otimizado.py` | Cópia da versão otimizada |

## 📚 Documentação Adicional

- `README_MELHORIAS.md` - Documentação técnica detalhada
- Comentários no código explicam cada função

## 🎓 Casos de Uso

### 1. Aposentadoria
**Meta:** R$ 3.000/mês em dividendos
- Com DY de 6%, precisa investir ~R$ 600.000
- Use o otimizador para distribuir o capital
- Valide com simulação histórica

### 2. Renda Extra
**Meta:** R$ 500/mês em dividendos
- Com DY de 6%, precisa investir ~R$ 100.000
- Diversifique em 5-8 empresas
- Acompanhe o calendário mensal

### 3. Acumulação
**Meta:** Reinvestir dividendos para crescer patrimônio
- Foque em ações com CAGR alto
- Use filtro de consistência > 80%
- Monitore crescimento anual

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas! Abra uma issue no GitHub.

## 📄 Licença

Projeto educacional. Use por sua conta e risco.

---

**Desenvolvido para investidores que buscam renda passiva através de dividendos** 💰

*Última atualização: 30/12/2025*
