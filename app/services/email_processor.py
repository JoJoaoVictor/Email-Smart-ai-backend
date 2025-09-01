"""
Serviço principal para processamento e classificação de emails
"""
import re
import logging
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from .openai_service import openai_service
from ..models.constants import PRODUCTIVE_KEYWORDS, UNPRODUCTIVE_KEYWORDS, KEYWORD_WEIGHTS

logger = logging.getLogger(__name__)

class EmailProcessor:
    """Processador de emails para classificação e geração de respostas"""
    
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = self._load_stopwords()
    
    def _load_stopwords(self):
        """Carregar stopwords com fallback robusto"""
        try:
            # Tenta baixar stopwords se não estiverem disponíveis
            try:
                nltk.data.find('corpora/stopwords')
            except LookupError:
                nltk.download('stopwords', quiet=True)
            
            # Tenta português primeiro
            return set(stopwords.words('portuguese'))
        except Exception as e:
            logger.warning(f"Stopwords português não disponíveis: {e}")
            try:
                # Fallback para inglês
                return set(stopwords.words('english'))
            except Exception as e2:
                logger.warning(f"Stopwords inglês não disponíveis: {e2}")
                # Fallback manual se tudo falhar
                return self._get_manual_stopwords()
    
    def _get_manual_stopwords(self):
        """Stopwords manuais como fallback absoluto"""
        portuguese_stopwords = {
            'a', 'ao', 'aos', 'aquela', 'aquelas', 'aquele', 'aqueles', 'aquilo', 'as', 'até', 
            'com', 'como', 'da', 'das', 'de', 'dela', 'delas', 'dele', 'deles', 'depois', 
            'do', 'dos', 'e', 'ela', 'elas', 'ele', 'eles', 'em', 'entre', 'era', 'eram', 
            'é', 'essa', 'essas', 'esse', 'esses', 'esta', 'estas', 'este', 'estes', 'eu', 
            'foi', 'foram', 'há', 'isso', 'isto', 'já', 'lhe', 'lhes', 'mais', 'mas', 'me', 
            'mesmo', 'meu', 'meus', 'minha', 'minhas', 'muito', 'na', 'nas', 'no', 'nos', 
            'nós', 'nossa', 'nossas', 'nosso', 'nossos', 'num', 'numa', 'o', 'os', 'ou', 
            'para', 'pela', 'pelas', 'pelo', 'pelos', 'por', 'quando', 'que', 'quem', 'se', 
            'sem', 'seu', 'seus', 'só', 'sua', 'suas', 'também', 'te', 'tem', 'têm', 'teu', 
            'teus', 'tu', 'tua', 'tuas', 'um', 'uma', 'você', 'vocês', 'vos', 'para', 'é',
            'ser', 'estar', 'tem', 'ter', 'foi', 'são', 'como', 'mas', 'já', 'ou', 'se',
            'não', 'sim', 'também', 'muito', 'pouco', 'mais', 'menos', 'bem', 'mal', 'agora',
            'depois', 'antes', 'sempre', 'nunca', 'hoje', 'ontem', 'amanhã'
        }
        logger.info("Usando stopwords manuais - NLTK não disponível")
        return portuguese_stopwords
    
    def _ensure_punkt(self):
        """Garante que o tokenizer punkt está disponível"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            try:
                nltk.download('punkt', quiet=True)
            except Exception as e:
                logger.warning(f"Punkt tokenizer não disponível: {e}")
    
    def preprocess_text(self, text: str) -> tuple[str, list[str]]:
        """Pré-processar texto e extrair palavras-chave"""
        processed_text = ""
        keywords = []
        
        try:
            if not text or not isinstance(text, str):
                return processed_text, keywords
            
            # Garante que o punkt está disponível
            self._ensure_punkt()
            
            text = text.lower()
            text = re.sub(r'[^a-zA-Záàâãéèêíïóôõöúçñ\s]', ' ', text)
            
            # Tenta tokenização com fallback
            try:
                tokens = word_tokenize(text)
            except Exception as tokenize_error:
                logger.warning(f"Tokenização falhou, usando split simples: {tokenize_error}")
                tokens = text.split()
            
            filtered_tokens = [
                word for word in tokens 
                if word not in self.stop_words and len(word) > 2
            ]
            
            keywords = [
                word for word in filtered_tokens 
                if word in PRODUCTIVE_KEYWORDS or word in UNPRODUCTIVE_KEYWORDS
            ]
            
            stemmed_tokens = [self.stemmer.stem(word) for word in filtered_tokens]
            processed_text = ' '.join(stemmed_tokens)
            
        except Exception as e:
            logger.error(f"Erro no pré-processamento: {e}")
            # Fallback básico
            if text:
                text_lower = text.lower()
                keywords = [
                    word for word in text_lower.split() 
                    if word in PRODUCTIVE_KEYWORDS or word in UNPRODUCTIVE_KEYWORDS
                ]
                processed_text = text_lower
        
        return processed_text, keywords
    
    def classify_email(self, email_text: str) -> tuple[str, float, list[str]]:
        """Classificar email em Produtivo/Improdutivo"""
        category = "Improdutivo"
        confidence = 0.5
        keywords = []
        
        try:
            if not email_text or len(email_text.strip()) < 5:
                return category, confidence, keywords
            
            _, keywords = self.preprocess_text(email_text)
            email_lower = email_text.lower()
            
            productive_score = 0
            unproductive_score = 0
            
            for word in PRODUCTIVE_KEYWORDS:
                count = email_lower.count(word)
                weight = KEYWORD_WEIGHTS.get(word, 1.2)
                productive_score += count * weight
            
            for word in UNPRODUCTIVE_KEYWORDS:
                count = email_lower.count(word)
                weight = KEYWORD_WEIGHTS.get(word, 1.0)
                unproductive_score += count * weight
            
            total_score = productive_score + unproductive_score
            
            if total_score == 0:
                if any(word in email_lower for word in ['reunião', 'projeto', 'relatório', 'prazo', 'entreg']):
                    category, confidence = "Produtivo", 0.6
                else:
                    category, confidence = "Improdutivo", 0.55
            else:
                ratio = productive_score / total_score
                
                if ratio > 0.6:
                    category, confidence = "Produtivo", min(0.95, 0.7 + (ratio - 0.6) * 2)
                elif ratio > 0.4:
                    category, confidence = "Produtivo", 0.6 + (ratio - 0.4) * 0.5
                elif ratio > 0.3:
                    category, confidence = "Improdutivo", 0.55
                else:
                    category, confidence = "Improdutivo", min(0.95, 0.7 + (0.3 - ratio) * 2)
            
            return category, confidence, keywords
            
        except Exception as e:
            logger.error(f"Erro na classificação: {e}")
            return category, confidence, keywords
    
    def generate_response(self, email_text: str, category: str, keywords: list[str] = None) -> str:
        """Gerar resposta automática"""
        if not email_text or len(email_text.strip()) < 5:
            return self._get_fallback_response(category)
        
        try:
            if openai_service.is_configured():
                prompt = self._build_contextual_prompt(email_text, category, keywords)
                system_prompt = self._get_system_prompt(category)
                return openai_service.generate_response(prompt, system_prompt)
            else:
                return self._get_contextual_fallback_response(email_text, category, keywords)
                
        except Exception as e:
            logger.error(f"Erro na geração de resposta: {e}")
            return self._get_contextual_fallback_response(email_text, category, keywords)
    
    def _get_system_prompt(self, category: str) -> str:
        """Obter prompt do sistema baseado na categoria"""
        if category == "Produtivo":
            return "Você é um assistente virtual profissional. Responda emails corporativos de forma clara e útil."
        else:
            return "Você é um assistente pessoal educado. Responda emails pessoais de forma amigável."
    
    def _build_contextual_prompt(self, email_text: str, category: str, keywords: list[str]) -> str:
        """Construir prompt contextualizado"""
        context = self._analyze_email_context(email_text, keywords)
        
        if category == "Produtivo":
            return f"""
            ANÁLISE: {context}
            EMAIL: "{email_text[:1000]}"
            INSTRUÇÕES: Gere resposta profissional baseada no contexto.
            RESPOSTA:
            """
        else:
            return f"""
            ANÁLISE: {context}
            EMAIL: "{email_text[:1000]}"
            INSTRUÇÕES: Gere resposta amigável baseada no contexto.
            RESPOSTA:
            """
    
    def _analyze_email_context(self, email_text: str, keywords: list[str]) -> str:
        """Analisar contexto do email"""
        email_lower = email_text.lower()
        context_elements = []
        
        # Detecção de tipo (implementação simplificada)
        if any(word in email_lower for word in ['solicit', 'pedido', 'requer']):
            context_elements.append("Solicitação")
        elif any(word in email_lower for word in ['problema', 'erro', 'bug']):
            context_elements.append("Problema")
        elif any(word in email_lower for word in ['dúvida', 'pergunta']):
            context_elements.append("Dúvida")
        
        if keywords:
            context_elements.append(f"Palavras-chave: {', '.join(keywords[:3])}")
        
        return " | ".join(context_elements) if context_elements else "Mensagem geral"
    
    def _get_contextual_fallback_response(self, email_text: str, category: str, keywords: list[str]) -> str:
        """Resposta fallback contextualizada"""
        email_lower = email_text.lower()
        
        if category == "Produtivo":
            if any(word in email_lower for word in ['solicit', 'pedido']):
                return "Agradecemos sua solicitação. Nossa equipe analisará e retornará em breve."
            elif any(word in email_lower for word in ['problema', 'erro']):
                return "Lamentamos pelo problema. Nossa equipe técnica está trabalhando na solução."
            else:
                return "Agradecemos seu contato. Retornaremos em breve com uma resposta."
        else:
            if any(word in email_lower for word in ['agradec', 'obrigad']):
                return "Ficamos felizes com seu agradecimento! É um prazer ajudar."
            else:
                return "Agradecemos seu contato! Ficamos felizes em receber sua mensagem."
    
    def _get_fallback_response(self, category: str) -> str:
        """Resposta fallback básica"""
        return "Agradecemos seu contato. Nossa equipe retornará em breve." if category == "Produtivo" else "Obrigado pelo seu email!"

# Instância global do processador
email_processor = EmailProcessor()