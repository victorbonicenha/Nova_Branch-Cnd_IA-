# 🤖 RPA - Certidões Negativas com IA

Este projeto automatiza a emissão, download e processamento de **Certidões Negativas (CNDs)** utilizando **Selenium + AntiCaptcha + OpenAI + OCR**.  

Além de baixar e organizar os arquivos, o robô usa **IA (ChatChef com OpenAI + EasyOCR/pdfplumber)** para extrair automaticamente informações como **número, validade e emissão das certidões**.  
Os resultados são armazenados no banco de dados e enviados via **Telegram**.

---

## 📂 Estrutura do Projeto

📁 RPA-CND  
│  
├── 📜 main.py — código principal (fluxo das certidões)  
├── 📦 requirements.txt — dependências do projeto  
├── 🔑 .env — variáveis de ambiente (não subir no GitHub)  
├── 📘 README.md — documentação  
├── 📜 Solution_bank.py — módulo de conexão e queries no banco  
├── 📜 Solution_telegram.py — módulo de envio de mensagens/imagens para Telegram  
└── 📜 Solution_file_ia.py — módulo de integração com OpenAI (ChatChef)  

---

## ⚙️ Pré-requisitos

- 🐍 Python 3.9+  
- 🌐 Google Chrome instalado  
- ⚡ ChromeDriver (gerenciado automaticamente pelo `webdriver-manager`)  
- 🔑 Conta no [Anti-Captcha](https://anti-captcha.com/)  
- 🤖 Bot no Telegram (token + chat_id)  
- 🗄️ Banco de dados SQL Server (tabela `cnd_testes`)  
- 🧠 Chave da OpenAI (para ChatChef/LLM)  

---

📥 Instalação e Uso

🔹 Clone o repositório
```bash
git clone https://github.com/seuusuario/RPA-CND.git
cd RPA-CND
```

---

🔹 Crie e ative o ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

---

🔹 Instale as dependências
```bash
pip install -r requirements.txt
```

---

🔑 Configuração do .env

Crie um arquivo .env na raiz do projeto com os seguintes dados:
```bash
# CNPJs/CPF
CNPJ_BASE=12345678
CNPJ_BASICO=12345678
CNPJ_SC=12345678000199
CPF=12345678900
NOME=Seu Nome

# API Keys
CHAVE_API_CAPTCHA=xxxx
CHAVE_OPENIA=sk-xxxx

# Telegram
ITOKEN_TELEGRAM=xxxx
CHAT_ID=xxxx

# Banco de dados
DB_USER=usuario
DB_PASS=senha
DB_HOST=host
DB_NAME=rpa

# Caminhos
BASE_PATH=C:\Robos\Certidoes
```

---

▶️ Execução

Para rodar o robô:
```bash
python main.py
