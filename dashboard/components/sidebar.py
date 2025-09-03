"""
Componentes da sidebar do dashboard
"""

import streamlit as st
from datetime import datetime
import sys
import os

# Adiciona path para importações
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from news_collector import NewsCollector


def get_date_range_local(df):
    """Obtém intervalo de datas para os filtros (versão local)"""
    try:
        import pandas as pd
        from datetime import datetime, timedelta

        # Tenta usar data de publicação primeiro
        df["data_publicacao_dt"] = pd.to_datetime(
            df["data_publicacao"], errors="coerce"
        )

        # Filtra datas válidas
        hoje = datetime.now()
        um_ano_atras = hoje - timedelta(days=365)
        um_mes_no_futuro = hoje + timedelta(days=30)

        datas_validas = df[
            (df["data_publicacao_dt"] >= um_ano_atras)
            & (df["data_publicacao_dt"] <= um_mes_no_futuro)
            & df["data_publicacao_dt"].notna()
        ]

        if not datas_validas.empty:
            data_min = datas_validas["data_publicacao_dt"].min().date()
            data_max = datas_validas["data_publicacao_dt"].max().date()
        else:
            # Fallback para data de coleta
            df["data_coleta_dt"] = pd.to_datetime(df["data_coleta"])
            data_min = df["data_coleta_dt"].min().date()
            data_max = df["data_coleta_dt"].max().date()

        return data_min, data_max

    except Exception:
        # Fallback para hoje
        hoje = datetime.now().date()
        return hoje, hoje


def render_data_collection_controls():
    """Renderiza controles de coleta de dados"""
    st.header("⚙️ Controles")

    # Botão para coletar novas notícias
    if st.button("🔄 Coletar Novas Notícias"):
        with st.spinner("Coletando notícias..."):
            collector = NewsCollector()
            news_data = collector.collect_all_news(max_per_term=4)

            if news_data:
                collector.save_to_csv(news_data)
                st.success(f"✅ {len(news_data)} notícias coletadas!")
                st.rerun()
            else:
                st.error("❌ Nenhuma notícia foi coletada")

    st.markdown("---")


def render_download_controls(df_analyzed):
    """Renderiza controles de download"""
    if not df_analyzed.empty:
        csv_data = df_analyzed.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f"analise_ia_piaui_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )
        st.markdown("---")


def render_filters(df, df_analyzed):
    """Renderiza todos os filtros da sidebar"""
    st.subheader("🔍 Filtros")

    # Filtro por sentimento
    sentimentos_disponiveis = (
        ["Todos"] + list(df_analyzed["sentimento"].unique())
        if not df_analyzed.empty
        else ["Todos"]
    )
    filtro_sentimento = st.selectbox("Filtrar por sentimento:", sentimentos_disponiveis)

    # Filtro por termo de busca
    termos_disponiveis = (
        ["Todos"] + list(df["termo_busca"].unique()) if not df.empty else ["Todos"]
    )
    filtro_termo = st.selectbox("Filtrar por termo:", termos_disponiveis)

    # Controles de confiança
    show_confidence = st.checkbox("Mostrar confiança da análise", value=True)
    min_confidence = st.slider("Confiança mínima", 0.0, 1.0, 0.0, 0.1)

    # Filtro por data
    if not df.empty:
        data_min, data_max = get_date_range_local(df)
        filtro_data = st.date_input(
            "Filtrar por período:",
            value=(data_min, data_max),
            min_value=data_min,
            max_value=data_max,
        )
    else:
        filtro_data = ()

    return {
        "sentimento": filtro_sentimento,
        "termo": filtro_termo,
        "data": filtro_data,
        "show_confidence": show_confidence,
        "min_confidence": min_confidence,
    }


def render_sidebar(df, df_analyzed):
    """Renderiza toda a sidebar"""
    with st.sidebar:
        render_data_collection_controls()

        if not df_analyzed.empty:
            render_download_controls(df_analyzed)

        filters = render_filters(df, df_analyzed)

    return filters
