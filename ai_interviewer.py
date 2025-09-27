import json
import random
from datetime import datetime
import re

class AIInterviewer:
    def __init__(self):
        self.interview_templates = self._load_interview_templates()
        self.evaluation_criteria = self._load_evaluation_criteria()
        
    def _load_interview_templates(self):
        """Templates de perguntas por área e nível"""
        return {
            "technical": {
                "Junior": [
                    "Explique a diferença entre uma lista e um dicionário em Python.",
                    "O que é versionamento de código e por que é importante?",
                    "Como você debugaria um erro em seu código?",
                    "Qual a diferença entre GET e POST em APIs REST?",
                    "O que é um algoritmo de ordenação? Cite um exemplo.",
                ],
                "Pleno": [
                    "Como você implementaria um cache distribuído em uma aplicação?",
                    "Explique os princípios SOLID e dê um exemplo prático.",
                    "Como você otimizaria uma consulta SQL lenta?",
                    "Qual sua experiência com containerização (Docker/Kubernetes)?",
                    "Como você lidaria com alta concorrência em uma aplicação web?",
                ],
                "Senior": [
                    "Como você arquitetaria um sistema de microserviços escalável?",
                    "Explique diferentes padrões de design e quando aplicá-los.",
                    "Como você implementaria um sistema de backup e disaster recovery?",
                    "Qual sua abordagem para refatoração de código legado?",
                    "Como você garantiria segurança em uma arquitetura distribuída?",
                ]
            },
            "behavioral": [
                "Conte sobre um desafio técnico complexo que você resolveu.",
                "Como você lida com pressão e prazos apertados?",
                "Descreva uma situação onde teve que trabalhar em equipe.",
                "Como você se mantém atualizado com novas tecnologias?",
                "Conte sobre um erro que cometeu e como lidou com ele.",
                "Qual foi seu maior aprendizado profissional recente?",
                "Como você resolveria um conflito com um colega de equipe?",
                "O que te motiva profissionalmente?",
            ],
            "cultural": [
                "O que você sabe sobre nossa empresa e cultura?",
                "Como você se vê contribuindo para nossa equipe?",
                "Quais são seus objetivos de carreira a longo prazo?",
                "O que é mais importante para você em um ambiente de trabalho?",
                "Como você lida com feedback construtivo?",
                "Descreva seu estilo de trabalho ideal.",
            ]
        }
    
    def _load_evaluation_criteria(self):
        """Critérios de avaliação estruturados"""
        return {
            "technical": {
                "weight": 0.35,
                "criteria": [
                    "Conhecimento técnico adequado ao nível",
                    "Capacidade de resolver problemas",
                    "Experiência com tecnologias relevantes",
                    "Pensamento lógico e estruturado",
                    "Conhecimento de boas práticas"
                ]
            },
            "communication": {
                "weight": 0.25,
                "criteria": [
                    "Clareza na comunicação",
                    "Capacidade de explicar conceitos técnicos",
                    "Escuta ativa",
                    "Confiança ao responder",
                    "Estruturação do pensamento"
                ]
            },
            "cultural_fit": {
                "weight": 0.25,
                "criteria": [
                    "Alinhamento com valores da empresa",
                    "Atitude colaborativa",
                    "Adaptabilidade",
                    "Proatividade",
                    "Interesse genuíno na vaga"
                ]
            },
            "engagement": {
                "weight": 0.15,
                "criteria": [
                    "Motivação para a posição",
                    "Preparação para a entrevista",
                    "Perguntas relevantes sobre a empresa",
                    "Energia e entusiasmo",
                    "Compromisso a longo prazo"
                ]
            }
        }
    
    def generate_interview_script(self, candidate, job):
        """Gera roteiro personalizado de entrevista"""
        script = {
            "candidate_info": {
                "name": candidate["nome"],
                "level": candidate["nivel"],
                "area": candidate["area_atuacao"],
                "experience": candidate["anos_experiencia"]
            },
            "job_info": {
                "title": job["titulo"],
                "level": job["nivel_requerido"],
                "area": job["area"],
                "technologies": job["tecnologias_obrigatorias"]
            },
            "interview_sections": self._build_interview_sections(candidate, job),
            "evaluation_form": self._build_evaluation_form(),
            "estimated_duration": "45-60 minutos",
            "generated_at": datetime.now().isoformat()
        }
        
        return script
    
    def _build_interview_sections(self, candidate, job):
        """Constrói seções da entrevista"""
        sections = []
        
        # 1. Abertura (5 min)
        sections.append({
            "name": "Abertura",
            "duration": "5 min",
            "objectives": ["Quebrar o gelo", "Apresentar a empresa", "Explicar processo"],
            "script": [
                "Olá [NOME], seja bem-vindo(a)! Como está?",
                "Deixe-me apresentar nossa empresa e a vaga...",
                "Vou fazer algumas perguntas sobre sua experiência e conhecimentos técnicos.",
                "Sinta-se à vontade para fazer perguntas durante a conversa."
            ]
        })
        
        # 2. Apresentação do candidato (10 min)
        sections.append({
            "name": "Apresentação do Candidato",
            "duration": "10 min",
            "objectives": ["Conhecer trajetória", "Avaliar comunicação", "Identificar motivações"],
            "questions": [
                "Conte um pouco sobre sua trajetória profissional.",
                "O que te levou a se interessar por esta vaga?",
                "Quais são seus objetivos profissionais atuais?",
                f"Vi que você tem experiência em {candidate['area_atuacao']}. Pode detalhar?"
            ]
        })
        
        # 3. Perguntas técnicas (20 min)
        technical_questions = self._select_technical_questions(candidate, job)
        sections.append({
            "name": "Avaliação Técnica",
            "duration": "20 min",
            "objectives": ["Avaliar conhecimento técnico", "Verificar experiência prática"],
            "questions": technical_questions,
            "focus_areas": job["tecnologias_obrigatorias"]
        })
        
        # 4. Perguntas comportamentais (15 min)
        behavioral_questions = random.sample(self.interview_templates["behavioral"], 3)
        sections.append({
            "name": "Avaliação Comportamental",
            "duration": "15 min",
            "objectives": ["Avaliar soft skills", "Entender fit cultural"],
            "questions": behavioral_questions
        })
        
        # 5. Fit cultural (8 min)
        cultural_questions = random.sample(self.interview_templates["cultural"], 2)
        sections.append({
            "name": "Fit Cultural",
            "duration": "8 min",
            "objectives": ["Avaliar alinhamento cultural", "Entender motivações"],
            "questions": cultural_questions
        })
        
        # 6. Perguntas do candidato (7 min)
        sections.append({
            "name": "Perguntas do Candidato",
            "duration": "7 min",
            "objectives": ["Avaliar interesse", "Esclarecer dúvidas"],
            "script": [
                "Agora é sua vez! Que perguntas você tem sobre a vaga ou empresa?",
                "Observe o tipo e qualidade das perguntas para avaliar engajamento."
            ]
        })
        
        return sections
    
    def _select_technical_questions(self, candidate, job):
        """Seleciona perguntas técnicas baseadas no perfil"""
        level = job["nivel_requerido"]
        
        # Perguntas base por nível
        base_questions = self.interview_templates["technical"].get(level, 
                        self.interview_templates["technical"]["Junior"])
        
        # Selecionar 3-4 perguntas base
        selected_questions = random.sample(base_questions, min(3, len(base_questions)))
        
        # Adicionar perguntas específicas das tecnologias da vaga
        tech_questions = []
        for tech in job["tecnologias_obrigatorias"][:2]:  # Máximo 2 tecnologias
            tech_questions.extend(self._generate_tech_specific_questions(tech))
        
        # Combinar perguntas
        all_questions = selected_questions + tech_questions[:2]
        
        return all_questions
    
    def _generate_tech_specific_questions(self, technology):
        """Gera perguntas específicas por tecnologia"""
        tech_questions = {
            "Python": [
                "Como funciona o GIL (Global Interpreter Lock) no Python?",
                "Explique decorators e dê um exemplo prático.",
                "Qual a diferença entre lista e tupla?"
            ],
            "Java": [
                "Explique a diferença entre interface e classe abstrata.",
                "Como funciona o garbage collector no Java?",
                "O que são streams e como utilizá-las?"
            ],
            "JavaScript": [
                "Explique closures em JavaScript.",
                "Qual a diferença entre var, let e const?",
                "Como funciona o event loop?"
            ],
            "React": [
                "Explique o ciclo de vida dos componentes React.",
                "O que são hooks e quando usá-los?",
                "Como otimizar performance em aplicações React?"
            ],
            "Docker": [
                "Qual a diferença entre imagem e container?",
                "Como funciona o Docker networking?",
                "Explique o conceito de multi-stage builds."
            ],
            "AWS": [
                "Quais são os principais serviços AWS que você utilizou?",
                "Como funciona o Auto Scaling?",
                "Explique a diferença entre S3 e EBS."
            ]
        }
        
        return tech_questions.get(technology, [f"Qual sua experiência com {technology}?"])
    
    def _build_evaluation_form(self):
        """Constrói formulário de avaliação estruturado"""
        form = {}
        
        for category, details in self.evaluation_criteria.items():
            form[category] = {
                "weight": details["weight"],
                "criteria": {},
                "overall_score": 0,
                "comments": ""
            }
            
            # Cada critério tem score de 1-5
            for criterion in details["criteria"]:
                form[category]["criteria"][criterion] = {
                    "score": 0,
                    "notes": ""
                }
        
        form["final_recommendation"] = {
            "approved": False,
            "overall_score": 0,
            "strengths": [],
            "improvement_areas": [],
            "next_steps": "",
            "general_feedback": ""
        }
        
        return form
    
    def simulate_interview_evaluation(self, candidate, job):
        """Simula avaliação de entrevista com IA"""
        # Calcular scores baseado no perfil do candidato
        evaluation = self._build_evaluation_form()
        
        # Score técnico baseado em experiência e skills
        tech_score = self._calculate_technical_score(candidate, job)
        evaluation["technical"]["overall_score"] = tech_score
        
        # Score de comunicação baseado no histórico
        comm_score = min(5, candidate["score_comunicacao"] * 5)
        evaluation["communication"]["overall_score"] = comm_score
        
        # Score cultural baseado no fit
        cultural_score = min(5, candidate["score_fit_cultural"] * 5)
        evaluation["cultural_fit"]["overall_score"] = cultural_score
        
        # Score de engajamento
        engagement_score = min(5, candidate["score_engajamento"] * 5)
        evaluation["engagement"]["overall_score"] = engagement_score
        
        # Score final ponderado
        final_score = (
            tech_score * self.evaluation_criteria["technical"]["weight"] +
            comm_score * self.evaluation_criteria["communication"]["weight"] +
            cultural_score * self.evaluation_criteria["cultural_fit"]["weight"] +
            engagement_score * self.evaluation_criteria["engagement"]["weight"]
        )
        
        evaluation["final_recommendation"]["overall_score"] = round(final_score, 1)
        evaluation["final_recommendation"]["approved"] = final_score >= 3.5
        
        # Gerar feedback automático
        evaluation["final_recommendation"]["strengths"] = self._generate_strengths(candidate, job)
        evaluation["final_recommendation"]["improvement_areas"] = self._generate_improvements(candidate, job)
        evaluation["final_recommendation"]["general_feedback"] = self._generate_general_feedback(
            candidate, job, final_score
        )
        
        return evaluation
    
    def _calculate_technical_score(self, candidate, job):
        """Calcula score técnico baseado na compatibilidade"""
        # Compatibilidade de skills
        candidate_skills = set(candidate["tecnologias"])
        required_skills = set(job["tecnologias_obrigatorias"])
        
        if required_skills:
            skill_match = len(candidate_skills.intersection(required_skills)) / len(required_skills)
        else:
            skill_match = 1.0
        
        # Experiência vs requisito
        exp_match = min(1.0, candidate["anos_experiencia"] / max(1, job["anos_experiencia_min"]))
        
        # Score histórico técnico
        historical_score = candidate["score_tecnico"]
        
        # Combinar scores
        tech_score = (skill_match * 0.4 + exp_match * 0.3 + historical_score * 0.3) * 5
        
        return min(5, max(1, tech_score))
    
    def _generate_strengths(self, candidate, job):
        """Gera pontos fortes baseado no perfil"""
        strengths = []
        
        if candidate["score_tecnico"] > 0.7:
            strengths.append("Sólido conhecimento técnico")
        
        if candidate["score_comunicacao"] > 0.7:
            strengths.append("Excelente comunicação")
        
        if candidate["anos_experiencia"] >= job["anos_experiencia_min"]:
            strengths.append("Experiência adequada para a posição")
        
        if candidate["taxa_sucesso"] > 0.6:
            strengths.append("Histórico consistente de aprovações")
        
        if len(candidate["tecnologias"]) > 8:
            strengths.append("Amplo conhecimento em tecnologias")
        
        return strengths[:3]  # Máximo 3 pontos fortes
    
    def _generate_improvements(self, candidate, job):
        """Gera áreas de melhoria"""
        improvements = []
        
        if candidate["score_tecnico"] < 0.6:
            improvements.append("Aprofundar conhecimentos técnicos específicos")
        
        if candidate["score_comunicacao"] < 0.6:
            improvements.append("Desenvolver habilidades de comunicação")
        
        if candidate["anos_experiencia"] < job["anos_experiencia_min"]:
            improvements.append("Ganhar mais experiência prática")
        
        candidate_skills = set(candidate["tecnologias"])
        required_skills = set(job["tecnologias_obrigatorias"])
        missing_skills = required_skills - candidate_skills
        
        if missing_skills:
            improvements.append(f"Conhecimento em: {', '.join(list(missing_skills)[:2])}")
        
        return improvements[:2]  # Máximo 2 melhorias
    
    def _generate_general_feedback(self, candidate, job, final_score):
        """Gera feedback geral da entrevista"""
        if final_score >= 4.0:
            return f"Candidato demonstrou excelente adequação à vaga. Recomendado para próximas etapas."
        elif final_score >= 3.5:
            return f"Candidato apresentou boa compatibilidade com alguns pontos de atenção."
        elif final_score >= 2.5:
            return f"Candidato tem potencial mas precisa desenvolver algumas competências."
        else:
            return f"Candidato não atende aos requisitos básicos da posição no momento."
    
    def generate_interview_report(self, candidate, job):
        """Gera relatório completo da entrevista"""
        script = self.generate_interview_script(candidate, job)
        evaluation = self.simulate_interview_evaluation(candidate, job)
        
        report = {
            "interview_info": {
                "candidate_name": candidate["nome"],
                "job_title": job["titulo"],
                "date": datetime.now().isoformat(),
                "duration": "60 minutos",
                "interviewer": "Sistema IA Decision"
            },
            "interview_script": script,
            "evaluation": evaluation,
            "recommendations": {
                "proceed": evaluation["final_recommendation"]["approved"],
                "next_steps": "Enviar para próxima etapa" if evaluation["final_recommendation"]["approved"] 
                             else "Agradecer participação",
                "feedback_to_candidate": self._generate_candidate_feedback(evaluation)
            }
        }
        
        return report
    
    def _generate_candidate_feedback(self, evaluation):
        """Gera feedback para o candidato"""
        feedback = {
            "overall": evaluation["final_recommendation"]["general_feedback"],
            "strengths": evaluation["final_recommendation"]["strengths"],
            "development_areas": evaluation["final_recommendation"]["improvement_areas"],
            "suggestions": [
                "Continue desenvolvendo suas habilidades técnicas",
                "Pratique apresentações e comunicação técnica",
                "Mantenha-se atualizado com as tecnologias do mercado"
            ]
        }
        
        return feedback

# Função para teste
def test_ai_interviewer():
    # Carregar dados
    with open('/Users/joaopaulolucchi/Desktop/tech_05/data/applicants.json', 'r', encoding='utf-8') as f:
        candidates = json.load(f)
    
    with open('/Users/joaopaulolucchi/Desktop/tech_05/data/vagas.json', 'r', encoding='utf-8') as f:
        jobs = json.load(f)
    
    # Criar interviewer
    interviewer = AIInterviewer()
    
    # Testar com primeiro candidato e primeira vaga
    if candidates and jobs:
        candidate = candidates[0]
        job = jobs[0]
        
        print("🤖 Testando Agente de IA para Entrevistas")
        print("="*50)
        
        # Gerar relatório
        report = interviewer.generate_interview_report(candidate, job)
        
        print(f"📋 Entrevista: {candidate['nome']} para {job['titulo']}")
        print(f"⏱️  Duração estimada: {report['interview_script']['estimated_duration']}")
        print(f"📊 Score final: {report['evaluation']['final_recommendation']['overall_score']}/5")
        print(f"✅ Aprovado: {'Sim' if report['evaluation']['final_recommendation']['approved'] else 'Não'}")
        
        print("\n🎯 Seções da entrevista:")
        for section in report['interview_script']['interview_sections']:
            print(f"  - {section['name']} ({section['duration']})")
        
        print(f"\n💪 Pontos fortes:")
        for strength in report['evaluation']['final_recommendation']['strengths']:
            print(f"  - {strength}")
        
        print(f"\n📈 Áreas de melhoria:")
        for improvement in report['evaluation']['final_recommendation']['improvement_areas']:
            print(f"  - {improvement}")
        
        print(f"\n📄 Relatório gerado e testado com sucesso!")

if __name__ == "__main__":
    test_ai_interviewer()
