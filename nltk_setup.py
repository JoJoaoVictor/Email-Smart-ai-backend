import nltk
import os

print("🚀 Configurando NLTK...")

# Tenta baixar recursos, mas não é crítico se falhar
try:
    nltk.download('stopwords', quiet=True)
    print("✅ stopwords configurado")
except:
    print("⚠️  stopwords não disponível (usando fallback)")

try:
    nltk.download('punkt', quiet=True)
    print("✅ punkt configurado")
except:
    print("⚠️  punkt não disponível (usando tokenização alternativa)")

print("🎉 Configuração concluída - aplicação pode iniciar")