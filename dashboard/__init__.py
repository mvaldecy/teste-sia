"""
Dashboard para Monitoramento de Percepção Pública sobre IA no Piauí

Este pacote contém todos os módulos necessários para o dashboard de análise
de sentimentos em notícias sobre Inteligência Artificial no Piauí.

Módulos:
- config: Configurações e constantes
- data_utils: Utilitários para processamento de dados
- sentiment: Análise de sentimentos
- components: Componentes da interface (sidebar, interface)
- visualizations: Gráficos e visualizações

Desenvolvido para o teste técnico da Secretaria de Inteligência Artificial do Piauí.
"""

__version__ = "1.0.0"
__author__ = "Marcos Valdecy Macedo Costa Leite"

# Importações principais para facilitar o uso
from .config import PAGE_CONFIG, CUSTOM_CSS, COLORS
from .data_utils import load_data, apply_filters
from .sentiment import analyze_sentiments

__all__ = [
    "PAGE_CONFIG",
    "CUSTOM_CSS",
    "COLORS",
    "load_data",
    "apply_filters",
    "analyze_sentiments",
]
