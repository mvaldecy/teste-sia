"""
Script para coleta de notícias do Google RSS sobre IA no Piauí
"""

import requests
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
import re
from urllib.parse import quote
import time
import os


class NewsCollector:
    def __init__(self):
        self.base_url = "https://news.google.com/rss/search"
        self.search_terms = [
            "Inteligência Artificial Piauí",
            "SIA Piauí",
            "IA Piauí",
            "Artificial Intelligence Piauí",
            "Secretaria Inteligência Artificial Piauí",
            "SoberanIA Piauí",
        ]
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )

    def clean_text(self, text):
        """Limpa o texto removendo tags HTML e caracteres especiais"""
        if not text:
            return ""

        # Remove tags HTML
        text = re.sub(r"<[^>]+>", "", text)
        # Remove caracteres especiais mantendo acentos
        text = re.sub(r"[^\w\s\-.,;:!?áéíóúàèìòùâêîôûãõçÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕÇ]", "", text)
        # Remove espaços extras
        text = " ".join(text.split())

        return text.strip()

    def fetch_news_for_term(self, search_term, max_retries=3):
        """Busca notícias para um termo específico"""
        base_url = "https://news.google.com/rss/search"
        query = f"{search_term}"
        url = f"{base_url}?q={query}&hl=pt-BR&gl=BR&ceid=BR:pt"

        for attempt in range(max_retries):
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }

                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()

                try:
                    root = ET.fromstring(response.content)
                    news_data = []

                    for i, item in enumerate(root.findall(".//item")):
                        if i >= 50:  # Limita a 50 itens por termo
                            break

                        try:
                            title = item.find("title")
                            title_text = title.text if title is not None else ""
                            title_clean = self.clean_text(title_text)

                            description = item.find("description")
                            desc_text = (
                                description.text if description is not None else ""
                            )
                            desc_clean = self.clean_text(desc_text)

                            link = item.find("link")
                            link_text = link.text if link is not None else ""

                            pub_date = item.find("pubDate")
                            pub_date_text = (
                                pub_date.text if pub_date is not None else ""
                            )

                            if title_clean:
                                news_item = {
                                    "termo_busca": search_term,
                                    "titulo": title_clean,
                                    "link": link_text,
                                    "descricao": desc_clean,
                                    "data_publicacao": pub_date_text,
                                    "data_coleta": datetime.now().isoformat(),
                                    "texto_completo": f"{title_clean} {desc_clean}",
                                }
                                news_data.append(news_item)

                        except Exception as e:
                            continue

                    return news_data

                except ET.ParseError as e:
                    if attempt < max_retries - 1:
                        time.sleep(2**attempt)
                        continue
                    else:
                        return []

            except requests.RequestException as e:
                if attempt < max_retries - 1:
                    time.sleep(2**attempt)
                    continue
                else:
                    return []
            except Exception as e:
                return []

        return []

    def collect_all_news(self, max_per_term=4):
        """Coleta notícias para todos os termos de busca"""
        all_news = []

        for term in self.search_terms:
            news_items = self.fetch_news_for_term(term, max_per_term)
            all_news.extend(news_items)
            time.sleep(1)  # Pausa entre requisições

        return all_news

    def save_to_csv(self, news_data, filename="data/noticias.csv"):
        """Salva os dados em CSV"""
        if not news_data:
            return

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        df = pd.DataFrame(news_data)
        df.to_csv(filename, index=False, encoding="utf-8")

    def save_to_json(self, news_data, filename="data/noticias.json"):
        """Salva os dados em JSON"""
        if not news_data:
            return

        import json

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)


def main():
    """Função principal"""
    collector = NewsCollector()
    news_data = collector.collect_all_news(max_per_term=4)

    if news_data:
        collector.save_to_csv(news_data)
        collector.save_to_json(news_data)


if __name__ == "__main__":
    main()
