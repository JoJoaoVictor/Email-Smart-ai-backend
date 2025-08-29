"""
Rotas para processamento de emails via upload de arquivo
"""
from fastapi import APIRouter, HTTPException, File, UploadFile
from ..models.schemas import EmailResponse
from ..services.email_processor import email_processor
from ..services.file_processor import FileProcessor
from ..config.settings import MAX_FILE_SIZE
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["File Processing"])
file_processor = FileProcessor()

@router.post("/process-file", response_model=EmailResponse)
async def process_file_email(file: UploadFile = File(...)):
    """
    Processar e classificar email a partir de upload de arquivo
    """
    category = "Improdutivo"
    confidence = 0.5
    keywords = []
    extracted_text = ""
    detected_type = "unknown"
    file_content = b""
    
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="Nome do arquivo não fornecido")
        
        file_content = await file.read()
        
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="Arquivo muito grande")
        
        if len(file_content) == 0:
            raise HTTPException(status_code=400, detail="Arquivo vazio")
        
        extracted_text, detected_type = file_processor.process_file(file_content, file.filename)
        
        if extracted_text and len(extracted_text.strip()) >= 5:
            category, confidence, keywords = email_processor.classify_email(extracted_text)
            response_text = email_processor.generate_response(extracted_text, category, keywords)
        else:
            response_text = email_processor.generate_response("", category)
        
        email_preview = extracted_text[:100] + '...' if len(extracted_text) > 100 else extracted_text
        
        file_info = {
            "filename": file.filename,
            "size_bytes": len(file_content),
            "detected_type": detected_type,
            "extracted_chars": len(extracted_text),
            "success": bool(extracted_text and len(extracted_text) >= 5)
        }
        
        logger.info(f"Arquivo processado - {file.filename} -> {category}")
        
        return EmailResponse(
            category=category,
            confidence=round(confidence, 2),
            response=response_text,
            email_preview=email_preview,
            processed_keywords=keywords[:10] if keywords else None,
            file_info=file_info
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no processamento de arquivo: {e}")
        
        response_text = email_processor.generate_response(extracted_text, category, keywords)
        
        return EmailResponse(
            category=category,
            confidence=confidence,
            response=response_text,
            email_preview=extracted_text[:100] + '...' if extracted_text else "Erro na extração",
            processed_keywords=keywords,
            file_info={
                "filename": file.filename if file else "unknown",
                "size_bytes": len(file_content),
                "detected_type": detected_type,
                "extracted_chars": len(extracted_text) if extracted_text else 0,
                "success": False,
                "error": str(e)
            }
        )