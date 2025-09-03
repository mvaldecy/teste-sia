"""
Classe principal do analisador de sentimento

NOTA: Algoritmos de classificação e cálculo de confiança
desenvolvidos com assistência de IA, adaptados para o contexto específico.
"""

from collections import Counter
from .dictionaries import POSITIVE_WORDS, NEGATIVE_WORDS, NEUTRAL_WORDS
from .text_processor import preprocess_text, analyze_with_context
from .confidence import calculate_improved_confidence, calculate_neutral_confidence


class SentimentAnalyzer:
    """Analisador de sentimento baseado em regras com tratamento avançado"""

    def __init__(self):
        """Inicializa o analisador"""
        pass

    def calculate_sentiment_score(self, words_with_context):
        """Calcula score considerando negação e intensificadores"""
        positive_score = 0
        negative_score = 0
        positive_words = []
        negative_words = []

        for word, is_negated, intensifier in words_with_context:
            base_positive_weight = POSITIVE_WORDS.get(word, 0)
            base_negative_weight = NEGATIVE_WORDS.get(word, 0)

            # Aplica intensificador
            positive_weight = base_positive_weight * intensifier
            negative_weight = base_negative_weight * intensifier

            # Aplica negação (inverte o sentimento)
            if is_negated:
                if positive_weight > 0:
                    # Palavra positiva negada vira negativa
                    negative_score += positive_weight
                    negative_words.append(f"não_{word}")
                elif negative_weight > 0:
                    # Palavra negativa negada vira positiva
                    positive_score += negative_weight
                    positive_words.append(f"não_{word}")
            else:
                # Sem negação, aplica normalmente
                if positive_weight > 0:
                    positive_score += positive_weight
                    if intensifier > 1.0:
                        positive_words.append(f"muito_{word}")
                    else:
                        positive_words.append(word)
                elif negative_weight > 0:
                    negative_score += negative_weight
                    if intensifier > 1.0:
                        negative_words.append(f"muito_{word}")
                    else:
                        negative_words.append(word)

        return positive_score, negative_score, positive_words, negative_words

    def analyze_sentiment(self, text):
        """Analisa o sentimento do texto com cálculo melhorado de confiança"""
        words = preprocess_text(text)

        if not words:
            return (
                "neutro",
                0.1,
                {
                    "positivas": [],
                    "negativas": [],
                    "total_palavras": 0,
                    "palavras_sentimento": 0,
                    "peso_positivo": 0,
                    "peso_negativo": 0,
                    "negacoes_detectadas": 0,
                    "intensificadores_detectados": 0,
                },
            )

        # Analisa com contexto (negação e intensificadores)
        words_with_context = analyze_with_context(words)

        # Calcula scores considerando contexto
        positive_score, negative_score, positive_words, negative_words = (
            self.calculate_sentiment_score(words_with_context)
        )

        # Conta detecções especiais
        negations_count = sum(
            1 for _, is_negated, _ in words_with_context if is_negated
        )
        intensifiers_count = sum(
            1 for _, _, intensifier in words_with_context if intensifier != 1.0
        )

        positive_count = len(positive_words)
        negative_count = len(negative_words)

        # Determina sentimento baseado no score total
        if positive_score == 0 and negative_score == 0:
            sentiment = "neutro"
            # Confiança baseada no tamanho do texto e palavras técnicas
            confidence = calculate_neutral_confidence(words)
        elif positive_score > negative_score:
            sentiment = "positivo"
            confidence = calculate_improved_confidence(
                positive_count,
                negative_count,
                positive_score,
                negative_score,
                len(words),
            )
        elif negative_score > positive_score:
            sentiment = "negativo"
            confidence = calculate_improved_confidence(
                positive_count,
                negative_count,
                positive_score,
                negative_score,
                len(words),
            )
        else:
            # Empate nos scores - neutralidade por equilíbrio
            sentiment = "neutro"
            confidence = 0.4 + min(len(words) / 50, 0.2)  # 0.4 a 0.6 baseado no tamanho

        details = {
            "positivas": list(set(positive_words)),
            "negativas": list(set(negative_words)),
            "total_palavras": len(words),
            "palavras_sentimento": positive_count + negative_count,
            "peso_positivo": round(positive_score, 2),
            "peso_negativo": round(negative_score, 2),
            "negacoes_detectadas": negations_count,
            "intensificadores_detectados": intensifiers_count,
        }

        return sentiment, confidence, details

    def analyze_batch(self, texts):
        """Analisa uma lista de textos"""
        results = []

        for i, text in enumerate(texts):
            sentiment, confidence, details = self.analyze_sentiment(text)

            result = {
                "index": i,
                "text": text,
                "sentiment": sentiment,
                "confidence": confidence,
                "details": details,
            }

            results.append(result)

        return results

    def get_sentiment_stats(self, results):
        """Calcula estatísticas dos sentimentos"""
        sentiments = [r["sentiment"] for r in results]
        sentiment_counts = Counter(sentiments)

        total = len(sentiments)
        stats = {
            "total": total,
            "counts": dict(sentiment_counts),
            "percentages": {
                sentiment: (count / total) * 100
                for sentiment, count in sentiment_counts.items()
            },
        }

        return stats

    def get_word_frequency(self, results, min_length=4):
        """Obtém a frequência de palavras dos textos analisados"""
        all_words = []

        for result in results:
            words = preprocess_text(result["text"])
            # Filtra palavras muito comuns ou neutras
            filtered_words = [
                word
                for word in words
                if len(word) >= min_length
                and word not in NEUTRAL_WORDS
                and word
                not in {"para", "com", "uma", "como", "mais", "ser", "ter", "fazer"}
            ]
            all_words.extend(filtered_words)

        return Counter(all_words)
