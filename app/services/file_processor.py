"""
Serviço para processamento de arquivos
"""
import logging
from fastapi import HTTPException
from io import BytesIO
import PyPDF2
import pdfplumber
import docx2txt
import magic
from ..models.constants import ALLOWED_FILE_TYPES

logger = logging.getLogger(__name__)

class FileProcessor:
    """Processador de arquivos para extração de texto"""
    
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """Extrair texto de PDF usando múltiplas abordagens"""
        text = ""
        
        # Tentar pdfplumber primeiro (mais preciso)
        try:
            with pdfplumber.open(BytesIO(file_content)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                logger.info("Texto extraído com pdfplumber")
                return text
        except Exception as e:
            logger.warning(f"pdfplumber falhou: {e}")
        
        # Fallback para PyPDF2
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            if text.strip():
                logger.info("Texto extraído com PyPDF2")
                return text
        except Exception as e:
            logger.warning(f"PyPDF2 falhou: {e}")
        
        raise Exception("Não foi possível extrair texto do PDF")
    
    @staticmethod
    def extract_text_from_docx(file_content: bytes) -> str:
        """Extrair texto de arquivos DOCX"""
        try:
            text = docx2txt.process(BytesIO(file_content))
            if not text.strip():
                raise Exception("Documento DOCX vazio")
            return text
        except Exception as e:
            raise Exception(f"Erro ao processar DOCX: {e}")
    
    @staticmethod
    def extract_text_from_txt(file_content: bytes) -> str:
        """Extrair texto de arquivos TXT com detecção de encoding"""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                text = file_content.decode(encoding)
                if text.strip():
                    return text
            except UnicodeDecodeError:
                continue
        
        raise Exception("Não foi possível decodificar o arquivo")
    
    @staticmethod
    def detect_file_type(file_content: bytes) -> str:
        """Detectar tipo MIME do arquivo"""
        try:
            mime_type = magic.from_buffer(file_content, mime=True)
            return mime_type
        except:
            # Fallback para detecção básica
            if file_content.startswith(b'%PDF'):
                return 'application/pdf'
            elif file_content.startswith(b'PK'):
                return 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            else:
                return 'text/plain'
    
    @classmethod
    def process_file(cls, file_content: bytes, filename: str) -> tuple[str, str]:
        """Processar arquivo e extrair texto"""
        mime_type = cls.detect_file_type(file_content)
        logger.info(f"Tipo detectado: {mime_type} para {filename}")
        
        if mime_type not in ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=400, 
                detail=f"Tipo de arquivo não suportado: {mime_type}"
            )
        
        # Extrair texto baseado no tipo
        if mime_type == 'application/pdf':
            text = cls.extract_text_from_pdf(file_content)
        elif mime_type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword']:
            text = cls.extract_text_from_docx(file_content)
        elif mime_type == 'text/plain':
            text = cls.extract_text_from_txt(file_content)
        else:
            raise HTTPException(status_code=400, detail=f"Processamento não implementado para: {mime_type}")
        
        if not text or len(text.strip()) < 5:
            raise HTTPException(status_code=400, detail="Arquivo não contém texto suficiente")
        
        return text, mime_type