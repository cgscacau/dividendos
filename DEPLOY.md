# 🚀 Guia de Deploy - Otimizador de Carteira de Dividendos

## 📋 Pré-requisitos

- Conta no GitHub (gratuita)
- Repositório: https://github.com/cgscacau/dividendos

## ☁️ Deploy no Streamlit Cloud (Recomendado - GRÁTIS)

### Passo 1: Criar Conta no Streamlit Cloud

1. Acesse: https://share.streamlit.io/
2. Clique em "Sign in with GitHub"
3. Autorize o Streamlit a acessar sua conta GitHub

### Passo 2: Fazer Deploy do Aplicativo

1. **No Streamlit Cloud Dashboard:**
   - Clique em "New app" (botão no canto superior direito)

2. **Configurações do Deploy:**
   ```
   Repository: cgscacau/dividendos
   Branch: main
   Main file path: analise_dividendos_app.py
   ```

3. **Configurações Avançadas (Opcional):**
   - Python version: 3.9 ou superior
   - As dependências serão instaladas automaticamente do `requirements.txt`

4. **Clique em "Deploy!"**
   - O primeiro deploy pode levar 2-5 minutos
   - Você verá logs de instalação em tempo real

### Passo 3: Acessar seu Aplicativo

- URL será gerada automaticamente no formato:
  ```
  https://[seu-app-name].streamlit.app
  ```
- Você pode customizar o nome do app nas configurações

### Passo 4: Atualizações Automáticas

- ✅ Cada commit na branch `main` atualiza o app automaticamente
- ✅ Não precisa fazer deploy manual novamente
- ✅ Rollback é possível através do GitHub

## 🏠 Deploy Local (Para Desenvolvimento)

### Requisitos
- Python 3.8+
- pip instalado

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/cgscacau/dividendos.git
cd dividendos

# 2. (Opcional) Crie um ambiente virtual
python -m venv venv

# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o aplicativo
streamlit run analise_dividendos_app.py
```

### Acessar Localmente

- O aplicativo abrirá automaticamente em: `http://localhost:8501`
- Se não abrir, acesse manualmente esse endereço no navegador

## 🐳 Deploy com Docker (Avançado)

### Criar Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "analise_dividendos_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build e Run

```bash
# Build da imagem
docker build -t dividendos-app .

# Executar container
docker run -p 8501:8501 dividendos-app
```

## 🔧 Configurações do Streamlit

### Arquivo `.streamlit/config.toml`

Já incluído no repositório com configurações otimizadas:

```toml
[theme]
primaryColor="#FF4B4B"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F0F2F6"
textColor="#262730"
font="sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false
```

### Variáveis de Ambiente (Opcional)

Para configurações sensíveis, use secrets do Streamlit Cloud:

1. No dashboard do app, vá em "Settings" → "Secrets"
2. Adicione variáveis no formato TOML:

```toml
# .streamlit/secrets.toml (NÃO commitar este arquivo!)
api_key = "sua_chave_aqui"
```

3. Acesse no código:
```python
import streamlit as st
api_key = st.secrets["api_key"]
```

## 📦 Dependências do Projeto

Arquivo `requirements.txt`:

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

**Notas:**
- Todas as dependências são públicas e gratuitas
- Não há necessidade de API keys externas
- Yahoo Finance é usado via biblioteca `yfinance` (gratuito)

## ⚙️ Troubleshooting

### Problema: App não carrega ou dá timeout

**Solução:**
- O app pode estar analisando muitos ativos de uma vez
- Reduza a quantidade de tickers sendo analisados
- Verifique se o Yahoo Finance está acessível

### Problema: Dados desatualizados

**Solução:**
- Use o cache do Streamlit (já implementado)
- TTL padrão é 30 minutos para dados de mercado
- Para forçar atualização, reinicie o app ou limpe o cache

### Problema: Deploy falha no Streamlit Cloud

**Solução:**
1. Verifique se todos os arquivos estão commitados no GitHub
2. Confirme que `requirements.txt` está correto
3. Veja os logs de erro no dashboard do Streamlit Cloud
4. Verifique se o arquivo principal está correto: `analise_dividendos_app.py`

### Problema: Erro de importação de módulos

**Solução:**
- Certifique-se que `acoes_b3_completa.py` está no mesmo diretório
- Verifique se o arquivo não tem erros de sintaxe

## 🌐 Opções de Hospedagem Alternativas

### 1. Heroku (Gratuito com limitações)

```bash
# Instalar Heroku CLI
heroku login
heroku create seu-app-dividendos

# Criar Procfile
echo "web: streamlit run analise_dividendos_app.py --server.port=$PORT" > Procfile

# Deploy
git push heroku main
```

### 2. Replit (Gratuito)

1. Importe o repositório do GitHub
2. Configure o comando run: `streamlit run analise_dividendos_app.py`
3. Clique em "Run"

### 3. Railway (Gratuito com $5 de crédito)

1. Conecte sua conta GitHub
2. Selecione o repositório
3. Railway detectará automaticamente que é um app Python
4. Configure o start command: `streamlit run analise_dividendos_app.py`

## 📊 Monitoramento

### Streamlit Cloud

- Analytics integrados mostram:
  - Número de usuários
  - Tempo de uso
  - Erros e exceções
  - Performance do app

### Google Analytics (Opcional)

Adicione no início do `analise_dividendos_app.py`:

```python
import streamlit.components.v1 as components

# Google Analytics
components.html("""
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-XXXXXXXXX-X"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'UA-XXXXXXXXX-X');
</script>
""", height=0)
```

## 🔒 Segurança

### Boas Práticas

- ✅ Não commite API keys ou senhas
- ✅ Use `.gitignore` para excluir arquivos sensíveis
- ✅ Use secrets do Streamlit Cloud para variáveis sensíveis
- ✅ Mantenha dependências atualizadas

### Arquivo `.gitignore` (Já Incluído)

```
__pycache__/
*.py[cod]
.streamlit/secrets.toml
venv/
.env
*.log
```

## 📞 Suporte

**Problemas com o código:**
- Abra uma issue no GitHub: https://github.com/cgscacau/dividendos/issues

**Problemas com Streamlit Cloud:**
- Documentação: https://docs.streamlit.io/streamlit-community-cloud
- Fórum: https://discuss.streamlit.io/

## ✅ Checklist de Deploy

Antes de fazer deploy, certifique-se:

- [ ] Código funciona localmente (`streamlit run analise_dividendos_app.py`)
- [ ] `requirements.txt` está completo e atualizado
- [ ] `.streamlit/config.toml` está commitado
- [ ] `.gitignore` está configurado corretamente
- [ ] Não há API keys hardcoded no código
- [ ] Todos os arquivos necessários estão no GitHub
- [ ] Branch `main` está atualizada

## 🎉 Próximos Passos Após Deploy

1. **Teste o aplicativo online** completamente
2. **Compartilhe o URL** com usuários
3. **Configure domínio customizado** (opcional, disponível no Streamlit Cloud)
4. **Monitore uso e erros** através do dashboard
5. **Atualize regularmente** através de commits no GitHub

---

**Deploy realizado com sucesso?** 🚀

Agora seu aplicativo está online e acessível 24/7 gratuitamente!

*Última atualização: 31/12/2025*
