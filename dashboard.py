"""
Dashboard Streamlit Modularizado para Monitoramento de Percepção Pública sobre IA no Piauí
"""

import streamlit as st
import sys
import os

# Adiciona o diretório raiz ao path para importações
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importações dos módulos criados
from dashboard.config import PAGE_CONFIG, CUSTOM_CSS
from dashboard.data_utils import load_data, apply_filters
from dashboard.sentiment import analyze_sentiments
from dashboard.components.sidebar import render_sidebar
from dashboard.components.interface import (
    render_header,
    render_metrics,
    render_main_visualizations,
    render_timeline_chart,
    render_secondary_charts,
    render_data_table,
    render_detailed_statistics,
    render_limitations_info,
    render_footer,
)
from dashboard.visualizations import charts


def main():
    """Função principal do dashboard"""

    # Configuração da página
    st.set_page_config(**PAGE_CONFIG)

    # CSS customizado
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # Header
    render_header()

    # Carrega e analisa dados
    df = load_data()

    if df.empty:
        st.warning(
            "⚠️ Nenhum dado encontrado. Clique em 'Coletar Novas Notícias' para começar."
        )
        # Renderiza sidebar mesmo sem dados para permitir coleta
        render_sidebar(df, df)
        return

    # Analisa sentimentos
    df_analyzed = analyze_sentiments(df)

    # Renderiza sidebar e obtém filtros
    filters = render_sidebar(df, df_analyzed)

    # Aplica filtros
    df_filtered = apply_filters(
        df_analyzed,
        filters["sentimento"],
        filters["termo"],
        filters["data"],
        filters["min_confidence"],
    )

    # Métricas principais
    render_metrics(df_filtered)

    # Visualizações principais
    render_main_visualizations(df_filtered, charts)

    # Gráfico temporal
    render_timeline_chart(df_filtered, charts)

    # Gráficos secundários
    render_secondary_charts(df_filtered, charts)

    # Tabela de dados
    render_data_table(df_filtered, filters["show_confidence"])

    # Estatísticas detalhadas
    render_detailed_statistics(df_filtered)

    # Informações sobre limitações
    render_limitations_info()

    # Footer
    render_footer()


if __name__ == "__main__":
    main()
