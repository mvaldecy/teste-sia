"""
Utilitários para processamento de dados
"""

import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import os
from .config import DATE_VALIDATION


@st.cache_data
def load_data():
    """Carrega dados do CSV ou retorna DataFrame vazio se não existir"""
    csv_path = "data/noticias.csv"

    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            if not df.empty:
                return df
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")

    return pd.DataFrame()


def validate_dates(df, date_column="data_publicacao"):
    """Valida e filtra datas dentro de um intervalo razoável"""
    try:
        df[f"{date_column}_dt"] = pd.to_datetime(df[date_column], errors="coerce")

        # Define intervalo válido
        hoje = datetime.now()
        limite_passado = hoje - timedelta(days=DATE_VALIDATION["days_back"])
        limite_futuro = hoje + timedelta(days=DATE_VALIDATION["days_forward"])

        # Filtra datas válidas
        df_valid = df[
            (df[f"{date_column}_dt"] >= limite_passado)
            & (df[f"{date_column}_dt"] <= limite_futuro)
            & df[f"{date_column}_dt"].notna()
        ].copy()

        return df_valid

    except Exception:
        return pd.DataFrame()


def get_date_range(df, date_column="data_publicacao"):
    """Obtém intervalo de datas válidas para filtros"""
    try:
        df_valid = validate_dates(df, date_column)

        if not df_valid.empty:
            data_min = df_valid[f"{date_column}_dt"].min().date()
            data_max = df_valid[f"{date_column}_dt"].max().date()
            return data_min, data_max
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


def apply_filters(df, filtro_sentimento, filtro_termo, filtro_data, min_confidence):
    """Aplica todos os filtros ao DataFrame"""
    df_filtered = df.copy()

    # Filtro de confiança
    if min_confidence > 0:
        df_filtered = df_filtered[df_filtered["confianca"] >= min_confidence]

    # Filtro de sentimento
    if not df_filtered.empty and filtro_sentimento != "Todos":
        df_filtered = df_filtered[df_filtered["sentimento"] == filtro_sentimento]

    # Filtro de termo
    if not df_filtered.empty and filtro_termo != "Todos":
        df_filtered = df_filtered[df_filtered["termo_busca"] == filtro_termo]

    # Filtro de data
    if not df_filtered.empty and len(filtro_data) == 2:
        df_filtered = apply_date_filter(df_filtered, filtro_data)

    return df_filtered


def apply_date_filter(df, filtro_data):
    """Aplica filtro de data com fallback inteligente"""
    try:
        df_valid = validate_dates(df, "data_publicacao")
        inicio, fim = filtro_data

        if not df_valid.empty:
            # Use data de publicação se válida
            df_filtered = df[
                (
                    pd.to_datetime(df["data_publicacao"], errors="coerce").dt.date
                    >= inicio
                )
                & (
                    pd.to_datetime(df["data_publicacao"], errors="coerce").dt.date
                    <= fim
                )
                & pd.to_datetime(df["data_publicacao"], errors="coerce").notna()
            ]
        else:
            # Fallback para data de coleta
            df["data_coleta_dt"] = pd.to_datetime(df["data_coleta"])
            df_filtered = df[
                (df["data_coleta_dt"].dt.date >= inicio)
                & (df["data_coleta_dt"].dt.date <= fim)
            ]

        return df_filtered

    except Exception:
        # Em caso de erro, retorna DataFrame original
        return df
