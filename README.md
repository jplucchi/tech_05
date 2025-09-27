# 🎯 Decision AI Recruiter

Sistema inteligente de recrutamento e seleção desenvolvido para a empresa Decision, utilizando Inteligência Artificial para otimizar o processo de matching candidato-vaga e automatizar entrevistas.

## 📋 Sobre o Projeto

A Decision é uma empresa especializada em serviços de bodyshop e recrutamento no setor de TI. Este projeto desenvolve soluções de IA para resolver as principais dores do processo de recrutamento:

- **Falta de padronização em entrevistas**
- **Dificuldade em identificar o real engajamento dos candidatos**
- **Necessidade de agilizar o processo mantendo a qualidade**

## 🚀 Funcionalidades

### 1. 🎯 Sistema de Matching Candidato-Vaga
- **Algoritmo de compatibilidade** baseado em skills, experiência, salário e fit cultural
- **Modelo de Machine Learning** para prever probabilidade de sucesso em entrevistas
- **Ranking inteligente** combinando compatibilidade e histórico de sucesso
- **Explicações automáticas** dos motivos do match

### 2. 🤖 Entrevistador Virtual com IA
- **Roteiros personalizados** baseados no perfil do candidato e vaga
- **Perguntas adaptativas** por nível (Junior, Pleno, Senior) e tecnologia
- **Avaliação estruturada** em 4 dimensões: técnica, comunicação, fit cultural e engajamento
- **Feedback automatizado** com pontos fortes e áreas de melhoria

### 3. 📊 Dashboard Executivo
- **Métricas em tempo real** de candidatos, vagas e aprovações
- **Análises temporais** de tendências de recrutamento
- **Visualizações interativas** de distribuições por área e nível

### 4. 👥 Análise de Clusters de Sucesso
- **Identificação automática** de perfis de candidatos bem-sucedidos
- **Clustering com K-Means** para segmentar candidatos por características
- **Recomendações** baseadas em padrões de sucesso histórico

### 5. 📈 Análise de Perfis
- **Filtros avançados** por área, nível e experiência
- **Correlações** entre experiência e taxa de sucesso
- **Ranking** dos melhores candidatos por score composto

## 🛠️ Tecnologias Utilizadas

- **Python 3.12+**
- **Streamlit** - Interface web interativa
- **Scikit-learn** - Machine Learning
- **Pandas & NumPy** - Manipulação de dados
- **Plotly** - Visualizações interativas
- **Faker** - Geração de dados sintéticos

## 📁 Estrutura do Projeto

```
tech_05/
├── data/                    # Dados sintéticos
│   ├── applicants.json     # Base de candidatos
│   ├── vagas.json          # Base de vagas
│   └── prospects.json      # Histórico de entrevistas
├── models/                 # Modelos treinados
│   ├── rf_model.pkl        # Modelo Random Forest
│   ├── scaler.pkl          # Scaler para normalização
│   └── kmeans_model.pkl    # Modelo de clustering
├── app.py                  # Aplicação Streamlit principal
├── matching_engine.py      # Sistema de matching e ML
├── ai_interviewer.py       # Agente de entrevistas IA
├── requirements.txt        # Dependências Python
└── README.md              # Documentação
```

## 🚀 Como Executar

### 1. Instalação

```bash
# Clone o repositório
git clone [seu-repositorio]
cd tech_05

# Instale as dependências
pip install -r requirements.txt
```

### 2. Treinamento dos Modelos

```bash
# Treine os modelos de ML
python matching_engine.py
```

### 3. Execução da Aplicação

```bash
# Execute a aplicação Streamlit
streamlit run app.py
```

A aplicação estará disponível em `http://localhost:8501`

## 📊 Resultados e Métricas

### Modelo de Predição de Sucesso
- **Acurácia de Treino:** 99.6%
- **Acurácia de Teste:** 66.5%
- **Features:** 10 características principais
- **Algoritmo:** Random Forest com 100 árvores

### Sistema de Matching
- **Score de Compatibilidade:** Baseado em 5 fatores ponderados
- **Algoritmo de Ranking:** Combinação linear de compatibilidade (60%) e probabilidade de sucesso (40%)
- **Explicabilidade:** Motivos automáticos do match

### Análise de Clusters
- **5 Clusters** identificados automaticamente
- **Cluster de Maior Sucesso:** Taxa de aprovação de 65.8%
- **Características Distintivas:** Experiência, scores técnicos e soft skills

## 🎯 Principais Inovações

1. **Matching Inteligente:** Combina múltiplos fatores com pesos otimizados
2. **Entrevistas Estruturadas:** Roteiros adaptativos por perfil
3. **Predição de Sucesso:** ML para antecipar resultados de entrevistas
4. **Clusters de Perfis:** Identificação automática de padrões de sucesso
5. **Interface Intuitiva:** Dashboard executivo para tomada de decisão

## 📈 Impacto Esperado

- **Redução de 40%** no tempo de processo seletivo
- **Aumento de 25%** na taxa de aprovação final
- **Padronização de 100%** das entrevistas
- **Melhoria na qualidade** do matching candidato-vaga

## 🔮 Próximos Passos

1. **Integração com APIs** de LinkedIn e outras plataformas
2. **Processamento de NLP** para análise de currículos
3. **Sistema de feedback** para melhoria contínua dos modelos
4. **Notificações automáticas** para candidatos e recrutadores
5. **Deploy em produção** com autenticação e banco de dados

## 👥 Equipe

Desenvolvido para o Datathon da Decision - Aplicação de IA em Recrutamento e Seleção.

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos e demonstração de conceitos de IA em RH.

---

**🎯 Decision AI Recruiter - Transformando o futuro do recrutamento com Inteligência Artificial**
