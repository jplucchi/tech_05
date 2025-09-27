# 🎯 Decision AI Recruiter - Demonstração

## 🚀 Como Executar a Demonstração

### Passo 1: Preparação do Ambiente
```bash
# Navegue até o diretório do projeto
cd /Users/joaopaulolucchi/Desktop/tech_05

# Instale as dependências (se necessário)
pip install -r requirements.txt
```

### Passo 2: Iniciar a Aplicação
```bash
# Opção 1: Comando direto
streamlit run app.py

# Opção 2: Script de inicialização
./start.sh

# Opção 3: Deploy automático
python3 deploy.py
```

### Passo 3: Acessar a Aplicação
- Abra seu navegador em: `http://localhost:8501`
- A aplicação carregará automaticamente

## 🎮 Roteiro de Demonstração

### 1. 📊 Dashboard Executivo (2 min)
**O que demonstrar:**
- Métricas principais: 500 candidatos, vagas ativas, taxa de aprovação
- Gráficos de distribuição por nível e área
- Tendências temporais de entrevistas

**Pontos de destaque:**
- Interface moderna e intuitiva
- Visualizações interativas com Plotly
- Métricas atualizadas em tempo real

### 2. 🎯 Sistema de Matching (5 min)
**O que demonstrar:**
1. Selecionar uma vaga (ex: "Junior Data Science Developer")
2. Visualizar os top 10 candidatos compatíveis
3. Explorar os scores de compatibilidade e probabilidade de sucesso
4. Analisar os motivos do match (skills, experiência, salário)

**Pontos de destaque:**
- Score final combinado (60% compatibilidade + 40% probabilidade de sucesso)
- Explicabilidade dos resultados
- Sistema de ranking inteligente

### 3. 🤖 Entrevista com IA (7 min)
**O que demonstrar:**
1. Agendar entrevista a partir do matching
2. Gerar roteiro personalizado de entrevista
3. Visualizar seções estruturadas (técnica, comportamental, cultural)
4. Analisar simulação de avaliação automática
5. Baixar relatório completo

**Pontos de destaque:**
- Roteiros adaptativos por nível e área
- Perguntas específicas por tecnologia
- Avaliação em 4 dimensões com pesos
- Feedback estruturado e automático

### 4. 📈 Análise de Perfis (3 min)
**O que demonstrar:**
1. Aplicar filtros por área, nível e experiência
2. Visualizar correlações entre experiência e sucesso
3. Analisar distribuição de scores
4. Explorar ranking dos melhores candidatos

**Pontos de destaque:**
- Análise estatística avançada
- Gráficos de correlação interativos
- Score composto personalizable

### 5. 👥 Clusters de Sucesso (3 min)
**O que demonstrar:**
1. Visualizar 5 clusters identificados automaticamente
2. Analisar características de cada cluster
3. Identificar cluster com maior taxa de sucesso (65.8%)
4. Visualizar gráfico de bolhas interativo

**Pontos de destaque:**
- Machine Learning não supervisionado (K-Means)
- Identificação automática de padrões
- Recomendações baseadas em dados

## 📊 Dados de Demonstração

### Estatísticas Gerais
- **500 candidatos** sintéticos realistas
- **100 vagas** em diferentes áreas de TI
- **1000 entrevistas** com histórico completo
- **5 clusters** de perfis identificados

### Tecnologias Representadas
- **Backend:** Python, Java, Node.js, Spring Boot
- **Frontend:** React, Angular, Vue.js, JavaScript
- **DevOps:** Docker, Kubernetes, AWS, Azure
- **Data Science:** TensorFlow, PyTorch, Pandas, SQL

### Áreas de Atuação
- Frontend Development
- Backend Development  
- Full Stack Development
- DevOps Engineering
- Data Science
- Mobile Development
- QA Engineering
- UX/UI Design

## 🎯 Principais Resultados

### Modelo de Machine Learning
- **Acurácia de teste:** 66.5%
- **Features utilizadas:** 10 características principais
- **Algoritmo:** Random Forest com 100 árvores
- **Validação:** Train/test split com 80/20

### Sistema de Matching
- **Fatores considerados:** Experiência (25%), Skills (30%), Salário (15%), Localização (10%), Soft Skills (20%)
- **Explicabilidade:** Motivos automáticos para cada match
- **Performance:** Ranking de 500 candidatos em < 1 segundo

### Clusters Identificados
- **Cluster de Alto Sucesso:** 65.8% de taxa de aprovação
- **Características distintivas:** Alta experiência + alto score técnico
- **Aplicação prática:** Priorização de candidatos similares

## 💡 Perguntas Frequentes

### Q: Os dados são reais?
**R:** Não, utilizamos dados sintéticos gerados com a biblioteca Faker para simular um ambiente realista sem comprometer dados pessoais.

### Q: Como o sistema calcula a compatibilidade?
**R:** Utilizamos um algoritmo ponderado que considera skills técnicas (30%), experiência (25%), adequação salarial (15%), localização/modelo de trabalho (10%) e soft skills (20%).

### Q: O agente de IA substitui totalmente o recrutador?
**R:** Não, o sistema é um assistente inteligente que padroniza e otimiza o processo, mas o recrutador humano permanece essencial para a decisão final.

### Q: Como garantir a qualidade das predições?
**R:** O modelo é treinado continuamente com novos dados de entrevistas e resultados, permitindo melhoria constante da acurácia.

## 🚀 Próximos Passos para Produção

### Integrações
- **LinkedIn API** para busca automática de candidatos
- **E-mail** para notificações automáticas
- **Calendário** para agendamento de entrevistas
- **ATS** existente da empresa

### Melhorias Técnicas
- **Processamento de NLP** para análise de currículos
- **Computer Vision** para análise de vídeo-entrevistas
- **Feedback Loop** para melhoria contínua dos modelos
- **A/B Testing** para otimização de algoritmos

### Infraestrutura
- **Banco de dados** PostgreSQL/MongoDB
- **Autenticação** OAuth2/LDAP
- **Deploy** containerizado com Docker
- **Monitoramento** com logs e métricas

---

**🎯 Decision AI Recruiter - Demonstração preparada para o Datathon**
*Transformando o futuro do recrutamento com Inteligência Artificial*
