"""
Rotas utilitárias e de informação
"""
from fastapi import APIRouter
from datetime import datetime
from ..models.schemas import HealthCheckResponse, OpenAITestResponse
from ..services.openai_service import openai_service
from ..models.constants import ALLOWED_FILE_TYPES
from ..config.settings import MAX_FILE_SIZE
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Utility"])

@router.get("/", include_in_schema=False)
async def root():
    """Endpoint raiz - Informações da API"""
    return {
        "status": "OK", 
        "message": "EmailSmart API está funcionando!",
        "version": "4.0.0",
        "openai_configured": openai_service.is_configured(),
        "endpoints": {
            "docs": "/docs",
            "process_email": "/process-email",
            "process_file": "/process-file",
            "health": "/health",
            "test_openai": "/test-openai"
        }
    }

@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check da aplicação"""
    return {
        "status": "healthy",
        "openai_configured": openai_service.is_configured(),
        "nltk_ready": True,
        "file_processing": "enabled",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@router.get("/test-openai", response_model=OpenAITestResponse)
async def test_openai():
    """Testar conexão com OpenAI"""
    try:
        result = openai_service.test_connection()
        return {
            "status": result["status"],
            "response": result.get("response"),
            "openai_configured": openai_service.is_configured(),
            "model": result.get("model")
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "openai_configured": openai_service.is_configured()
        }

@router.get("/supported-formats")
async def get_supported_formats():
    """Listar formatos de arquivo suportados"""
    return {
        "supported_formats": ALLOWED_FILE_TYPES,
        "max_file_size_mb": MAX_FILE_SIZE / 1024 / 1024,
        "description": "Formatos suportados para upload de arquivo"
    }