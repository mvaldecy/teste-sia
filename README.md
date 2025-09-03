# 🧠 Monitor de Percepção Pública sobre IA no Piauí

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-Educational-green.svg)](https://github.com/mvaldecy/teste-sia)
[![GitHub](https://img.shields.io/badge/GitHub-teste--sia-black.svg)](https://github.com/mvaldecy/teste-sia)
[![Deploy](https://img.shields.io/badge/Deploy-Online-brightgreen.svg)](https://mvaldecy-teste-sia-dashboard-otrkvd.streamlit.app/)

Sistema de monitoramento e análise de sentimento de notícias sobre Inteligência Artificial no estado do Piauí, desenvolvido para a Secretaria de Inteligência Artificial.

## 🌐 Demo Online

🔗 **[Acesse o Dashboard Online](https://mvaldecy-teste-sia-dashboard-otrkvd.streamlit.app/)**

> ✨ **Pronto para usar!** O dashboard está disponível online no Streamlit Cloud - sem necessidade de instalação.

## 📋 Visão Geral

O projeto coleta automaticamente notícias relacionadas à IA no Piauí através do Google News RSS, analisa o sentimento do conteúdo e apresenta insights através de um dashboard interativo construído com Streamlit.

### 🎯 Principais Funcionalidades

- **Coleta Automatizada**: Monitoramento contínuo de 6 termos relacionados à IA no Piauí
- **Análise de Sentimento**: Classificação em positivo, negativo ou neutro com nível de confiança
- **Dashboard Interativo**: Visualizações em tempo real com filtros avançados
- **Exportação de Dados**: Download dos resultados em formato CSV
- **Arquitetura Modular**: Código organizado e de fácil manutenção

## 🚀 Início Rápido

### ⚡ Execução em Uma Linha

```bash
git clone https://github.com/mvaldecy/teste-sia.git && cd teste-sia && ./start.sh
```

> 🎯 **Este comando faz tudo**: clona o repositório, configura o ambiente e inicia o dashboard!

### Pré-requisitos

- **Python 3.10+** ([Download aqui](https://www.python.org/downloads/))
- **pip** (incluído com Python)
- **git** (para clonar o repositório)

### Instalação e Execução

#### Opção 1: Acesso Online (Mais Fácil) 🌐

```
🔗 https://mvaldecy-teste-sia-dashboard-otrkvd.streamlit.app/
```

> ✅ **Sem instalação necessária!** Acesse diretamente pelo navegador.

#### Opção 2: Execução Automática Local (Recomendada)

```bash
# Clone o repositório
git clone https://github.com/mvaldecy/teste-sia.git
cd teste-sia

# Execute o script automático (faz tudo automaticamente)
./start.sh
```

> 🚀 **O script `start.sh` faz tudo automaticamente:**
>
> - Verifica se Python está instalado
> - Cria o ambiente virtual se necessário
> - Instala todas as dependências
> - Coleta dados iniciais (opcional)
> - Inicia o dashboard

#### Opção 3: Instalação Manual

1. **Clone e acesse o repositório**

```bash
git clone https://github.com/mvaldecy/teste-sia.git
cd teste-sia
```

2. **Configure o ambiente virtual**

```bash
# Criar ambiente virtual
python3 -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

3. **Instale as dependências**

```bash
# Instalação básica (compatível com Streamlit Cloud)
pip install -r requirements.txt

# OU instalação completa com WordCloud (apenas para desenvolvimento local)
pip install -r requirements-full.txt
```

> 💡 **Nota**: O `requirements.txt` não inclui o WordCloud para garantir compatibilidade com o Streamlit Cloud. Para desenvolvimento local com todas as funcionalidades, use `requirements-full.txt`.

4. **Colete dados iniciais (opcional)**

```bash
python3 news_collector.py
```

> ⏱️ Este passo demora ~2-3 minutos e é opcional. O dashboard funciona com dados de exemplo.

5. **Execute o dashboard**

```bash
streamlit run dashboard.py
```

#### Acesso ao Dashboard

- Abra [http://localhost:8501](http://localhost:8501) no navegador
- O dashboard carregará automaticamente

### 🔧 Verificação Rápida

```bash
# Teste se tudo funciona
python3 test_suite.py
```

## 📁 Estrutura do Projeto

```
teste-sia/
├── README.md                    # Documentação principal
├── DECISIONS.md                 # Decisões técnicas e arquiteturais
├── requirements.txt             # Dependências Python
├── config.py                    # Configurações centralizadas
├── start.sh                     # Script de inicialização
├── dashboard.py                 # Aplicação principal Streamlit
├── news_collector.py            # Coleta de notícias RSS
├── test_suite.py               # Suite de testes completa
├── sentiment_analysis/          # Módulo de análise de sentimento
│   ├── __init__.py
│   ├── analyzer.py             # Analisador principal
│   ├── dictionaries.py         # Dicionários de palavras
│   ├── confidence.py           # Cálculo de confiança
│   └── text_processor.py       # Processamento de texto
├── dashboard/                   # Componentes do dashboard
│   ├── config.py               # Configurações do dashboard
│   ├── data_utils.py           # Utilitários de dados
│   ├── sentiment.py            # Interface de sentimento
│   ├── components/             # Componentes da interface
│   │   ├── interface.py        # Interface principal
│   │   └── sidebar.py          # Barra lateral
│   └── visualizations/         # Visualizações
│       └── charts.py           # Gráficos e charts
├── utils/                      # Utilitários gerais
│   └── text_processing.py     # Processamento de texto
└── data/                       # Dados coletados
    ├── noticias.csv           # Dados em formato CSV
    └── noticias.json          # Dados em formato JSON
```

│ ├── analyzer.py # Analisador principal
│ ├── dictionaries.py # Dicionários de palavras
│ ├── confidence.py # Cálculo de confiança
│ └── text_processor.py # Processamento de texto
├── dashboard/ # Componentes do dashboard
│ ├── config.py # Configurações do dashboard
│ ├── data_utils.py # Utilitários de dados
│ ├── sentiment.py # Interface de sentimento
│ ├── components/ # Componentes da interface
│ │ ├── interface.py # Interface principal
│ │ └── sidebar.py # Barra lateral
│ └── visualizations/ # Visualizações
│ └── charts.py # Gráficos e charts
├── utils/ # Utilitários gerais
│ └── text_processing.py # Processamento de texto
└── data/ # Dados coletados
├── noticias.csv # Dados em formato CSV
└── noticias.json # Dados em formato JSON

````

## 🔧 Componentes Principais

### 📊 Dashboard Streamlit

- Interface web interativa
- Filtros por sentimento, termo e data
- Visualizações: gráficos de pizza, linha temporal, nuvem de palavras
- Tabela de dados com links clicáveis
- Métricas em tempo real

### 🤖 Sistema de Análise de Sentimento

- Arquitetura modular com 5 componentes especializados
- Dicionários de palavras positivas e negativas
- Tratamento de negações e intensificadores
- Cálculo de confiança baseado na densidade de palavras-chave
- Suporte completo ao português brasileiro

### 📰 Coletor de Notícias

- Busca em 6 termos relacionados à IA no Piauí
- Integração com Google News RSS
- Sistema de retry e tratamento de erros
- Limpeza e normalização de texto
- Armazenamento em CSV e JSON

### 🧪 Sistema de Testes

- Testes unitários para todos os componentes
- Validação de integridade de dados
- Testes de regressão para mudanças

## ⚡ Comandos Úteis

```bash
# Coletar notícias manualmente
python3 news_collector.py

# Executar testes completos
python3 test_suite.py

# Iniciar dashboard (modo desenvolvimento)
streamlit run dashboard.py

# Verificar versão do Python
python3 --version
````

## 🔧 Solução de Problemas

### Problema: "Python3 não encontrado"

```bash
# Instale Python 3.10+
# Ubuntu/Debian: sudo apt install python3 python3-venv
# macOS: brew install python3
# Windows: https://www.python.org/downloads/
```

### Problema: "Permission denied" no start.sh

```bash
# Torne o script executável
chmod +x start.sh
```

### Problema: "ModuleNotFoundError"

```bash
# Use o script automático que resolve tudo
./start.sh

# OU ative o ambiente virtual manualmente
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Problema: Dashboard não carrega

1. Verifique se a porta 8501 está livre
2. Tente usar outra porta: `streamlit run dashboard.py --server.port 8502`
3. Verifique os logs no terminal
4. Use o script automático: `./start.sh`

### Problema: Sem dados na tabela

```bash
# Execute a coleta de dados primeiro
python3 news_collector.py

# OU use o script completo
./start.sh
```

### Problema: Ambiente virtual não ativa

```bash
# Use o script automático (cria e ativa automaticamente)
./start.sh
```

## 🎨 Capturas de Tela

O dashboard apresenta:

- Métricas resumidas (total, positivas, negativas, neutras)
- Gráfico de distribuição de sentimentos
- Nuvem de palavras dos termos mais frequentes
- Evolução temporal dos sentimentos
- Tabela interativa com filtros avançados

## ⚠️ Limitações e Considerações

### Análise de Sentimento

- Baseada em dicionários de palavras-chave
- Não detecta sarcasmo ou ironia
- Limitada ao contexto de frases simples
- Recomendada como análise inicial, não substitui revisão humana

### Coleta de Dados

- Dependente da disponibilidade do Google News RSS
- Limitada aos termos de busca pré-definidos
- Sem detecção avançada de duplicatas

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**: Linguagem principal
- **Streamlit**: Framework para dashboard web
- **Pandas**: Manipulação de dados
- **Plotly**: Visualizações interativas
- **WordCloud**: Geração de nuvem de palavras
- **Requests**: Requisições HTTP
- **XML Parser**: Processamento de RSS

## 📈 Próximos Passos

- Integração com modelos de IA mais avançados (BERT, GPT)
- Sistema de alertas para sentimentos críticos
- Análise de trending topics
- Suporte a múltiplas fontes de notícias
- Dashboard mobile-friendly

## 🤖 Uso de Inteligência Artificial no Desenvolvimento

Para fins de transparência, informo que algumas partes deste projeto foram desenvolvidas com auxílio de modelos de IA:

### Componentes com Assistência de IA:

- **Interface do Dashboard (Streamlit)**: Layout, componentes visuais e estrutura da interface
- **Dicionários de Sentimento**: Compilação e organização das listas de palavras positivas e negativas
- **Lógica de Análise de Sentimento**: Algoritmos de classificação e cálculo de confiança
- **Documentação**: Estruturação do README.md e DECISIONS.md
- **Comentários de Código**: Documentação inline e docstrings

### Desenvolvimento Próprio:

- **Arquitetura do Sistema**: Decisões de design e estrutura modular
- **Integração de Componentes**: Conexão entre módulos e fluxo de dados
- **Lógica de Negócio**: Regras específicas para o contexto do Piauí
- **Tratamento de Erros**: Estratégias de fallback e robustez
- **Testes**: Casos de teste e validações

### Justificativa:

O uso de IA foi estratégico para acelerar o desenvolvimento de componentes não-críticos, permitindo focar tempo e energia nas decisões arquiteturais importantes e na lógica de negócio específica do projeto.

## 🌐 Deploy e Produção

### Status do Deploy

✅ **Online e Funcionando**  
🔗 [https://mvaldecy-teste-sia-dashboard-otrkvd.streamlit.app/](https://mvaldecy-teste-sia-dashboard-otrkvd.streamlit.app/)

### Características do Deploy:

- **Plataforma**: Streamlit Cloud
- **Python**: 3.11 (otimizado para compatibilidade)
- **Dependencies**: Configuração otimizada sem WordCloud para máxima compatibilidade
- **Disponibilidade**: 24/7 com auto-restart
- **Performance**: Cache inteligente e otimizações de carregamento

### Configurações Especiais:

- `runtime.txt`: Especifica Python 3.11 para estabilidade
- `requirements.txt`: Versão otimizada para cloud (sem dependências problemáticas)
- `.streamlit/config.toml`: Configurações personalizadas de tema e performance
- WordCloud opcional: Interface adaptativa que funciona com ou sem a biblioteca

## 👥 Desenvolvimento

Desenvolvido para a Secretaria de Inteligência Artificial do Piauí como parte do processo seletivo.

**Autor**: Marcos Valdecy Macedo Costa Leite  
**Período**: Setembro 2025  
**Versão**: 1.0.0  
**Repositório**: [https://github.com/mvaldecy/teste-sia](https://github.com/mvaldecy/teste-sia)

## 📄 Documentação Adicional

- [`DECISIONS.md`](DECISIONS.md): Decisões técnicas e arquiteturais detalhadas
