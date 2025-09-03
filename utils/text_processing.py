"""
Utilitários para processamento de texto
"""

import re
from collections import Counter
import pandas as pd


def clean_html_tags(text):
    """Remove tags HTML do texto"""
    if not text:
        return ""
    return re.sub(r"<[^>]+>", "", text)


def remove_special_chars(text, keep_accents=True):
    """Remove caracteres especiais mantendo acentos opcionalmente"""
    if not text:
        return ""

    if keep_accents:
        # Mantém acentos portugueses
        pattern = r"[^\w\s\-.,;:!?áéíóúàèìòùâêîôûãõçÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕÇ]"
    else:
        pattern = r"[^\w\s\-.,;:!?]"

    return re.sub(pattern, "", text)


def normalize_whitespace(text):
    """Normaliza espaços em branco"""
    if not text:
        return ""
    return " ".join(text.split())


def clean_text_pipeline(text, verbose=False):
    """
    Pipeline completa de limpeza de texto
    """
    if not text or not isinstance(text, str):
        return ""

    # Aplicar todas as limpezas em sequência
    cleaned = text
    cleaned = clean_html_tags(cleaned)
    cleaned = normalize_whitespace(cleaned)
    cleaned = remove_special_chars(cleaned)

    return cleaned.strip()


def clean_dataframe_text_columns(df, columns=None, verbose=False):
    """
    Aplica limpeza de texto em colunas específicas de um DataFrame
    """
    if df.empty:
        return df

    df_clean = df.copy()

    # Se não especificar colunas, usa colunas de texto detectadas automaticamente
    if columns is None:
        columns = df_clean.select_dtypes(include=["object"]).columns.tolist()

    for col in columns:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].apply(
                lambda x: clean_text_pipeline(x, verbose=False) if pd.notna(x) else x
            )


def extract_keywords(text, min_length=4, max_keywords=20):
    """Extrai palavras-chave do texto"""
    if not text:
        return []

    # Palavras irrelevantes para filtrar
    stop_words = {
        "para",
        "com",
        "uma",
        "como",
        "mais",
        "ser",
        "ter",
        "fazer",
        "esse",
        "essa",
        "este",
        "esta",
        "isso",
        "aquele",
        "aquela",
        "pelo",
        "pela",
        "pelos",
        "pelas",
        "desde",
        "ainda",
        "também",
        "apenas",
        "todos",
        "todas",
        "muito",
        "muita",
        "onde",
        "quando",
        "porque",
        "então",
        "assim",
        "depois",
        "antes",
        "durante",
        "sobre",
        "entre",
        "através",
        "mediante",
        "segundo",
        "conforme",
        "enquanto",
    }

    # Preprocessa o texto
    text = text.lower()
    text = re.sub(r"[^\w\s\-áéíóúàèìòùâêîôûãõç]", " ", text)
    words = text.split()

    # Filtra palavras
    keywords = [
        word
        for word in words
        if len(word) >= min_length and word not in stop_words and not word.isdigit()
    ]

    # Conta frequências
    word_freq = Counter(keywords)

    # Retorna as mais frequentes
    return [word for word, count in word_freq.most_common(max_keywords)]


def calculate_text_stats(text):
    """Calcula estatísticas básicas do texto"""
    if not text:
        return {"caracteres": 0, "palavras": 0, "frases": 0, "palavras_unicas": 0}

    # Conta caracteres
    char_count = len(text)

    # Conta palavras
    words = text.split()
    word_count = len(words)
    unique_words = len(set(word.lower() for word in words))

    # Conta frases (aproximação baseada em pontuação)
    sentence_count = len(re.findall(r"[.!?]+", text))
    if sentence_count == 0 and text.strip():
        sentence_count = 1

    return {
        "caracteres": char_count,
        "palavras": word_count,
        "frases": sentence_count,
        "palavras_unicas": unique_words,
    }


def process_dataframe_texts(df, text_columns):
    """Processa colunas de texto em um DataFrame"""
    df_processed = df.copy()

    for col in text_columns:
        if col in df_processed.columns:
            # Aplica limpeza
            df_processed[f"{col}_limpo"] = df_processed[col].apply(clean_text_pipeline)

            # Extrai keywords
            df_processed[f"{col}_keywords"] = df_processed[col].apply(
                lambda x: ", ".join(extract_keywords(x, max_keywords=10))
            )

            # Calcula estatísticas
            stats = df_processed[col].apply(calculate_text_stats)
            df_processed[f"{col}_num_palavras"] = [s["palavras"] for s in stats]
            df_processed[f"{col}_num_caracteres"] = [s["caracteres"] for s in stats]

    return df_processed


def create_word_frequency_data(texts, min_length=4, max_words=50):
    """Cria dados de frequência de palavras para visualização"""
    all_text = " ".join(str(text) for text in texts if text)
    keywords = extract_keywords(all_text, min_length=min_length, max_keywords=max_words)

    # Conta frequências em todo o corpus
    word_freq = Counter()
    for text in texts:
        if text:
            text_keywords = extract_keywords(str(text), min_length=min_length)
            word_freq.update(text_keywords)

    # Retorna como lista de dicionários para fácil uso com plotly
    freq_data = [
        {"palavra": word, "frequencia": freq}
        for word, freq in word_freq.most_common(max_words)
    ]

    return freq_data


def main():
    """Função de teste silenciosa"""
    # Texto de exemplo para teste
    test_text = """
    <p>A <strong>inteligência artificial</strong> está revolucionando o setor público no Piauí!!! 
    Através de parcerias estratégicas, o governo implementa soluções inovadoras... 
    Isso representa um grande avanço tecnológico para nosso estado.</p>
    """

    # Testes silenciosos
    clean = clean_text_pipeline(test_text)
    keywords = extract_keywords(clean)
    stats = calculate_text_stats(clean)

    # Retorna resultados para possível verificação
    return {"original": test_text, "clean": clean, "keywords": keywords, "stats": stats}


if __name__ == "__main__":
    main()
