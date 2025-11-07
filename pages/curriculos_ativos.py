import streamlit as st
st.set_page_config(page_title="Currículos Ativos", page_icon="👥", layout="wide")

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


st.title("👥 Currículos Ativos")

# Filtros para recrutadores
with st.sidebar:
    st.header("Filtros de Busca")
    
    st.subheader("Competências")
    skills_busca = st.text_input("Skills desejadas", placeholder="Python, React, SQL...")
    
    st.subheader("Experiência")
    exp_minima = st.slider("Experiência Mínima (anos)", 0, 20, 0)
    
    st.subheader("Formação")
    formacao_filtro = st.selectbox("Formação", [
        "Todas", "Ciência da Computação", "Engenharia", "Sistemas de Informação", 
        "Análise e Desenvolvimento", "Outras"
    ])
    
    st.subheader("Idiomas")
    idiomas_filtro = st.text_input("Idiomas", placeholder="Inglês, Espanhol...")

# Área principal
st.subheader(f"📊 {8} Currículos Encontrados")

# Exemplo de dados - substituir pelos dados reais depois
curriculos_exemplo = [
    {
        "nome": "João Silva",
        "formacao": "Bacharelado em Ciência da Computação",
        "experiencia": "3 anos como Desenvolvedor Full Stack",
        "skills": "Python, Django, React, PostgreSQL, Docker",
        "idiomas": "Português, Inglês",
        "resumo": "Desenvolvedor com experiência em aplicações web escaláveis..."
    },
    {
        "nome": "Maria Santos",
        "formacao": "Engenharia de Software",
        "experiencia": "5 anos como Cientista de Dados",
        "skills": "Python, SQL, Machine Learning, TensorFlow, AWS",
        "idiomas": "Português, Inglês, Espanhol",
        "resumo": "Cientista de dados com expertise em modelos preditivos..."
    }
]

# Exibir currículos
for i, currículo in enumerate(curriculos_exemplo):
    with st.expander(f"**{currículo['nome']}** - {currículo['formacao']}"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"**Experiência:** {currículo['experiencia']}")
            st.write(f"**Skills:** {currículo['skills']}")
            st.write(f"**Idiomas:** {currículo['idiomas']}")
            st.write(f"**Resumo:** {currículo['resumo']}")
        
        with col2:
            if st.button("👀 Ver Perfil Completo", key=f"perfil_{i}"):
                st.session_state.perfil_selecionado = currículo['nome']
            
            if st.button("💼 Oferecer Vaga", key=f"oferta_{i}"):
                st.success(f"Vaga oferecida para {currículo['nome']}!")

# Mensagem quando não há currículos
if not curriculos_exemplo:
    st.info("""
    🔍 **Nenhum currículo encontrado com os filtros selecionados.**
    
    Sugestões:
    - Ampliar os filtros de skills
    - Ajustar a experiência mínima
    - Verificar o spelling das competências
    """)