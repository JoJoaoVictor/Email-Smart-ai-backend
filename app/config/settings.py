"""
Configurações da aplicação e variáveis de ambiente
"""
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações da API
API_CONFIG = {
    "title": "EmailSmart - Classificador Inteligente de Emails",
    "description": "API para classificação automática de emails com IA",
    "version": "4.0.0",
    "docs_url": "/docs",
    "redoc_url": "/redoc",
    "debug": True,
    
}

# Configuração OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "250"))
OPENAI_TIMEOUT = int(os.getenv("OPENAI_TIMEOUT", "15"))

# Configurações de arquivo
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Configurações do servidor
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Origins permitidos para CORS
ALLOWED_ORIGINS = [
    # DOMÍNIOS DA VERCEL (ADICIONE ESTES)
    "https://email-smart-ai-frontend.vercel.app",
    "https://email-smart-ai-frontend-git-main-jojoaovictors-projects.vercel.app",
    "https://email-smart-ai-frontend-7Ouo3xOxt-jojoaovictors-projects.vercel.app",
    
    # Desenvolvimento local (já existente)
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://localhost:4200",
    "http://localhost:8000",
    
    # Versões HTTPS do localhost (importante)
    "https://localhost:3000",
    "https://localhost:5173",
    "https://localhost:8000",
]