import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from matching_engine import CandidateJobMatcher
from ai_interviewer import AIInterviewer
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Decision AI Recruiter",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .candidate-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #fafafa;
    }
    .score-high { color: #28a745; font-weight: bold; }
    .score-medium { color: #ffc107; font-weight: bold; }
    .score-low { color: #dc3545; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Carrega e processa os dados"""
    try:
        # Usar caminhos relativos que funcionam tanto local quanto no deploy
        import os
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        with open(os.path.join(base_path, 'data', 'applicants.json'), 'r', encoding='utf-8') as f:
            candidates = json.load(f)
        
        with open(os.path.join(base_path, 'data', 'vagas.json'), 'r', encoding='utf-8') as f:
            jobs = json.load(f)
            
        with open(os.path.join(base_path, 'data', 'prospects.json'), 'r', encoding='utf-8') as f:
            interviews = json.load(f)
        
        return candidates, jobs, interviews
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return [], [], []

@st.cache_resource
def load_matcher():
    """Carrega o sistema de matching"""
    try:
        matcher = CandidateJobMatcher()
        matcher.load_data()
        matcher.train_success_prediction_model()
        return matcher
    except Exception as e:
        st.error(f"Erro ao carregar matcher: {e}")
        return None

def format_score(score):
    """Formata score com cores"""
    if score >= 0.7:
        return f"<span class='score-high'>{score:.1%}</span>"
    elif score >= 0.5:
        return f"<span class='score-medium'>{score:.1%}</span>"
    else:
        return f"<span class='score-low'>{score:.1%}</span>"

def main():
    # Header
    st.markdown("<h1 class='main-header'>🎯 Decision AI Recruiter</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #666;'>Sistema Inteligente de Recrutamento e Seleção</p>", unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🔧 Painel de Controle")
    page = st.sidebar.selectbox(
        "Selecione uma funcionalidade:",
        [
            "📊 Dashboard Executivo",
            "🎯 Matching Candidato-Vaga", 
            "🤖 Entrevista com IA",
            "📈 Análise de Perfis",
            "👥 Clusters de Sucesso"
        ]
    )
    
    # Carregar dados
    candidates, jobs, interviews = load_data()
    
    if not candidates:
        st.error("Dados não encontrados. Execute primeiro o script de geração de dados.")
        return
    
    # Roteamento de páginas
    if page == "📊 Dashboard Executivo":
        show_dashboard(candidates, jobs, interviews)
    elif page == "🎯 Matching Candidato-Vaga":
        show_matching(candidates, jobs)
    elif page == "🤖 Entrevista com IA":
        show_ai_interview(candidates, jobs)
    elif page == "📈 Análise de Perfis":
        show_profile_analysis(candidates, jobs, interviews)
    elif page == "👥 Clusters de Sucesso":
        show_clustering_analysis(candidates)

def show_dashboard(candidates, jobs, interviews):
    """Dashboard executivo"""
    st.header("📊 Dashboard Executivo")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Candidatos", len(candidates))
    
    with col2:
        active_jobs = len([j for j in jobs if j['status'] == 'Aberta'])
        st.metric("Vagas Ativas", active_jobs)
    
    with col3:
        approved_interviews = len([i for i in interviews if i['aprovado']])
        approval_rate = approved_interviews / len(interviews) if interviews else 0
        st.metric("Taxa de Aprovação", f"{approval_rate:.1%}")
    
    with col4:
        avg_score = np.mean([c['taxa_sucesso'] for c in candidates])
        st.metric("Score Médio Candidatos", f"{avg_score:.1%}")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição por nível
        nivel_counts = pd.Series([c['nivel'] for c in candidates]).value_counts()
        fig_nivel = px.pie(
            values=nivel_counts.values, 
            names=nivel_counts.index,
            title="Distribuição de Candidatos por Nível"
        )
        st.plotly_chart(fig_nivel, use_container_width=True)
    
    with col2:
        # Distribuição por área
        area_counts = pd.Series([c['area_atuacao'] for c in candidates]).value_counts()
        fig_area = px.bar(
            x=area_counts.index, 
            y=area_counts.values,
            title="Candidatos por Área de Atuação"
        )
        fig_area.update_layout(xaxis_title="Área", yaxis_title="Quantidade")
        st.plotly_chart(fig_area, use_container_width=True)
    
    # Análise temporal
    st.subheader("📈 Tendências Temporais")
    
    # Conversão de datas
    interviews_df = pd.DataFrame(interviews)
    if not interviews_df.empty:
        interviews_df['data_entrevista'] = pd.to_datetime(interviews_df['data_entrevista'])
        interviews_df['mes'] = interviews_df['data_entrevista'].dt.to_period('M')
        
        monthly_stats = interviews_df.groupby('mes').agg({
            'aprovado': ['count', 'sum']
        }).reset_index()
        
        monthly_stats.columns = ['mes', 'total_entrevistas', 'aprovadas']
        monthly_stats['taxa_aprovacao'] = monthly_stats['aprovadas'] / monthly_stats['total_entrevistas']
        monthly_stats['mes'] = monthly_stats['mes'].astype(str)
        
        fig_timeline = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_timeline.add_trace(
            go.Bar(x=monthly_stats['mes'], y=monthly_stats['total_entrevistas'], 
                  name="Total Entrevistas", opacity=0.7),
            secondary_y=False,
        )
        
        fig_timeline.add_trace(
            go.Scatter(x=monthly_stats['mes'], y=monthly_stats['taxa_aprovacao'], 
                      mode='lines+markers', name="Taxa de Aprovação"),
            secondary_y=True,
        )
        
        fig_timeline.update_xaxes(title_text="Mês")
        fig_timeline.update_yaxes(title_text="Número de Entrevistas", secondary_y=False)
        fig_timeline.update_yaxes(title_text="Taxa de Aprovação", secondary_y=True)
        fig_timeline.update_layout(title_text="Evolução Mensal - Entrevistas e Aprovações")
        
        st.plotly_chart(fig_timeline, use_container_width=True)

def show_matching(candidates, jobs):
    """Sistema de matching candidato-vaga"""
    st.header("🎯 Sistema de Matching Candidato-Vaga")
    
    # Selecionar vaga
    active_jobs = [j for j in jobs if j['status'] == 'Aberta']
    
    if not active_jobs:
        st.warning("Nenhuma vaga ativa encontrada.")
        return
    
    job_options = {f"{job['titulo']} - {job['empresa']}": job['id'] for job in active_jobs}
    selected_job_name = st.selectbox("Selecione uma vaga:", list(job_options.keys()))
    selected_job_id = job_options[selected_job_name]
    
    # Encontrar vaga selecionada
    selected_job = next(j for j in active_jobs if j['id'] == selected_job_id)
    
    # Carregar matcher
    matcher = load_matcher()
    if not matcher:
        st.error("Erro ao carregar sistema de matching.")
        return
    
    # Encontrar matches
    with st.spinner("Analisando candidatos..."):
        matches = matcher.find_best_matches(selected_job_id, top_n=10)
    
    # Mostrar detalhes da vaga
    st.subheader("📋 Detalhes da Vaga")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Título:** {selected_job['titulo']}")
        st.write(f"**Empresa:** {selected_job['empresa']}")
        st.write(f"**Nível:** {selected_job['nivel_requerido']}")
        st.write(f"**Área:** {selected_job['area']}")
        st.write(f"**Experiência:** {selected_job['anos_experiencia_min']}-{selected_job['anos_experiencia_max']} anos")
    
    with col2:
        st.write(f"**Salário:** R$ {selected_job['salario_min']:,} - R$ {selected_job['salario_max']:,}")
        st.write(f"**Modelo:** {selected_job['modelo_trabalho']}")
        st.write(f"**Local:** {selected_job['cidade']}, {selected_job['estado']}")
        st.write(f"**Skills obrigatórias:** {', '.join(selected_job['tecnologias_obrigatorias'][:3])}")
    
    # Mostrar matches
    st.subheader(f"🏆 Top {len(matches)} Candidatos Compatíveis")
    
    for i, match in enumerate(matches, 1):
        candidate = match['candidato']
        
        with st.expander(f"#{i} - {candidate['nome']} (Score: {match['final_score']:.3f})"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**Informações Básicas:**")
                st.write(f"- Idade: {candidate['idade']} anos")
                st.write(f"- Experiência: {candidate['anos_experiencia']} anos")
                st.write(f"- Nível: {candidate['nivel']}")
                st.write(f"- Área: {candidate['area_atuacao']}")
                st.write(f"- Local: {candidate['cidade']}, {candidate['estado']}")
            
            with col2:
                st.write("**Scores de Compatibilidade:**")
                st.markdown(f"- Score Final: {format_score(match['final_score'])}", unsafe_allow_html=True)
                st.markdown(f"- Compatibilidade: {format_score(match['compatibility_score'])}", unsafe_allow_html=True)
                st.markdown(f"- Prob. Sucesso: {format_score(match['success_probability'])}", unsafe_allow_html=True)
                st.markdown(f"- Taxa Histórica: {format_score(candidate['taxa_sucesso'])}", unsafe_allow_html=True)
            
            with col3:
                st.write("**Principais Motivos:**")
                for motivo in match['motivos_match'][:4]:
                    st.write(f"✅ {motivo}")
            
            # Botão para entrevista
            if st.button(f"📅 Agendar Entrevista - {candidate['nome']}", key=f"interview_{candidate['id']}"):
                st.session_state.interview_candidate = candidate
                st.session_state.interview_job = selected_job
                st.success(f"Entrevista agendada para {candidate['nome']}!")

def show_ai_interview(candidates, jobs):
    """Sistema de entrevista com IA"""
    st.header("🤖 Entrevista Automatizada com IA")
    
    # Verificar se há entrevista agendada
    if 'interview_candidate' in st.session_state and 'interview_job' in st.session_state:
        candidate = st.session_state.interview_candidate
        job = st.session_state.interview_job
        
        st.success(f"Entrevista agendada: {candidate['nome']} para {job['titulo']}")
        
        if st.button("🎯 Gerar Roteiro de Entrevista"):
            interviewer = AIInterviewer()
            
            with st.spinner("Gerando roteiro personalizado..."):
                report = interviewer.generate_interview_report(candidate, job)
            
            # Mostrar informações da entrevista
            st.subheader("📋 Informações da Entrevista")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Candidato:** {candidate['nome']}")
                st.write(f"**Vaga:** {job['titulo']}")
                st.write(f"**Duração estimada:** {report['interview_script']['estimated_duration']}")
            
            with col2:
                st.write(f"**Área:** {job['area']}")
                st.write(f"**Nível:** {job['nivel_requerido']}")
                st.write(f"**Experiência candidato:** {candidate['anos_experiencia']} anos")
            
            # Roteiro da entrevista
            st.subheader("📝 Roteiro da Entrevista")
            
            for section in report['interview_script']['interview_sections']:
                with st.expander(f"{section['name']} ({section['duration']})"):
                    st.write(f"**Objetivos:** {', '.join(section['objectives'])}")
                    
                    if 'questions' in section:
                        st.write("**Perguntas:**")
                        for i, question in enumerate(section['questions'], 1):
                            st.write(f"{i}. {question}")
                    
                    if 'script' in section:
                        st.write("**Script:**")
                        for item in section['script']:
                            st.write(f"• {item}")
            
            # Formulário de avaliação simulada
            st.subheader("📊 Simulação de Avaliação")
            
            evaluation = report['evaluation']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Scores por Categoria:**")
                for category, details in evaluation.items():
                    if category != 'final_recommendation':
                        score = details['overall_score']
                        weight = details.get('weight', 0)
                        st.markdown(f"- **{category.title()}:** {score:.1f}/5.0 (peso: {weight:.0%})", unsafe_allow_html=True)
            
            with col2:
                final = evaluation['final_recommendation']
                st.write("**Resultado Final:**")
                st.markdown(f"- **Score Final:** {final['overall_score']:.1f}/5.0")
                st.markdown(f"- **Aprovado:** {'✅ Sim' if final['approved'] else '❌ Não'}")
                st.write(f"- **Feedback:** {final['general_feedback']}")
            
            # Pontos fortes e melhorias
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**💪 Pontos Fortes:**")
                for strength in evaluation['final_recommendation']['strengths']:
                    st.write(f"✅ {strength}")
            
            with col2:
                st.write("**📈 Áreas de Melhoria:**")
                for improvement in evaluation['final_recommendation']['improvement_areas']:
                    st.write(f"🔧 {improvement}")
            
            # Download do relatório (apenas quando solicitado)
            if st.button("📄 Gerar Relatório para Download"):
                report_json = json.dumps(report, ensure_ascii=False, indent=2)
                st.download_button(
                    "📥 Baixar Relatório JSON",
                    report_json,
                    f"entrevista_{candidate['nome'].replace(' ', '_')}_{job['titulo'].replace(' ', '_')}.json",
                    "application/json",
                    key="download_report"
                )
    
    else:
        st.info("Selecione um candidato na página de Matching para agendar uma entrevista.")
        
        # Opção manual de seleção
        st.subheader("🔧 Seleção Manual")
        
        col1, col2 = st.columns(2)
        
        with col1:
            candidate_options = {f"{c['nome']} ({c['nivel']} {c['area_atuacao']})": c for c in candidates}
            selected_candidate_name = st.selectbox("Selecione um candidato:", list(candidate_options.keys()))
            selected_candidate = candidate_options[selected_candidate_name]
        
        with col2:
            job_options = {f"{j['titulo']} - {j['empresa']}": j for j in jobs}
            selected_job_name = st.selectbox("Selecione uma vaga:", list(job_options.keys()))
            selected_job = job_options[selected_job_name]
        
        if st.button("🎯 Iniciar Entrevista"):
            st.session_state.interview_candidate = selected_candidate
            st.session_state.interview_job = selected_job
            st.rerun()

def show_profile_analysis(candidates, jobs, interviews):
    """Análise de perfis de candidatos"""
    st.header("📈 Análise de Perfis de Candidatos")
    
    # Filtros
    st.subheader("🔍 Filtros")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        areas = list(set([c['area_atuacao'] for c in candidates]))
        selected_areas = st.multiselect("Áreas:", areas, default=areas[:3])
    
    with col2:
        niveis = list(set([c['nivel'] for c in candidates]))
        selected_niveis = st.multiselect("Níveis:", niveis, default=niveis[:3])
    
    with col3:
        exp_range = st.slider("Anos de Experiência:", 0, 20, (0, 10))
    
    # Filtrar dados
    filtered_candidates = [
        c for c in candidates 
        if c['area_atuacao'] in selected_areas 
        and c['nivel'] in selected_niveis
        and exp_range[0] <= c['anos_experiencia'] <= exp_range[1]
    ]
    
    if not filtered_candidates:
        st.warning("Nenhum candidato encontrado com os filtros selecionados.")
        return
    
    # Análises
    st.subheader(f"📊 Análise de {len(filtered_candidates)} Candidatos")
    
    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_success = np.mean([c['taxa_sucesso'] for c in filtered_candidates])
        st.metric("Taxa Sucesso Média", f"{avg_success:.1%}")
    
    with col2:
        avg_experience = np.mean([c['anos_experiencia'] for c in filtered_candidates])
        st.metric("Experiência Média", f"{avg_experience:.1f} anos")
    
    with col3:
        avg_salary = np.mean([c['pretensao_salarial'] for c in filtered_candidates])
        st.metric("Salário Médio", f"R$ {avg_salary:,.0f}")
    
    with col4:
        avg_technical = np.mean([c['score_tecnico'] for c in filtered_candidates])
        st.metric("Score Técnico Médio", f"{avg_technical:.2f}")
    
    # Gráficos de correlação
    col1, col2 = st.columns(2)
    
    with col1:
        # Correlação experiência vs sucesso
        exp_data = [c['anos_experiencia'] for c in filtered_candidates]
        success_data = [c['taxa_sucesso'] for c in filtered_candidates]
        
        fig_exp = px.scatter(
            x=exp_data, y=success_data,
            title="Experiência vs Taxa de Sucesso",
            labels={"x": "Anos de Experiência", "y": "Taxa de Sucesso"}
        )
        st.plotly_chart(fig_exp, use_container_width=True)
    
    with col2:
        # Distribuição de scores
        scores_data = []
        for c in filtered_candidates:
            scores_data.extend([
                {"Score": "Técnico", "Valor": c['score_tecnico']},
                {"Score": "Comunicação", "Valor": c['score_comunicacao']},
                {"Score": "Fit Cultural", "Valor": c['score_fit_cultural']},
                {"Score": "Engajamento", "Valor": c['score_engajamento']}
            ])
        
        scores_df = pd.DataFrame(scores_data)
        fig_scores = px.box(scores_df, x="Score", y="Valor", title="Distribuição de Scores")
        st.plotly_chart(fig_scores, use_container_width=True)
    
    # Ranking dos melhores candidatos
    st.subheader("🏆 Top Candidatos")
    
    # Calcular score composto
    for c in filtered_candidates:
        c['score_composto'] = (
            c['score_tecnico'] * 0.3 +
            c['score_comunicacao'] * 0.25 +
            c['score_fit_cultural'] * 0.25 +
            c['score_engajamento'] * 0.2
        )
    
    top_candidates = sorted(filtered_candidates, key=lambda x: x['score_composto'], reverse=True)[:10]
    
    for i, candidate in enumerate(top_candidates, 1):
        with st.expander(f"#{i} - {candidate['nome']} (Score: {candidate['score_composto']:.3f})"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Área:** {candidate['area_atuacao']}")
                st.write(f"**Nível:** {candidate['nivel']}")
                st.write(f"**Experiência:** {candidate['anos_experiencia']} anos")
                st.write(f"**Idade:** {candidate['idade']} anos")
            
            with col2:
                st.markdown(f"**Score Técnico:** {format_score(candidate['score_tecnico'])}", unsafe_allow_html=True)
                st.markdown(f"**Score Comunicação:** {format_score(candidate['score_comunicacao'])}", unsafe_allow_html=True)
                st.markdown(f"**Score Cultural:** {format_score(candidate['score_fit_cultural'])}", unsafe_allow_html=True)
                st.markdown(f"**Score Engajamento:** {format_score(candidate['score_engajamento'])}", unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"**Taxa Sucesso:** {format_score(candidate['taxa_sucesso'])}", unsafe_allow_html=True)
                st.write(f"**Pretensão:** R$ {candidate['pretensao_salarial']:,}")
                st.write(f"**Tecnologias:** {len(candidate['tecnologias'])}")
                st.write(f"**Certificações:** {candidate['certificacoes']}")

def show_clustering_analysis(candidates):
    """Análise de clusters de candidatos"""
    st.header("👥 Análise de Clusters de Sucesso")
    
    # Carregar matcher para análise de clusters
    matcher = load_matcher()
    if not matcher:
        st.error("Erro ao carregar sistema de análise.")
        return
    
    with st.spinner("Analisando clusters de candidatos..."):
        cluster_analysis = matcher.analyze_candidate_clusters()
    
    st.subheader("📊 Clusters Identificados")
    
    # Métricas gerais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Número de Clusters", len(cluster_analysis))
    
    with col2:
        best_cluster = max(cluster_analysis.values(), key=lambda x: x['avg_success_rate'])
        st.metric("Melhor Taxa de Sucesso", f"{best_cluster['avg_success_rate']:.1%}")
    
    with col3:
        total_candidates = sum([c['size'] for c in cluster_analysis.values()])
        st.metric("Total de Candidatos", total_candidates)
    
    # Análise detalhada por cluster
    for cluster_id, analysis in cluster_analysis.items():
        with st.expander(f"🎯 {cluster_id.upper()} - {analysis['size']} candidatos"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Características Principais:**")
                st.write(f"- Taxa de Sucesso: {analysis['avg_success_rate']:.1%}")
                st.write(f"- Experiência Média: {analysis['avg_experience']:.1f} anos")
                st.write(f"- Score Técnico: {analysis['avg_technical_score']:.2f}")
                st.write(f"- Salário Médio: R$ {analysis['avg_salary']:,.0f}")
            
            with col2:
                st.write("**Características Distintivas:**")
                if analysis['characteristics']:
                    for feature, details in list(analysis['characteristics'].items())[:5]:
                        diff = details['difference']
                        symbol = "📈" if diff > 0 else "📉"
                        st.write(f"{symbol} {feature}: {details['cluster_avg']:.2f}")
                else:
                    st.write("Cluster com características médias.")
    
    # Visualização dos clusters
    st.subheader("📈 Visualização dos Clusters")
    
    # Preparar dados para visualização
    cluster_data = []
    for cluster_id, analysis in cluster_analysis.items():
        cluster_data.append({
            'Cluster': cluster_id.replace('cluster_', 'Cluster ').upper(),
            'Taxa de Sucesso': analysis['avg_success_rate'],
            'Experiência Média': analysis['avg_experience'],
            'Score Técnico': analysis['avg_technical_score'],
            'Tamanho': analysis['size']
        })
    
    cluster_df = pd.DataFrame(cluster_data)
    
    # Gráfico de bolhas
    fig_bubble = px.scatter(
        cluster_df, 
        x='Experiência Média', 
        y='Taxa de Sucesso',
        size='Tamanho',
        color='Score Técnico',
        hover_name='Cluster',
        title="Clusters: Experiência vs Taxa de Sucesso",
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig_bubble, use_container_width=True)
    
    # Recomendações baseadas nos clusters
    st.subheader("💡 Recomendações")
    
    best_cluster_id = max(cluster_analysis.keys(), key=lambda x: cluster_analysis[x]['avg_success_rate'])
    best_cluster = cluster_analysis[best_cluster_id]
    
    st.success(f"""
    **Perfil de Maior Sucesso ({best_cluster_id.upper()}):**
    - Taxa de sucesso: {best_cluster['avg_success_rate']:.1%}
    - Experiência média: {best_cluster['avg_experience']:.1f} anos
    - Score técnico: {best_cluster['avg_technical_score']:.2f}
    
    💡 **Recomendação:** Priorizar candidatos com perfil similar ao {best_cluster_id.upper()} 
    para aumentar as chances de sucesso nas contratações.
    """)

if __name__ == "__main__":
    main()
