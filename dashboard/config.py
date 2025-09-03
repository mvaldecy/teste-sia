"""
Configurações do dashboard
"""

# Configurações de cores
COLORS = {"positivo": "#27AE60", "negativo": "#E74C3C", "neutro": "#95A5A6"}

# Configurações de página
PAGE_CONFIG = {
    "page_title": "Monitor IA Piauí",
    "page_icon": "🧠",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# CSS customizado
CUSTOM_CSS = """
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79, #2e7d3e);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f4e79;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #856404;
    }
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #666;
        border-top: 1px solid #eee;
        margin-top: 3rem;
    }
</style>
"""

# Configurações de palavra cloud
WORDCLOUD_CONFIG = {
    "width": 800,
    "height": 400,
    "background_color": "white",
    "colormap": "viridis",
    "max_words": 50,
    "relative_scaling": 0.5,
    "min_font_size": 10,
}

# Configurações de validação de data
DATE_VALIDATION = {"days_back": 365, "days_forward": 30}
