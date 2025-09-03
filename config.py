# Configurações do Monitor IA Piauí

# Configurações de coleta
MAX_NOTICIAS_POR_TERMO = 5
INTERVALO_ENTRE_REQUISICOES = 1  # segundos
TIMEOUT_REQUISICAO = 15  # segundos

# Configurações de análise de sentimento
CONFIANCA_MINIMA_PADRAO = 0.0
PALAVRAS_MINIMAS_NUVEM = 4
MAX_PALAVRAS_NUVEM = 50

# Configurações do dashboard
PORTA_STREAMLIT = 8502
TEMA_CORES = {"positivo": "#27AE60", "negativo": "#E74C3C", "neutro": "#95A5A6"}

# Termos de busca (podem ser modificados conforme necessário)
TERMOS_BUSCA = [
    "Inteligência Artificial Piauí",
    "SIA Piauí",
    "IA Piauí",
    "Artificial Intelligence Piauí",
    "Secretaria Inteligência Artificial Piauí",
    "SoberanIA Piauí",
]

# Configurações de cache
CACHE_EXPIRY_HOURS = 1
