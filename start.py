#!/usr/bin/env python3
"""
Script de inicialização para o Heroku
"""
import os
import subprocess
import sys

def main():
    print("🚀 Iniciando EmailSmart Backend...")
    print("📥 Configurando recursos NLTK...")
    
    # Executa o setup do NLTK
    try:
        import nltk_setup
        nltk_setup.download_nltk_resources()
    except Exception as e:
        print(f"⚠️  Erro no setup NLTK: {e}")
        print("⏭️  Continuando com fallbacks manuais...")
    
    print("✅ Configuração concluída")
    print("🎯 Iniciando servidor Gunicorn...")
    
    # Inicia o gunicorn
    os.execvp("gunicorn", [
        "gunicorn", 
        "app.main:app", 
        "--bind", f"0.0.0.0:{os.environ.get('PORT', '8000')}",
        "--workers", "1",
        "--threads", "2",
        "--timeout", "120"
    ])

if __name__ == "__main__":
    main()