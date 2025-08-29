"""
Rotas para processamento de emails via texto
"""
from fastapi import APIRouter, HTTPException
from ..models.schemas import EmailRequest, EmailResponse
from ..services.email_processor import email_processor
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Email Processing"])

@router.post("/process-email", response_model=EmailResponse)
async def process_email(request: EmailRequest):
    """
    Processar e classificar email enviado como texto
    """
    try:
        email_text = request.email.strip()
        
        if len(email_text) < 5:
            raise HTTPException(status_code=422, detail="Texto muito curto")
        
        category, confidence, keywords = email_processor.classify_email(email_text)
        response_text = email_processor.generate_response(email_text, category, keywords)
        
        email_preview = email_text[:100] + '...' if len(email_text) > 100 else email_text
        
        logger.info(f"Email processado - {category} ({confidence:.2f})")
        
        return EmailResponse(
            category=category,
            confidence=round(confidence, 2),
            response=response_text,
            email_preview=email_preview,
            processed_keywords=keywords[:10] if keywords else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no processamento: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no processamento")