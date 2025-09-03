# Documentação de Decisões Técnicas

Este documento explica as principais decisões técnicas tomadas durante o desenvolvimento do projeto de monitoramento de percepção pública sobre IA no Piauí.

## 🤔 Por que escolhi a abordagem de regras para análise de sentimento?

### Decisão

Optei por implementar um sistema de análise de sentimento baseado em regras utilizando listas de palavras-chave positivas e negativas, em vez de um modelo de Machine Learning pré-treinado.

### Justificativas

1. **Simplicidade e Transparência**:

   - O sistema baseado em regras é mais fácil de entender e explicar
   - Permite identificar exatamente quais palavras influenciaram a classificação
   - Facilita a auditoria e validação dos resultados

2. **Controle e Customização**:

   - Posso ajustar facilmente as palavras-chave para o contexto específico de IA e Piauí
   - Não dependo de modelos treinados em outros domínios que podem não capturar as nuances locais
   - Permite adicionar termos técnicos específicos da área de IA governamental

3. **Recursos Limitados**:

   - Não requer grandes datasets de treinamento
   - Executa rapidamente sem necessidade de GPUs ou recursos computacionais intensivos
   - Adequado para um ambiente de teste/prototipação

4. **Interpretabilidade**:
   - Crucial para aplicações governamentais onde a transparência é essencial
   - Permite explicar facilmente como uma notícia foi classificada
   - Facilita a identificação de possíveis vieses nas classificações

### Limitações Reconhecidas

- Não captura contexto complexo, ironia ou sarcasmo
- Pode ser menos preciso que modelos de ML bem treinados
- Requer manutenção manual das listas de palavras

## 🔧 Como lidei com possíveis erros ou falta de notícias no feed RSS?

### Estratégias Implementadas

1. **Múltiplos Termos de Busca**:

   - Uso 4 variações de termos: "Inteligência Artificial Piauí", "SIA Piauí", "IA Piauí", "Artificial Intelligence Piauí"
   - Aumenta as chances de encontrar conteúdo relevante
   - Diversifica as fontes e perspectivas

2. **Tratamento Robusto de Erros**:

   ```python
   try:
       # Requisição HTTP com timeout
       response = requests.get(url, headers=headers, timeout=10)
       response.raise_for_status()
   except requests.RequestException as e:
       print(f"Erro na requisição: {e}")
       return []
   except ET.ParseError as e:
       print(f"Erro no parse XML: {e}")
       return []
   ```

3. **Validação de Dados**:

   - Verifico se os elementos XML existem antes de acessá-los
   - Forneco valores padrão para campos ausentes
   - Limpo e valido o conteúdo extraído

4. **Rate Limiting**:

   - Pausa de 1 segundo entre requisições para evitar bloqueios
   - Headers de User-Agent para simular navegador real

5. **Fallbacks e Logs**:

   - Sistema de logs detalhado para identificar problemas
   - Continua processando outros termos mesmo se um falhar
   - Salva dados parciais mesmo com alguns erros

6. **Formato Dual (RSS/Atom)**:
   - Suporte tanto para feeds RSS quanto Atom
   - Detecta automaticamente o formato e ajusta o parsing

### Cenários de Fallback

1. **Feed Indisponível**: Tenta outros termos de busca
2. **Dados Corrompidos**: Pula itens problemáticos e continua
3. **Rate Limiting**: Implementa delays progressivos
4. **Cache no Dashboard**: Evita reprocessamento de dados

## 🏗️ Outras Decisões Arquiteturais

### Estrutura Modular

- **news_collector.py**: Responsabilidade única de coleta
- **sentiment_analysis/**: Módulo de análise isolado e testável
- **dashboard.py**: Interface de usuário separada da lógica
- **utils/**: Funções auxiliares reutilizáveis

### Tecnologias Escolhidas

1. **Streamlit**:

   - Desenvolvimento rápido de interfaces
   - Ideal para prototipagem e dashboards de dados
   - Boa integração com pandas e plotly

2. **Pandas**:

   - Manipulação eficiente de dados estruturados
   - Excelente para análise e agregação
   - Facilita exportação para diferentes formatos

3. **Plotly**:

   - Gráficos interativos modernos
   - Boa experiência do usuário
   - Integração nativa com Streamlit

4. **WordCloud**:
   - Visualização intuitiva de frequência de palavras
   - Biblioteca madura e confiável

### Armazenamento de Dados

- **CSV**: Para visualização e análise humana
- **JSON**: Para integração com outros sistemas
- **Estrutura temporal**: Permite análise de tendências

### Considerações de Performance

- **Cache no Streamlit**: Evita reprocessamento desnecessário
- **Batch processing**: Analisa todos os textos de uma vez
- **Dados locais**: Evita requisições repetidas durante desenvolvimento

## 🔄 Melhorias Futuras Consideradas

1. **ML Integration**: Migração para modelos BERT/RoBERTa quando houver dados suficientes
2. **Real-time Updates**: Sistema de coleta automática agendada
3. **Advanced NLP**: Análise de entidades, tópicos e emoções
4. **Data Pipeline**: Apache Airflow para orquestração
5. **Monitoring**: Alertas para anomalias nos dados

## 🧪 Processo de Desenvolvimento

### Metodologia

1. **Análise de Requisitos**: Estudo detalhado do case
2. **Prototipagem Rápida**: MVP funcional primeiro
3. **Iteração**: Refinamento baseado em testes
4. **Documentação**: Processo contínuo durante desenvolvimento

### Testes Realizados

- Teste manual com diferentes termos de busca
- Validação da análise de sentimento com textos conhecidos
- Verificação da robustez com dados malformados
- Teste de interface em diferentes resoluções

## 🤖 Transparência sobre Uso de IA

### Componentes Desenvolvidos com Assistência de IA

1. **Dicionários de Sentimento** (`sentiment_analysis/dictionaries.py`):

   - Compilação das listas de palavras positivas e negativas
   - Organização por categorias temáticas
   - Inclusão de termos específicos do contexto governamental

2. **Interface do Dashboard** (`dashboard/components/interface.py`):

   - Layout responsivo e componentes visuais
   - Configuração de colunas e métricas
   - Estrutura de gráficos e visualizações

3. **Algoritmos de Análise** (`sentiment_analysis/analyzer.py`):
   - Lógica de classificação de sentimentos
   - Cálculo de scores de confiança
   - Tratamento de negações e intensificadores

### Decisões Técnicas Próprias

- **Arquitetura modular**: Separação em packages especializados
- **Estratégias de fallback**: Tratamento robusto de erros
- **Escolha de tecnologias**: Streamlit, Pandas, Plotly
- **Estrutura de dados**: CSV/JSON para armazenamento
- **Fluxo de processamento**: Pipeline de coleta → análise → visualização

### Justificativa

O uso de IA foi estratégico para acelerar desenvolvimento de:

- Componentes de interface com padrões estabelecidos
- Listas de palavras-chave abrangentes
- Documentação estruturada e clara

Permitindo focar nas decisões arquiteturais críticas e na lógica de negócio específica do contexto piauiense.

Esta documentação reflete as decisões tomadas para balancear simplicidade, funcionalidade e confiabilidade dentro das limitações de tempo e recursos do teste técnico.
