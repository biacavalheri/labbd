import streamlit as st
import pandas as pd
from datetime import datetime
st.set_page_config(page_title="Vagas Abertas", page_icon="🔍", layout="wide")

# CSS consistente para todas as páginas
st.markdown("""
<style>
    :root {
        --primary-blue: #1e3a8a;
        --secondary-blue: #3b82f6;
        --dark-blue: #1e40af;
    }
    
    h1 {
        color: var(--primary-blue) !important;
        font-weight: 700 !important;
        border-bottom: 3px solid var(--secondary-blue);
        padding-bottom: 10px;
    }
    
    h2 {
        color: var(--dark-blue) !important;
        font-weight: 600 !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--dark-blue) 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


st.title("🔍 Vagas Abertas")

# Filtros
with st.sidebar:
    st.header("Filtros")
    
    st.subheader("Localização")
    estados = st.multiselect("Estados", ["SP", "RJ", "MG", "RS", "PR", "SC", "BA", "DF"])
    cidades = st.text_input("Cidade")
    
    st.subheader("Tipo de Contratação")
    clt = st.checkbox("CLT", value=True)
    pj = st.checkbox("PJ", value=True)
    estagio = st.checkbox("Estágio", value=True)
    temporario = st.checkbox("Temporário", value=True)
    
    st.subheader("Salário")
    salario_min = st.slider("Salário Mínimo (R$)", 0, 20000, 0, 500)
    
    st.subheader("Skills")
    skills_filtro = st.text_input("Skills desejadas")

# Área principal
st.subheader(f"📋 {15} Vagas Encontradas")

# Exemplo de dados - substituir pelos dados reais depois
vagas_exemplo = [
    {
        "titulo": "Desenvolvedor Full Stack",
        "empresa": "Tech Solutions",
        "cidade": "São Paulo",
        "estado": "SP",
        "tipo_contratacao": "CLT",
        "salario": "R$ 8.000,00",
        "descricao": "Desenvolvimento de aplicações web modernas usando React e Node.js",
        "skills": "React, Node.js, SQL, AWS",
        "data_publicacao": "2024-01-15"
    },
    {
        "titulo": "Cientista de Dados",
        "empresa": "Data Analytics Co",
        "cidade": "Rio de Janeiro",
        "estado": "RJ",
        "tipo_contratacao": "PJ",
        "salario": "R$ 12.000,00",
        "descricao": "Análise de dados e construção de modelos preditivos",
        "skills": "Python, SQL, Machine Learning, TensorFlow",
        "data_publicacao": "2024-01-10"
    }
]

# Exibir vagas
for i, vaga in enumerate(vagas_exemplo):
    with st.expander(f"**{vaga['titulo']}** - {vaga['empresa']} ({vaga['cidade']}/{vaga['estado']})"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"**Descrição:** {vaga['descricao']}")
            st.write(f"**Skills:** {vaga['skills']}")
            st.write(f"**Publicada em:** {vaga['data_publicacao']}")
        
        with col2:
            st.write(f"**Tipo:** {vaga['tipo_contratacao']}")
            st.write(f"**Salário:** {vaga['salario']}")
            
            if st.button("Candidatar-se", key=f"candidatar_{i}"):
                st.success("Candidatura enviada com sucesso!")

# Mensagem quando não há vagas
if not vagas_exemplo:
    st.info("""
    🎯 **Nenhuma vaga encontrada com os filtros selecionados.**
    
    Tente:
    - Alterar os filtros de busca
    - Verificar o spelling das skills
    - Expandir o range salarial
    """)