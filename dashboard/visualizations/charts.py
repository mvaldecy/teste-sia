"""
Funções para criar visualizações do dashboard
"""

import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
from datetime import datetime, timedelta

# Adiciona path para importações
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.text_processing import clean_text_pipeline

# Configurações locais
COLORS = {"positivo": "#27AE60", "negativo": "#E74C3C", "neutro": "#95A5A6"}

WORDCLOUD_CONFIG = {
    "width": 800,
    "height": 400,
    "background_color": "white",
    "colormap": "viridis",
    "max_words": 50,
    "relative_scaling": 0.5,
    "min_font_size": 10,
}


def validate_dates_local(df, date_column="data_publicacao"):
    """Valida datas localmente"""
    try:
        df[f"{date_column}_dt"] = pd.to_datetime(df[date_column], errors="coerce")

        hoje = datetime.now()
        limite_passado = hoje - timedelta(days=365)
        limite_futuro = hoje + timedelta(days=30)

        df_valid = df[
            (df[f"{date_column}_dt"] >= limite_passado)
            & (df[f"{date_column}_dt"] <= limite_futuro)
            & df[f"{date_column}_dt"].notna()
        ].copy()

        return df_valid

    except Exception:
        return pd.DataFrame()


def create_sentiment_pie_chart(df):
    """Cria gráfico de pizza dos sentimentos"""
    if df.empty:
        return None

    sentiment_counts = df["sentimento"].value_counts()

    fig = px.pie(
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        title="Distribuição de Sentimentos",
        color=sentiment_counts.index,
        color_discrete_map=COLORS,
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Quantidade: %{value}<br>Percentual: %{percent}<extra></extra>",
    )

    fig.update_layout(showlegend=True, title_x=0.5, font_size=14)

    return fig


def create_wordcloud(df):
    """Cria nuvem de palavras"""
    if df.empty:
        return None

    # Combina todos os textos
    all_text = " ".join(df["texto_completo"].astype(str))

    # Limpa o texto
    clean_text = clean_text_pipeline(all_text)

    if not clean_text.strip():
        return None

    # Cria a word cloud
    wordcloud = WordCloud(**WORDCLOUD_CONFIG).generate(clean_text)

    # Cria o plot
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    ax.set_title("Termos Mais Frequentes", fontsize=16, pad=20)

    return fig


def create_term_distribution_chart(df):
    """Cria gráfico de barras da distribuição por termo de busca"""
    if df.empty:
        return None

    term_sentiment = (
        df.groupby(["termo_busca", "sentimento"]).size().reset_index(name="count")
    )

    fig = px.bar(
        term_sentiment,
        x="termo_busca",
        y="count",
        color="sentimento",
        title="Distribuição de Sentimentos por Termo de Busca",
        color_discrete_map=COLORS,
    )

    fig.update_layout(
        xaxis_title="Termo de Busca",
        yaxis_title="Número de Notícias",
        title_x=0.5,
        xaxis_tickangle=45,
    )

    return fig


def create_confidence_histogram(df):
    """Cria histograma da distribuição de confiança"""
    if df.empty:
        return None

    fig = px.histogram(
        df,
        x="confianca",
        color="sentimento",
        title="Distribuição da Confiança da Análise",
        nbins=20,
        color_discrete_map=COLORS,
    )

    fig.update_layout(xaxis_title="Confiança", yaxis_title="Frequência", title_x=0.5)

    return fig


def create_timeline_chart(df):
    """Cria gráfico de colunas temporal"""
    if df.empty:
        return None

    try:
        # Valida e usa datas de publicação
        df_valid = validate_dates_local(df, "data_publicacao")

        if not df_valid.empty:
            df_valid["data"] = df_valid["data_publicacao_dt"].dt.date
            timeline_data = (
                df_valid.groupby(["data", "sentimento"])
                .size()
                .reset_index(name="count")
            )
        else:
            # Fallback para data de coleta
            df["data_coleta_dt"] = pd.to_datetime(df["data_coleta"])
            df["data"] = df["data_coleta_dt"].dt.date
            timeline_data = (
                df.groupby(["data", "sentimento"]).size().reset_index(name="count")
            )

    except Exception:
        # Em caso de erro, use data de coleta como fallback
        df["data_coleta_dt"] = pd.to_datetime(df["data_coleta"])
        df["data"] = df["data_coleta_dt"].dt.date
        timeline_data = (
            df.groupby(["data", "sentimento"]).size().reset_index(name="count")
        )

    # Cria gráfico de colunas
    fig = px.bar(
        timeline_data,
        x="data",
        y="count",
        color="sentimento",
        title="Evolução dos Sentimentos ao Longo do Tempo",
        color_discrete_map=COLORS,
        barmode="group",  # Barras agrupadas lado a lado
    )

    # Configura o layout para começar do zero
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Número de Notícias",
        title_x=0.5,
        yaxis=dict(
            rangemode="tozero",  # Força o eixo Y a começar do zero
            showgrid=True,
            gridwidth=1,
            gridcolor="rgba(128,128,128,0.2)",
        ),
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor="rgba(128,128,128,0.2)"),
    )

    return fig
