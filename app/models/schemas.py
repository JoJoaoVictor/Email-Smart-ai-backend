"""
Schemas Pydantic para validação de dados
"""
from pydantic import BaseModel, Field
from typing import Optional

class EmailRequest(BaseModel):
    """Schema para requisição de processamento de email"""
    email: str = Field(
        ..., 
        min_length=5, 
        max_length=10000, 
        description="Conteúdo do email para classificação"
    )

class EmailResponse(BaseModel):
    """Schema para resposta da classificação de email"""
    category: str = Field(description="Categoria: Produtivo ou Improdutivo")
    confidence: float = Field(ge=0.0, le=1.0, description="Nível de confiança")
    response: str = Field(description="Resposta automática sugerida")
    email_preview: str = Field(description="Preview do email processado")
    processed_keywords: Optional[list[str]] = Field(
        default=None, 
        description="Palavras-chave identificadas"
    )
    file_info: Optional[dict] = Field(
        default=None, 
        description="Informações do arquivo processado"
    )

class HealthCheckResponse(BaseModel):
    """Schema para health check"""
    status: str
    openai_configured: bool
    nltk_ready: bool
    file_processing: str
    timestamp: str

class OpenAITestResponse(BaseModel):
    """Schema para teste da OpenAI"""
    status: str
    message: Optional[str] = None
    response: Optional[str] = None
    openai_configured: bool
    model: Optional[str] = None