"""
Funções para criar visualizações do dashboard
"""

import plotly.express as px
import plotly.graph_objects as go
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
    """Cria gráfico de frequência de palavras (consistente em todos os ambientes)"""
    if df.empty:
        return None

    # Combina todos os textos
    all_text = " ".join(df["texto_completo"].astype(str))

    # Limpa o texto
    clean_text = clean_text_pipeline(all_text)

    if not clean_text.strip():
        return None

    # Sempre usa o gráfico de barras para consistência
    return create_word_frequency_chart(clean_text)


def create_word_frequency_chart(text):
    """Cria gráfico de barras com palavras mais frequentes"""
    from collections import Counter
    import re
    
    # Separa palavras e conta frequência
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Remove palavras muito pequenas
    words = [word for word in words if len(word) > 3]
    
    # Conta frequência
    word_freq = Counter(words)
    
    # Pega as 15 palavras mais comuns
    top_words = word_freq.most_common(15)
    
    if not top_words:
        return None
    
    # Cria o gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    
    words_list = [item[0] for item in top_words]
    counts_list = [item[1] for item in top_words]
    
    # Cores gradientes
    colors = plt.cm.viridis([i/len(words_list) for i in range(len(words_list))])
    
    bars = ax.barh(range(len(words_list)), counts_list, color=colors)
    
    # Configurações do gráfico
    ax.set_yticks(range(len(words_list)))
    ax.set_yticklabels(words_list)
    ax.set_xlabel('Frequência')
    ax.set_title('Termos Mais Frequentes nas Notícias', fontsize=14, pad=20)
    
    # Inverte eixo Y para mostrar maior frequência no topo
    ax.invert_yaxis()
    
    # Adiciona valores nas barras
    for i, (bar, count) in enumerate(zip(bars, counts_list)):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                str(count), ha='left', va='center', fontsize=10)
    
    # Remove spines desnecessárias
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
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
