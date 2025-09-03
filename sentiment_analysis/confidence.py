"""
Módulo de cálculo de confiança para análise de sentimento
"""


def calculate_improved_confidence(
    positive_count,
    negative_count,
    positive_weight,
    negative_weight,
    total_words,
):
    """Calcula confiança melhorada considerando pesos e densidade"""

    # Se não há palavras de sentimento, confiança baixa
    if positive_count == 0 and negative_count == 0:
        return 0.1

    # Calcula densidade de sentimento (palavras de sentimento / total)
    sentiment_words_count = positive_count + negative_count
    sentiment_density = sentiment_words_count / max(total_words, 1)

    # Calcula força total do sentimento
    total_weight = positive_weight + negative_weight
    dominant_weight = max(positive_weight, negative_weight)

    # Confiança base mais conservadora (0.35 a 0.65)
    if total_weight > 0:
        weight_ratio = dominant_weight / total_weight
        # Mapeia de 0.5-1.0 para 0.35-0.65
        base_confidence = 0.35 + (weight_ratio - 0.5) * 0.6
    else:
        base_confidence = 0.35

    # Bônus por densidade (0 a 0.15)
    density_bonus = min(sentiment_density * 0.3, 0.15)

    # Bônus por força das palavras (0 a 0.1)
    if sentiment_words_count > 0:
        avg_weight = total_weight / sentiment_words_count
        weight_bonus = min((avg_weight - 1) * 0.05, 0.1)
    else:
        weight_bonus = 0

    # Bônus por clareza (0 a 0.1)
    if total_weight > 0:
        clarity = abs(positive_weight - negative_weight) / total_weight
        clarity_bonus = clarity * 0.1
    else:
        clarity_bonus = 0

    # Confiança final
    final_confidence = base_confidence + density_bonus + weight_bonus + clarity_bonus

    # Garante que está entre 0.2 e 0.85
    return max(0.2, min(final_confidence, 0.85))


def calculate_neutral_confidence(words):
    """Calcula confiança para textos neutros baseado em características do texto"""
    if not words:
        return 0.1

    word_count = len(words)

    # Palavras técnicas/neutras que indicam texto informativo (mais confiança na neutralidade)
    technical_words = {
        "sistema",
        "tecnologia",
        "projeto",
        "dados",
        "informação",
        "relatório",
        "apresenta",
        "desenvolve",
        "implementa",
        "utiliza",
        "funciona",
        "processo",
        "método",
        "análise",
        "estudo",
        "pesquisa",
        "resultado",
        "modelo",
        "algoritmo",
        "software",
        "hardware",
        "digital",
        "eletrônico",
        "computacional",
        "secretaria",
        "governo",
        "estado",
        "municipal",
        "público",
        "serviço",
        "piauí",
        "brasil",
        "nacional",
        "federal",
        "estadual",
        "regional",
    }

    # Conta palavras técnicas
    technical_count = sum(1 for word in words if word in technical_words)
    technical_ratio = technical_count / word_count

    # Confiança base por tamanho do texto
    if word_count < 3:
        base_confidence = 0.15  # Texto muito curto
    elif word_count < 8:
        base_confidence = 0.25  # Texto curto
    elif word_count < 15:
        base_confidence = 0.35  # Texto médio
    else:
        base_confidence = 0.45  # Texto longo

    # Bônus por conteúdo técnico/informativo
    technical_bonus = min(technical_ratio * 0.3, 0.25)

    # Confiança final para neutros
    final_confidence = base_confidence + technical_bonus

    # Entre 0.15 e 0.7 para neutros
    return max(0.15, min(final_confidence, 0.7))
