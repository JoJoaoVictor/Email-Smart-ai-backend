import nltk
import os
import sys

def download_nltk_resources():
    """Faz download dos recursos do NLTK de forma robusta"""
    resources = ['stopwords', 'punkt']
    
    print("🚀 Iniciando download dos recursos NLTK...")
    
    for resource in resources:
        try:
            # Verifica se já existe
            if resource == 'stopwords':
                nltk.data.find('corpora/stopwords')
                print(f"✅ {resource} já disponível")
            else:
                nltk.data.find(f'tokenizers/{resource}')
                print(f"✅ {resource} já disponível")
        except LookupError:
            try:
                print(f"📥 Baixando {resource}...")
                nltk.download(resource, quiet=True)
                print(f"✅ {resource} baixado com sucesso")
            except Exception as e:
                print(f"❌ Erro ao baixar {resource}: {e}")
                # Tenta com diretório específico
                try:
                    nltk_data_path = os.path.join(os.getcwd(), 'nltk_data')
                    os.makedirs(nltk_data_path, exist_ok=True)
                    nltk.download(resource, download_dir=nltk_data_path, quiet=True)
                    nltk.data.path.append(nltk_data_path)
                    print(f"✅ {resource} baixado para diretório local")
                except Exception as e2:
                    print(f"⚠️  {resource} não disponível, usando fallback")
    
    print("🎉 Configuração NLTK concluída!")

if __name__ == "__main__":
    download_nltk_resources()