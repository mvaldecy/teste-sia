"""
Visualizações do Dashboard

Este módulo contém todas as funções para criação de gráficos e visualizações:
- Gráfico de pizza dos sentimentos
- Nuvem de palavras
- Gráfico temporal (colunas)
- Distribuição por termo de busca
- Histograma de confiança

Todas as visualizações usam Plotly para interatividade e matplotlib para
componentes específicos como word cloud.
"""

from .charts import (
    create_sentiment_pie_chart,
    create_wordcloud,
    create_term_distribution_chart,
    create_confidence_histogram,
    create_timeline_chart,
)

__all__ = [
    "create_sentiment_pie_chart",
    "create_wordcloud",
    "create_term_distribution_chart",
    "create_confidence_histogram",
    "create_timeline_chart",
]
