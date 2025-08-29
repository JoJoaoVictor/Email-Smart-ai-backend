"""
Constantes e listas utilizadas na aplicação
"""

# Tipos MIME suportados
ALLOWED_FILE_TYPES = {
    'application/pdf': '.pdf',
    'text/plain': '.txt',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
    'application/msword': '.doc',
    'text/html': '.html',
    'application/rtf': '.rtf'
}

# Palavras-chave para classificação
PRODUCTIVE_KEYWORDS = [
    'suporte', 'problema', 'ajuda', 'erro', 'solicitação', 'atualização', 
    'dúvida', 'sistema', 'urgente', 'cliente', 'contrato', 'proposta', 
    'reunião', 'relatório', 'orçamento', 'prazo', 'projeto', 'tarefa',
    'bug', 'falha', 'pedido', 'requisição', 'necessário', 'importante'
]

UNPRODUCTIVE_KEYWORDS = [
    'obrigado', 'agradeço', 'parabéns', 'feliz', 'natal', 'ano novo',
    'comemoração', 'festa', 'férias', 'almoço', 'jantar', 'convite',
    'social', 'pessoal', 'aniversário', 'casamento', 'feriado',
    'descanso', 'diversão', 'lazer'
]

# Pesos para palavras-chave
KEYWORD_WEIGHTS = {
    'reunião': 2.0, 'projeto': 1.8, 'prazo': 1.7, 'entreg': 1.6,
    'trabalho': 1.5, 'urgente': 1.8, 'contrato': 1.7, 'cliente': 1.6,
    'fest': 1.8, 'festa': 1.8, 'social': 1.5, 'pessoal': 1.4
}