# EmailSmart Backend 📧

Um backend inteligente para processamento e análise de emails usando FastAPI, OpenAI e NLTK.

## 🚀 Funcionalidades

- **API RESTful** com FastAPI
- **Processamento de linguagem natural** com NLTK
- **Integração com OpenAI** para análise inteligente
- **Upload de arquivos** com suporte a multipart
- **Documentação automática** com Swagger/OpenAPI

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

## 🛠️ Instalação

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd emailsmart-backend
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Instale as dependências
```bash
pip install -r requirements.txt
```

### 5. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
OPENAI_API_KEY=sua_chave
# Adicione outras variáveis conforme necessário
```

## 🚀 Como executar

### Desenvolvimento (com auto-reload)
```bash
uvicorn app.main:app --reload
```

### Produção
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Executar com parâmetros específicos
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

## 📖 Documentação da API

Após iniciar o servidor, acesse:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc
- **API Base:** http://127.0.0.1:8000

## 📁 Estrutura do Projeto

```
emailsmart-backend/
├── app/
│   ├── __init__.py
│   └── main.py              # Arquivo principal da aplicação
├── venv/                    # Ambiente virtual
├── .env                     # Variáveis de ambiente
├── .gitignore              # Arquivos ignorados pelo Git
├── requirements.txt         # Dependências do projeto
└── README.md               # Este arquivo
```

## 📦 Dependências Principais

- **FastAPI** (0.116.1) - Framework web moderno
- **Uvicorn** (0.35.0) - Servidor ASGI
- **OpenAI** (0.28.1) - Integração com API da OpenAI
- **NLTK** (3.8.1) - Processamento de linguagem natural
- **Pydantic** (2.11.7) - Validação de dados
- **python-multipart** (0.0.20) - Suporte a upload de arquivos

## 🔧 Comandos Úteis

### Atualizar dependências
```bash
pip install --upgrade -r requirements.txt
```

### Gerar requirements.txt
```bash
pip freeze > requirements.txt
```

### Executar com logs detalhados
```bash
uvicorn app.main:app --reload --log-level debug
```

## 🐛 Solução de Problemas

### Erro: "No module named 'app'"
- Certifique-se de que existe um arquivo `__init__.py` na pasta `app/`
- Execute o comando a partir da raiz do projeto

### Erro de importação de módulos
- Verifique se o ambiente virtual está ativado
- Reinstale as dependências: `pip install -r requirements.txt`

### Porta já em uso
```bash
# Use uma porta diferente
uvicorn app.main:app --port 8001 --reload
```

## 🚀 Deploy

### Usando Docker (opcional)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Variáveis de ambiente para produção
```env
ENVIRONMENT=production
DEBUG=False
OPENAI_API_KEY=sua_chave_aqui
```

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

João Victor - (https://github.com/JoJoaoVictor)

---

