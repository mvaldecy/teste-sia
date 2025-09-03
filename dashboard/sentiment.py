"""
Módulo de análise de sentimento para o dashboard
"""

import pandas as pd
import streamlit as st
from sentiment_analysis import SentimentAnalyzer


@st.cache_data
def analyze_sentiments(df):
    """Analisa sentimentos dos textos no DataFrame"""
    if df.empty:
        return df

    analyzer = SentimentAnalyzer()

    # Analisa sentimento do texto completo
    sentiments = []
    confidences = []
    positive_words = []
    negative_words = []

    for text in df["texto_completo"]:
        sentiment, confidence, details = analyzer.analyze_sentiment(str(text))
        sentiments.append(sentiment)
        confidences.append(confidence)
        positive_words.append(", ".join(details["positivas"]))
        negative_words.append(", ".join(details["negativas"]))

    # Adiciona colunas de análise
    df_analyzed = df.copy()
    df_analyzed["sentimento"] = sentiments
    df_analyzed["confianca"] = confidences
    df_analyzed["palavras_positivas"] = positive_words
    df_analyzed["palavras_negativas"] = negative_words

    return df_analyzed
