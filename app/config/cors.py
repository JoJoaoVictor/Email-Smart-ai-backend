"""
Configuração CORS para a aplicação
"""
from fastapi.middleware.cors import CORSMiddleware
from .settings import ALLOWED_ORIGINS

def setup_cors(app):
    """Configurar middleware CORS"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
        allow_headers=["*"],
        expose_headers=["*"]
    )
    return app