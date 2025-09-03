"""
Componentes da interface principal

NOTA: Layout, estrutura visual e configurações dos componentes
desenvolvidos com assistência de IA para acelerar a prototipagem.
"""

import streamlit as st
import pandas as pd


def render_header():
    """Renderiza o cabeçalho do dashboard"""
    st.markdown(
        """
    <div class="main-header">
        <h1>🧠 Monitor de Percepção Pública sobre IA no Piauí</h1>
        <p>Análise de sentimento em notícias sobre Inteligência Artificial</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_metrics(df_filtered):
    """Renderiza as métricas principais"""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📰 Total de Notícias", len(df_filtered))

    with col2:
        positivas = len(df_filtered[df_filtered["sentimento"] == "positivo"])
        st.metric("😊 Notícias Positivas", positivas)

    with col3:
        negativas = len(df_filtered[df_filtered["sentimento"] == "negativo"])
        st.metric("😟 Notícias Negativas", negativas)

    with col4:
        neutras = len(df_filtered[df_filtered["sentimento"] == "neutro"])
        st.metric("😐 Notícias Neutras", neutras)


def render_main_visualizations(df_filtered, charts):
    """Renderiza as visualizações principais"""
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📊 Distribuição de Sentimentos")
        pie_chart = charts.create_sentiment_pie_chart(df_filtered)
        if pie_chart:
            st.plotly_chart(pie_chart, use_container_width=True)

    with col2:
        st.subheader("📊 Palavras Mais Frequentes")
        wordcloud_fig = charts.create_wordcloud(df_filtered)
        if wordcloud_fig:
            st.pyplot(wordcloud_fig)
        else:
            st.info("Não há dados suficientes para gerar a análise de palavras")


def render_timeline_chart(df_filtered, charts):
    """Renderiza o gráfico temporal"""
    if len(df_filtered) > 1:
        st.subheader("📈 Evolução Temporal")
        timeline_chart = charts.create_timeline_chart(df_filtered)
        if timeline_chart:
            st.plotly_chart(timeline_chart, use_container_width=True)


def render_secondary_charts(df_filtered, charts):
    """Renderiza gráficos secundários"""
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📊 Distribuição por Termo")
        term_chart = charts.create_term_distribution_chart(df_filtered)
        if term_chart:
            st.plotly_chart(term_chart, use_container_width=True)

    with col2:
        st.subheader("📈 Distribuição de Confiança")
        confidence_chart = charts.create_confidence_histogram(df_filtered)
        if confidence_chart:
            st.plotly_chart(confidence_chart, use_container_width=True)


def render_data_table(df_filtered, show_confidence):
    """Renderiza a tabela de dados"""
    st.subheader("📋 Dados Coletados")

    if show_confidence:
        st.info(
            "💡 **Dica:** A coluna 'Confiança' mostra o quão certeza o sistema tem da classificação (0% = incerto, 100% = muito certeza)"
        )

    # Preparar dados para exibição
    display_df = df_filtered.copy()
    display_df["data_publicacao"] = pd.to_datetime(
        display_df["data_publicacao"]
    ).dt.strftime("%d/%m/%Y %H:%M")

    # Truncar títulos muito longos para melhor visualização
    display_df["titulo_truncado"] = display_df["titulo"].apply(
        lambda x: x[:80] + "..." if len(x) > 80 else x
    )

    columns_to_show = [
        "titulo_truncado",
        "link",
        "sentimento",
        "termo_busca",
        "data_publicacao",
    ]
    if show_confidence:
        columns_to_show.insert(3, "confianca")

    # Renomear colunas para exibição
    display_columns = {
        "titulo_truncado": "Título",
        "link": "🔗 Link",
        "sentimento": "Sentimento",
        "confianca": "Confiança",
        "termo_busca": "Termo",
        "data_publicacao": "Data",
    }

    table_df = display_df[columns_to_show].rename(columns=display_columns)

    # Configuração das colunas
    column_config = {
        "🔗 Link": st.column_config.LinkColumn(
            "🔗 Link", help="Clique para acessar a notícia completa", width="small"
        ),
        "Título": st.column_config.TextColumn(
            "Título", width="large", help="Título da notícia"
        ),
        "Sentimento": st.column_config.TextColumn("Sentimento", width="small"),
        "Termo": st.column_config.TextColumn("Termo", width="small"),
        "Data": st.column_config.TextColumn("Data", width="medium"),
    }

    if show_confidence:
        column_config["Confiança"] = st.column_config.NumberColumn(
            "Confiança",
            help="Nível de confiança da análise de sentimento",
            min_value=0,
            max_value=1,
            format="%.2f",
            width="small",
        )

    # Exibir tabela com hyperlinks clicáveis
    st.dataframe(
        table_df,
        use_container_width=True,
        hide_index=True,
        column_config=column_config,
        height=400,
    )

    # Estatísticas resumidas da tabela
    st.caption(
        f"📊 Exibindo {len(table_df)} notícias de um total de {len(df_filtered)} após aplicar filtros."
    )


def render_detailed_statistics(df_filtered):
    """Renderiza estatísticas detalhadas"""
    with st.expander("📊 Estatísticas Detalhadas"):
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Distribuição por Termo de Busca:**")
            term_counts = df_filtered["termo_busca"].value_counts()
            st.bar_chart(term_counts)

        with col2:
            st.write("**Confiança Média por Sentimento:**")
            confidence_stats = (
                df_filtered.groupby("sentimento")["confianca"]
                .agg(["mean", "count"])
                .round(3)
            )
            confidence_stats.columns = ["Confiança Média", "Quantidade de Notícias"]
            confidence_stats.index.name = "Sentimento"
            st.dataframe(confidence_stats)

            st.info(
                """
            **💡 Confiança Média** indica o quão certeza o sistema tem:
            
            • **0.0-0.3**: Baixa confiança
            • **0.3-0.6**: Confiança moderada  
            • **0.6-1.0**: Alta confiança
            
            **Como funciona:** Conta palavras de sentimento e divide pelo total de palavras.
            """
            )


def render_limitations_info():
    """Renderiza informações sobre limitações"""
    st.warning("⚠️ **Sobre a Análise de Sentimento**")

    with st.expander("📖 Como funciona e limitações da análise"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                """
            **🔧 Como funciona:**
            
            • Lista de palavras positivas e negativas
            • "excelente", "inovação" → positivo
            • "problema", "risco" → negativo  
            • Sem palavras claras → neutro
            
            **📊 Cálculo da confiança:**
            
            • Conta palavras de sentimento
            • Divide pelo total de palavras
            • Mais palavras = maior confiança
            """
            )

        with col2:
            st.markdown(
                """
            **⚠️ Limitações importantes:**
            
            • Não entende sarcasmo ou ironia
            • Não considera contexto completo
            • Pode errar em textos complexos
            • É uma aproximação inicial
            
            **💡 Como usar:**
            
            • Primeiro indicativo da percepção
            • Sempre complementar com análise humana
            • Útil para visão geral dos dados
            """
            )


def render_footer():
    """Renderiza o rodapé"""
    st.markdown(
        """
    <div class="footer">
        <p>📅 Desenvolvido para o teste técnico da Secretaria de Inteligência Artificial do Piauí</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
