# pre_start.py (na raiz do projeto)
import nltk
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_nltk_data():
    """Pre-download dos recursos NLTK"""
    logger.info("Preparando recursos NLTK para o Heroku...")
    
    # Cria diretório para nltk_data no Heroku
    nltk_dir = os.path.join(os.getcwd(), 'nltk_data')
    os.makedirs(nltk_dir, exist_ok=True)
    
    # Adiciona ao path do NLTK
    nltk.data.path.append(nltk_dir)
    
    # Download dos recursos
    resources = ['stopwords', 'punkt']
    for resource in resources:
        try:
            nltk.download(resource, download_dir=nltk_dir, quiet=True)
            logger.info(f"✅ {resource} baixado com sucesso")
        except Exception as e:
            logger.error(f"❌ Erro ao baixar {resource}: {e}")

if __name__ == "__main__":
    download_nltk_data()