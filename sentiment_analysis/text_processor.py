"""
Módulo de processamento de texto para análise de sentimento
"""

import re
from .dictionaries import NEGATION_WORDS, NEGATION_BREAKERS, INTENSIFIERS


def preprocess_text(text):
    """Limpa e preprocessa o texto preservando estrutura para negação"""
    # Converte para minúsculas
    text = text.lower()

    # Preserva pontuação importante para contexto
    # Remove apenas pontuação excessiva, mantendo estrutura
    text = re.sub(r"[^\w\s\.\!\?]", " ", text)
    text = re.sub(r"\.{2,}", ".", text)
    text = re.sub(r"\!{2,}", "!", text)
    text = re.sub(r"\?{2,}", "?", text)

    # Remove espaços extras
    text = re.sub(r"\s+", " ", text).strip()

    # Divide em palavras preservando pontuação
    words = text.split()

    # Remove palavras muito curtas, exceto negações importantes
    filtered_words = []
    for word in words:
        # Remove pontuação das palavras mas mantém a palavra
        clean_word = re.sub(r"[^\w]", "", word)
        if len(clean_word) > 2 or clean_word in NEGATION_WORDS:
            filtered_words.append(clean_word)

    return filtered_words


def analyze_with_context(words):
    """Analisa palavras considerando negação e intensificadores"""
    result = []
    i = 0

    while i < len(words):
        word = words[i]
        is_negated = False
        intensifier = 1.0

        # Verifica intensificador na palavra anterior
        if i > 0 and words[i - 1] in INTENSIFIERS:
            intensifier = INTENSIFIERS[words[i - 1]]

        # Verifica negação nas 2-3 palavras anteriores
        negation_window = max(0, i - 3)
        for j in range(negation_window, i):
            if words[j] in NEGATION_WORDS:
                is_negated = True
            elif words[j] in NEGATION_BREAKERS:
                is_negated = False  # Quebra a negação

        result.append((word, is_negated, intensifier))
        i += 1

    return result
