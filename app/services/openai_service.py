"""
Serviço para integração com OpenAI
"""
import logging
from openai import OpenAI
from ..config.settings import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_MAX_TOKENS, OPENAI_TIMEOUT

logger = logging.getLogger(__name__)

class OpenAIService:
    """Serviço para comunicação com API da OpenAI"""
    
    def __init__(self):
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Inicializar cliente OpenAI"""
        if not OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY não configurada")
            return
        
        try:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            logger.info("Cliente OpenAI inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar cliente OpenAI: {e}")
            self.client = None
    
    def is_configured(self) -> bool:
        """Verificar se OpenAI está configurada"""
        return self.client is not None
    
    def generate_response(self, prompt: str, system_prompt: str) -> str:
        if not self.is_configured():
            raise Exception("OpenAI não configurada")
        
        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=OPENAI_MAX_TOKENS,
                temperature=0.8,
                timeout=OPENAI_TIMEOUT
            )
            content = response.choices[0].message.content
            return content.strip() if content else ""
            
        except Exception as e:
            logger.error(f"Erro na geração com OpenAI: {e}")
            raise

        
    def test_connection(self) -> dict:
        """Testar conexão com OpenAI"""
        if not self.is_configured():
            return {"status": "error", "message": "OpenAI não configurada"}
        
        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": "Teste de conexão. Responda 'OK'"}],
                max_tokens=10,
                temperature=0.1
            )
            
            return {
                "status": "success",
                "response": response.choices[0].message.content,
                "model": OPENAI_MODEL
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

# Instância global do serviço
openai_service = OpenAIService()