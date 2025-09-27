#!/usr/bin/env python3
"""
Script de deploy e configuração para o Decision AI Recruiter
"""

import subprocess
import sys
import os
import json
from pathlib import Path

def run_command(command, description=""):
    """Executa comando e mostra o resultado"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(f"✅ {description} - Concluído")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {description}: {e}")
        print(f"Saída de erro: {e.stderr}")
        return None

def check_requirements():
    """Verifica se todas as dependências estão instaladas"""
    print("📋 Verificando dependências...")
    
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'scikit-learn', 
        'plotly', 'joblib', 'faker'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"⚠️  Pacotes faltando: {', '.join(missing_packages)}")
        print("📦 Instalando dependências...")
        run_command("pip install -r requirements.txt", "Instalação de dependências")
    else:
        print("✅ Todas as dependências estão instaladas")

def setup_data():
    """Configura os dados se necessário"""
    data_files = ['applicants.json', 'vagas.json', 'prospects.json']
    data_dir = Path('data')
    
    # Verificar se dados existem e não estão vazios
    need_data = False
    
    for file in data_files:
        file_path = data_dir / file
        if not file_path.exists():
            need_data = True
            break
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                if not data:  # Se arquivo estiver vazio
                    need_data = True
                    break
        except:
            need_data = True
            break
    
    if need_data:
        print("📊 Gerando dados sintéticos...")
        run_command("python generate_data.py", "Geração de dados")
    else:
        print("✅ Dados já existem")

def setup_models():
    """Configura os modelos de ML"""
    models_dir = Path('models')
    
    if not models_dir.exists() or not list(models_dir.glob('*.pkl')):
        print("🤖 Treinando modelos de Machine Learning...")
        run_command("python matching_engine.py", "Treinamento de modelos")
    else:
        print("✅ Modelos já treinados")

def test_ai_interviewer():
    """Testa o sistema de entrevista IA"""
    print("🎯 Testando sistema de entrevista IA...")
    run_command("python3 ai_interviewer.py", "Teste do entrevistador IA")

def create_startup_script():
    """Cria script de inicialização"""
    startup_script = """#!/bin/bash
# Script de inicialização do Decision AI Recruiter

echo "🎯 Iniciando Decision AI Recruiter..."

# Verificar se o Python está instalado
if ! command -v python &> /dev/null; then
    echo "❌ Python não encontrado. Instale o Python 3.8+ primeiro."
    exit 1
fi

# Instalar dependências se necessário
pip install -r requirements.txt

# Gerar dados se necessário
if [ ! -f "data/applicants.json" ] || [ ! -s "data/applicants.json" ]; then
    echo "📊 Gerando dados..."
    python generate_data.py
fi

# Treinar modelos se necessário
if [ ! -d "models" ] || [ -z "$(ls -A models)" ]; then
    echo "🤖 Treinando modelos..."
    python matching_engine.py
fi

# Iniciar aplicação
echo "🚀 Iniciando aplicação Streamlit..."
streamlit run app.py
"""
    
    with open('start.sh', 'w') as f:
        f.write(startup_script)
    
    # Tornar executável
    os.chmod('start.sh', 0o755)
    print("✅ Script de inicialização criado: start.sh")

def main():
    """Função principal de deploy"""
    print("🎯 Decision AI Recruiter - Deploy e Configuração")
    print("=" * 60)
    
    # Verificar se estamos no diretório correto
    if not Path('app.py').exists():
        print("❌ Execute este script no diretório do projeto")
        sys.exit(1)
    
    # Executar etapas de configuração
    check_requirements()
    setup_data()
    setup_models()
    test_ai_interviewer()
    create_startup_script()
    
    print("\n🎉 Deploy concluído com sucesso!")
    print("=" * 60)
    print("📋 Próximos passos:")
    print("   1. Execute: streamlit run app.py")
    print("   2. Ou use: ./start.sh")
    print("   3. Acesse: http://localhost:8501")
    print("\n💡 Para deploy em produção:")
    print("   1. Configure variáveis de ambiente")
    print("   2. Use um servidor WSGI como Gunicorn")
    print("   3. Configure proxy reverso (Nginx)")
    print("   4. Configure SSL/HTTPS")
    
    # Mostrar informações do sistema
    print(f"\n📊 Informações do Sistema:")
    print(f"   - Python: {sys.version.split()[0]}")
    print(f"   - Diretório: {os.getcwd()}")
    print(f"   - Arquivos de dados: {len(list(Path('data').glob('*.json')))} encontrados")
    print(f"   - Modelos ML: {len(list(Path('models').glob('*.pkl'))) if Path('models').exists() else 0} encontrados")

if __name__ == "__main__":
    main()
