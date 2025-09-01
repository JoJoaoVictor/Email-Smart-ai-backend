# emailsmart-backend/src/main.py
"""
Ponto de entrada principal da aplicação EmailSmart
"""
import logging
from fastapi import FastAPI
from app.config.settings import API_CONFIG
from app.config.cors import setup_cors
from app.middleware.logging_middleware import logging_middleware
from app.routes import email_routes, file_routes, utility_routes
import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Criar aplicação FastAPI
app = FastAPI(**API_CONFIG)

# Configurar CORS
app = setup_cors(app)

# Adicionar middleware de logging
app.middleware("http")(logging_middleware)

# Registrar rotas
app.include_router(email_routes.router, prefix="")
app.include_router(file_routes.router, prefix="")
app.include_router(utility_routes.router, prefix="")

@app.on_event("startup")
async def startup_event():
    """Evento de inicialização da aplicação"""
    logger.info("Iniciando EmailSmart API")
    logger.info(f"📖 Documentação disponível em: http://localhost:8000/docs")

@app.on_event("shutdown")
async def shutdown_event():
    """Evento de desligamento da aplicação"""
    logger.info("🛑 Desligando EmailSmart API")

if __name__ == "__main__":
    import uvicorn
    from app.config.settings import HOST, PORT, DEBUG
    
    uvicorn.run(
        "src.main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info" if DEBUG else "warning"
    )