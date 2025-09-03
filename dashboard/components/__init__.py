"""
Componentes da Interface do Dashboard

Este módulo contém todos os componentes reutilizáveis da interface:
- sidebar: Componentes da barra lateral (filtros, controles)
- interface: Componentes da interface principal (métricas, tabelas, etc.)

Cada componente é uma função que renderiza uma parte específica da interface,
seguindo o padrão de componentes modulares do Streamlit.
"""

from .sidebar import render_sidebar
from .interface import (
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

__all__ = [
    "render_sidebar",
    "render_header",
    "render_metrics",
    "render_main_visualizations",
    "render_timeline_chart",
    "render_secondary_charts",
    "render_data_table",
    "render_detailed_statistics",
    "render_limitations_info",
    "render_footer",
]
