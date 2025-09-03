#!/bin/bash
# Script de inicialização completa para o projeto

echo "🚀 Inicializando projeto Monitor IA Piauí..."

# Verifica se Python está disponível
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Instale Python 3.10+ primeiro"
    echo "📥 Download: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python $(python3 --version) encontrado"

# Cria o ambiente virtual se não existir
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao criar ambiente virtual"
        exit 1
    fi
    echo "✅ Ambiente virtual criado"
fi

# Ativa o ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source .venv/bin/activate

# Verifica se ativação funcionou
if [ "$VIRTUAL_ENV" = "" ]; then
    echo "❌ Erro ao ativar ambiente virtual"
    exit 1
fi

echo "✅ Ambiente virtual ativo: $VIRTUAL_ENV"

# Instala dependências se necessário
if [ ! -f ".dependencies_installed" ]; then
    echo "📦 Instalando dependências..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao instalar dependências"
        exit 1
    fi
    touch .dependencies_installed
    echo "✅ Dependências instaladas"
else
    echo "✅ Dependências já instaladas"
fi

# Coleta dados se não existirem (opcional)
if [ ! -f "data/noticias.csv" ]; then
    echo "📰 Coletando dados iniciais (pode demorar 2-3 minutos)..."
    python3 news_collector.py
    if [ $? -eq 0 ]; then
        echo "✅ Dados coletados com sucesso"
    else
        echo "⚠️ Erro na coleta, mas continuando (dashboard funcionará com dados exemplo)"
    fi
else
    echo "✅ Dados já existem"
fi

# Inicia o dashboard
echo "🌐 Iniciando dashboard..."
echo "🔗 Acesse: http://localhost:8501"
echo "⏹️ Pressione Ctrl+C para parar"
python3 -m streamlit run dashboard.py
