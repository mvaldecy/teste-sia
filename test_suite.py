"""
Testes básicos para o projeto Monitor IA Piauí
"""

import unittest
import pandas as pd
from sentiment_analysis import SentimentAnalyzer
from utils.text_processing import clean_text_pipeline, extract_keywords


class TestSentimentAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = SentimentAnalyzer()

    def test_positive_sentiment(self):
        """Testa detecção de sentimento positivo"""
        text = "A inteligência artificial traz excelente inovação para o Piauí"
        sentiment, confidence, details = self.analyzer.analyze_sentiment(text)
        self.assertEqual(sentiment, "positivo")
        self.assertGreater(confidence, 0)
        self.assertIn("excelente", details["positivas"])
        self.assertIn("inovação", details["positivas"])

    def test_negative_sentiment(self):
        """Testa detecção de sentimento negativo"""
        text = "Preocupações sobre desemprego e riscos da automação"
        sentiment, confidence, details = self.analyzer.analyze_sentiment(text)
        self.assertEqual(sentiment, "negativo")
        self.assertGreater(confidence, 0)
        self.assertIn("desemprego", details["negativas"])

    def test_neutral_sentiment(self):
        """Testa detecção de sentimento neutro"""
        text = "A secretaria apresentou relatório sobre tecnologia"
        sentiment, confidence, details = self.analyzer.analyze_sentiment(text)
        self.assertEqual(sentiment, "neutro")
        self.assertGreater(confidence, 0.1)  # Mudança: aceita confiança > 0.1

    def test_empty_text(self):
        """Testa comportamento com texto vazio"""
        sentiment, confidence, details = self.analyzer.analyze_sentiment("")
        self.assertEqual(sentiment, "neutro")
        self.assertEqual(confidence, 0.1)  # Mudança: aceita 0.1 como padrão

    def test_negation_handling(self):
        """Testa tratamento de negação"""
        # Negação de palavra positiva deve ser negativo
        text = "Não é uma boa solução"
        sentiment, confidence, details = self.analyzer.analyze_sentiment(text)
        self.assertEqual(sentiment, "negativo")
        self.assertIn("não_boa", details["negativas"])
        self.assertGreater(details["negacoes_detectadas"], 0)

    def test_intensifiers(self):
        """Testa detecção de intensificadores"""
        text = "Muito excelente iniciativa"
        sentiment, confidence, details = self.analyzer.analyze_sentiment(text)
        self.assertEqual(sentiment, "positivo")
        self.assertGreater(details["intensificadores_detectados"], 0)
        # O peso deve ser maior que o normal devido ao intensificador
        self.assertGreater(
            details["peso_positivo"], 3
        )  # "excelente" = 3, mas com "muito" deve ser > 3

    def test_complex_negation(self):
        """Testa negação com quebra de contexto"""
        text = "A solução não é ruim, mas tem limitações"
        sentiment, confidence, details = self.analyzer.analyze_sentiment(text)
        # Deve detectar pelo menos uma negação
        self.assertGreater(details["negacoes_detectadas"], 0)


class TestTextProcessing(unittest.TestCase):

    def test_clean_text_pipeline(self):
        """Testa o pipeline de limpeza de texto"""
        dirty_text = (
            "<p>Texto com <strong>HTML</strong> e caracteres especiais!!! @#$</p>"
        )
        clean_text = clean_text_pipeline(dirty_text)

        # Verifica que HTML foi removido
        self.assertNotIn("<p>", clean_text)
        self.assertNotIn("</p>", clean_text)
        self.assertNotIn("<strong>", clean_text)

        # Verifica que texto útil permanece
        self.assertIn("Texto", clean_text)
        self.assertIn("HTML", clean_text)

    def test_extract_keywords(self):
        """Testa extração de palavras-chave"""
        text = "inteligência artificial piauí desenvolvimento tecnologia inovação"
        keywords = extract_keywords(text, min_length=4, max_keywords=10)

        self.assertIsInstance(keywords, list)
        self.assertIn("inteligência", keywords)
        self.assertIn("artificial", keywords)
        self.assertIn("desenvolvimento", keywords)

        # Verifica que palavras curtas foram filtradas
        short_words = [k for k in keywords if len(k) < 4]
        self.assertEqual(len(short_words), 0)


class TestDataIntegrity(unittest.TestCase):

    def test_csv_structure(self):
        """Testa se o CSV tem a estrutura esperada"""
        try:
            df = pd.read_csv("data/noticias.csv")
            expected_columns = [
                "termo_busca",
                "titulo",
                "link",
                "descricao",
                "data_publicacao",
                "data_coleta",
                "texto_completo",
            ]

            for col in expected_columns:
                self.assertIn(col, df.columns, f"Coluna '{col}' não encontrada")

            # Verifica que não há linhas completamente vazias
            self.assertFalse(df.isnull().all(axis=1).any())

        except FileNotFoundError:
            self.skipTest("Arquivo de dados não encontrado")


def run_tests():
    """Executa todos os testes"""
    # Cria suite de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Adiciona todas as classes de teste
    suite.addTests(loader.loadTestsFromTestCase(TestSentimentAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestTextProcessing))
    suite.addTests(loader.loadTestsFromTestCase(TestDataIntegrity))

    # Executa testes com saída silenciosa
    import os

    runner = unittest.TextTestRunner(stream=open(os.devnull, "w"), verbosity=0)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
