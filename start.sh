#!/bin/bash
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
