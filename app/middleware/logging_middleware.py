"""
Middleware para logging de requisições
"""
import logging
from fastapi import Request

logger = logging.getLogger(__name__)

async def logging_middleware(request: Request, call_next):
    """Middleware para log de requisições e respostas"""
    logger.info(f"Requisição: {request.method} {request.url}")
    
    response = await call_next(request)
    
    logger.info(f"Resposta: {response.status_code}")
    return response