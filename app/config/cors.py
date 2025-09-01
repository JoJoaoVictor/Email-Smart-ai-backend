# app/config/settings.py
import os
from typing import List

# Outras configurações existentes...
API_CONFIG = {
    "title": "EmailSmart API",
    "description": "API para classificação inteligente de emails",
    "version": "1.0.0"
}

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

#
ALLOWED_ORIGINS: List[str] = [
     # Domínio principal de produção
    "https://email-smart-ai-frontend.vercel.app",
    
    # Domínios de preview/deploy da Vercel
    "https://email-smart-ai-frontend-git-main-jojoaovictors-projects.vercel.app",
    "https://email-smart-ai-frontend-7Ouo3xOxt-jojoaovictors-projects.vercel.app",
    
     # Desenvolvimento local
    "http://localhost:3000",                    
    "http://localhost:5173",                       
    "http://localhost:8000",                      
    "https://localhost:3000",                      
    "https://localhost:5173",                     
]
