import json
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
import joblib
import warnings
warnings.filterwarnings('ignore')

class CandidateJobMatcher:
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.kmeans_model = KMeans(n_clusters=5, random_state=42)
        
    def load_data(self):
        """Carrega e processa os dados"""
        with open('/Users/joaopaulolucchi/Desktop/tech_05/data/applicants.json', 'r', encoding='utf-8') as f:
            self.candidates = json.load(f)
        
        with open('/Users/joaopaulolucchi/Desktop/tech_05/data/vagas.json', 'r', encoding='utf-8') as f:
            self.jobs = json.load(f)
            
        with open('/Users/joaopaulolucchi/Desktop/tech_05/data/prospects.json', 'r', encoding='utf-8') as f:
            self.interviews = json.load(f)
        
        self.candidates_df = pd.DataFrame(self.candidates)
        self.jobs_df = pd.DataFrame(self.jobs)
        self.interviews_df = pd.DataFrame(self.interviews)
        
        print(f"✅ Dados carregados: {len(self.candidates)} candidatos, {len(self.jobs)} vagas, {len(self.interviews)} entrevistas")
    
    def preprocess_features(self):
        """Preprocessa features para machine learning"""
        # Criar features numéricas para candidatos
        candidates_features = []
        
        for candidate in self.candidates:
            # Features básicas
            features = {
                'idade': candidate['idade'],
                'anos_experiencia': candidate['anos_experiencia'],
                'salario_atual': candidate['salario_atual'],
                'pretensao_salarial': candidate['pretensao_salarial'],
                'projetos_github': candidate['projetos_github'],
                'certificacoes': candidate['certificacoes'],
                'total_entrevistas': candidate['total_entrevistas'],
                'entrevistas_aprovadas': candidate['entrevistas_aprovadas'],
                'taxa_sucesso': candidate['taxa_sucesso'],
                'score_tecnico': candidate['score_tecnico'],
                'score_fit_cultural': candidate['score_fit_cultural'],
                'score_engajamento': candidate['score_engajamento'],
                'score_comunicacao': candidate['score_comunicacao'],
                'feedback_positivo': candidate['feedback_positivo'],
                'feedback_negativo': candidate['feedback_negativo']
            }
            
            # Encoding de features categóricas
            for cat_feature in ['formacao', 'nivel', 'area_atuacao', 'nivel_ingles', 'disponibilidade', 'modelo_trabalho']:
                if cat_feature not in self.label_encoders:
                    self.label_encoders[cat_feature] = LabelEncoder()
                    # Fit com todos os valores únicos
                    all_values = list(set([c[cat_feature] for c in self.candidates]))
                    self.label_encoders[cat_feature].fit(all_values)
                
                features[f'{cat_feature}_encoded'] = self.label_encoders[cat_feature].transform([candidate[cat_feature]])[0]
            
            # Features binárias
            features['aceita_viagem'] = int(candidate['aceita_viagem'])
            features['aceita_mudanca'] = int(candidate['aceita_mudanca'])
            features['status_ativo'] = int(candidate['status'] == 'Ativo')
            
            # Contar tecnologias e soft skills
            features['num_tecnologias'] = len(candidate['tecnologias'])
            features['num_soft_skills'] = len(candidate['soft_skills'])
            
            # Features derivadas
            features['experiencia_por_idade'] = candidate['anos_experiencia'] / candidate['idade']
            features['projetos_por_experiencia'] = candidate['projetos_github'] / max(1, candidate['anos_experiencia'])
            features['score_medio'] = (candidate['score_tecnico'] + candidate['score_fit_cultural'] + 
                                     candidate['score_engajamento'] + candidate['score_comunicacao']) / 4
            
            candidates_features.append(features)
        
        return pd.DataFrame(candidates_features)
    
    def calculate_compatibility_score(self, candidate, job):
        """Calcula score de compatibilidade entre candidato e vaga"""
        score = 0.0
        weights = {
            'experience': 0.25,
            'skills': 0.30,
            'salary': 0.15,
            'location': 0.10,
            'soft_skills': 0.20
        }
        
        # Score de experiência
        exp_diff = abs(candidate['anos_experiencia'] - job['anos_experiencia_min'])
        exp_score = max(0, 1 - exp_diff / 10)  # Normalizado
        score += weights['experience'] * exp_score
        
        # Score de skills técnicas
        candidate_skills = set(candidate['tecnologias'])
        required_skills = set(job['tecnologias_obrigatorias'])
        desired_skills = set(job['tecnologias_desejaveis'])
        
        if required_skills:
            required_match = len(candidate_skills.intersection(required_skills)) / len(required_skills)
        else:
            required_match = 1.0
            
        if desired_skills:
            desired_match = len(candidate_skills.intersection(desired_skills)) / len(desired_skills)
        else:
            desired_match = 1.0
            
        skills_score = 0.7 * required_match + 0.3 * desired_match
        score += weights['skills'] * skills_score
        
        # Score salarial
        if job['salario_min'] <= candidate['pretensao_salarial'] <= job['salario_max']:
            salary_score = 1.0
        else:
            # Penalizar baseado na distância da faixa
            if candidate['pretensao_salarial'] < job['salario_min']:
                salary_score = candidate['pretensao_salarial'] / job['salario_min']
            else:
                salary_score = job['salario_max'] / candidate['pretensao_salarial']
        
        score += weights['salary'] * salary_score
        
        # Score de localização/modelo de trabalho
        location_score = 1.0 if (candidate['modelo_trabalho'] == job['modelo_trabalho'] or 
                               job['modelo_trabalho'] == 'Híbrido' or 
                               candidate['modelo_trabalho'] == 'Híbrido') else 0.5
        score += weights['location'] * location_score
        
        # Score de soft skills
        candidate_soft = set(candidate['soft_skills'])
        required_soft = set(job.get('soft_skills_obrigatorias', []))
        
        if required_soft:
            soft_score = len(candidate_soft.intersection(required_soft)) / len(required_soft)
        else:
            soft_score = 1.0
            
        score += weights['soft_skills'] * soft_score
        
        return min(1.0, score)  # Garantir que não passe de 1.0
    
    def train_success_prediction_model(self):
        """Treina modelo para prever sucesso em entrevistas"""
        # Preparar dados de treinamento
        training_data = []
        
        for interview in self.interviews:
            # Encontrar candidato e vaga correspondentes
            candidate = next((c for c in self.candidates if c['id'] == interview['candidato_id']), None)
            job = next((j for j in self.jobs if j['id'] == interview['vaga_id']), None)
            
            if candidate and job:
                compatibility = self.calculate_compatibility_score(candidate, job)
                
                features = {
                    'compatibility_score': compatibility,
                    'score_tecnico_hist': candidate['score_tecnico'],
                    'score_fit_cultural_hist': candidate['score_fit_cultural'],
                    'score_engajamento_hist': candidate['score_engajamento'],
                    'score_comunicacao_hist': candidate['score_comunicacao'],
                    'taxa_sucesso_hist': candidate['taxa_sucesso'],
                    'anos_experiencia': candidate['anos_experiencia'],
                    'nivel_match': 1 if candidate['nivel'] == job['nivel_requerido'] else 0,
                    'area_match': 1 if candidate['area_atuacao'] == job['area'] else 0,
                    'salario_fit': 1 if job['salario_min'] <= candidate['pretensao_salarial'] <= job['salario_max'] else 0
                }
                
                features['success'] = interview['aprovado']
                training_data.append(features)
        
        training_df = pd.DataFrame(training_data)
        
        # Separar features e target
        feature_cols = [col for col in training_df.columns if col != 'success']
        X = training_df[feature_cols]
        y = training_df['success']
        
        # Dividir em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Treinar modelo
        self.rf_model.fit(X_train, y_train)
        
        # Avaliar modelo
        train_score = self.rf_model.score(X_train, y_train)
        test_score = self.rf_model.score(X_test, y_test)
        
        print(f"✅ Modelo treinado - Acurácia treino: {train_score:.3f}, Acurácia teste: {test_score:.3f}")
        
        # Salvar feature columns para predição
        self.feature_columns = feature_cols
        
        return train_score, test_score
    
    def predict_interview_success(self, candidate, job):
        """Prediz probabilidade de sucesso em entrevista"""
        compatibility = self.calculate_compatibility_score(candidate, job)
        
        features = {
            'compatibility_score': compatibility,
            'score_tecnico_hist': candidate['score_tecnico'],
            'score_fit_cultural_hist': candidate['score_fit_cultural'],
            'score_engajamento_hist': candidate['score_engajamento'],
            'score_comunicacao_hist': candidate['score_comunicacao'],
            'taxa_sucesso_hist': candidate['taxa_sucesso'],
            'anos_experiencia': candidate['anos_experiencia'],
            'nivel_match': 1 if candidate['nivel'] == job['nivel_requerido'] else 0,
            'area_match': 1 if candidate['area_atuacao'] == job['area'] else 0,
            'salario_fit': 1 if job['salario_min'] <= candidate['pretensao_salarial'] <= job['salario_max'] else 0
        }
        
        feature_array = np.array([[features[col] for col in self.feature_columns]])
        probability = self.rf_model.predict_proba(feature_array)[0][1]  # Probabilidade de sucesso
        
        return probability
    
    def find_best_matches(self, job_id, top_n=10):
        """Encontra os melhores candidatos para uma vaga"""
        job = next((j for j in self.jobs if j['id'] == job_id), None)
        if not job:
            return []
        
        matches = []
        
        for candidate in self.candidates:
            if candidate['status'] != 'Ativo':
                continue
                
            compatibility = self.calculate_compatibility_score(candidate, job)
            success_probability = self.predict_interview_success(candidate, job)
            
            # Score final combinado
            final_score = 0.6 * compatibility + 0.4 * success_probability
            
            matches.append({
                'candidato': candidate,
                'compatibility_score': compatibility,
                'success_probability': success_probability,
                'final_score': final_score,
                'motivos_match': self._generate_match_reasons(candidate, job)
            })
        
        # Ordenar por score final
        matches.sort(key=lambda x: x['final_score'], reverse=True)
        
        return matches[:top_n]
    
    def _generate_match_reasons(self, candidate, job):
        """Gera explicações do match"""
        reasons = []
        
        # Skills match
        candidate_skills = set(candidate['tecnologias'])
        required_skills = set(job['tecnologias_obrigatorias'])
        matched_skills = candidate_skills.intersection(required_skills)
        
        if matched_skills:
            reasons.append(f"Possui skills obrigatórias: {', '.join(list(matched_skills)[:3])}")
        
        # Experiência
        if job['anos_experiencia_min'] <= candidate['anos_experiencia'] <= job['anos_experiencia_max']:
            reasons.append(f"Experiência adequada ({candidate['anos_experiencia']} anos)")
        
        # Nível
        if candidate['nivel'] == job['nivel_requerido']:
            reasons.append(f"Nível compatível ({candidate['nivel']})")
        
        # Salário
        if job['salario_min'] <= candidate['pretensao_salarial'] <= job['salario_max']:
            reasons.append("Expectativa salarial dentro da faixa")
        
        # Histórico de sucesso
        if candidate['taxa_sucesso'] > 0.7:
            reasons.append(f"Alto histórico de sucesso ({candidate['taxa_sucesso']:.0%})")
        
        return reasons
    
    def analyze_candidate_clusters(self):
        """Analisa clusters de candidatos para identificar perfis de sucesso"""
        features_df = self.preprocess_features()
        
        # Selecionar features numéricas para clustering
        numeric_features = features_df.select_dtypes(include=[np.number]).columns
        X_cluster = features_df[numeric_features]
        
        # Normalizar dados
        X_scaled = self.scaler.fit_transform(X_cluster)
        
        # Aplicar K-means
        clusters = self.kmeans_model.fit_predict(X_scaled)
        
        # Adicionar clusters ao dataframe
        features_df['cluster'] = clusters
        
        # Analisar características de cada cluster
        cluster_analysis = {}
        
        for cluster_id in range(self.kmeans_model.n_clusters):
            cluster_data = features_df[features_df['cluster'] == cluster_id]
            
            analysis = {
                'size': len(cluster_data),
                'avg_success_rate': cluster_data['taxa_sucesso'].mean(),
                'avg_experience': cluster_data['anos_experiencia'].mean(),
                'avg_salary': cluster_data['pretensao_salarial'].mean(),
                'avg_technical_score': cluster_data['score_tecnico'].mean(),
                'characteristics': {}
            }
            
            # Identificar características distintivas
            for col in numeric_features:
                if col in cluster_data.columns:
                    cluster_mean = cluster_data[col].mean()
                    overall_mean = features_df[col].mean()
                    
                    if abs(cluster_mean - overall_mean) > 0.5 * features_df[col].std():
                        analysis['characteristics'][col] = {
                            'cluster_avg': cluster_mean,
                            'overall_avg': overall_mean,
                            'difference': cluster_mean - overall_mean
                        }
            
            cluster_analysis[f'cluster_{cluster_id}'] = analysis
        
        return cluster_analysis
    
    def save_models(self):
        """Salva os modelos treinados"""
        joblib.dump(self.rf_model, '/Users/joaopaulolucchi/Desktop/tech_05/models/rf_model.pkl')
        joblib.dump(self.scaler, '/Users/joaopaulolucchi/Desktop/tech_05/models/scaler.pkl')
        joblib.dump(self.kmeans_model, '/Users/joaopaulolucchi/Desktop/tech_05/models/kmeans_model.pkl')
        joblib.dump(self.label_encoders, '/Users/joaopaulolucchi/Desktop/tech_05/models/label_encoders.pkl')
        joblib.dump(self.feature_columns, '/Users/joaopaulolucchi/Desktop/tech_05/models/feature_columns.pkl')
        
        print("✅ Modelos salvos com sucesso!")

def main():
    import os
    os.makedirs('/Users/joaopaulolucchi/Desktop/tech_05/models', exist_ok=True)
    
    # Inicializar e treinar sistema
    matcher = CandidateJobMatcher()
    matcher.load_data()
    
    # Treinar modelo de predição de sucesso
    train_acc, test_acc = matcher.train_success_prediction_model()
    
    # Analisar clusters
    cluster_analysis = matcher.analyze_candidate_clusters()
    
    # Salvar modelos
    matcher.save_models()
    
    # Teste do sistema
    print("\n🔍 Testando sistema de matching...")
    
    # Pegar primeira vaga ativa
    active_jobs = [job for job in matcher.jobs if job['status'] == 'Aberta']
    if active_jobs:
        test_job = active_jobs[0]
        matches = matcher.find_best_matches(test_job['id'], top_n=5)
        
        print(f"\n📋 Top 5 candidatos para vaga: {test_job['titulo']}")
        print("="*60)
        
        for i, match in enumerate(matches, 1):
            candidate = match['candidato']
            print(f"{i}. {candidate['nome']}")
            print(f"   Score Final: {match['final_score']:.3f}")
            print(f"   Compatibilidade: {match['compatibility_score']:.3f}")
            print(f"   Prob. Sucesso: {match['success_probability']:.3f}")
            print(f"   Razões: {', '.join(match['motivos_match'][:2])}")
            print()
    
    # Mostrar análise de clusters
    print("\n📊 Análise de Clusters de Candidatos:")
    print("="*50)
    
    for cluster_id, analysis in cluster_analysis.items():
        print(f"\n{cluster_id.upper()} (n={analysis['size']}):")
        print(f"  Taxa de Sucesso Média: {analysis['avg_success_rate']:.1%}")
        print(f"  Experiência Média: {analysis['avg_experience']:.1f} anos")
        print(f"  Score Técnico Médio: {analysis['avg_technical_score']:.2f}")
    
    print(f"\n✅ Sistema treinado e testado com sucesso!")
    print(f"   - Acurácia do modelo: {test_acc:.1%}")
    print(f"   - {len(cluster_analysis)} clusters identificados")

if __name__ == "__main__":
    main()
