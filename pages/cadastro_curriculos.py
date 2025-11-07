import streamlit as st

st.set_page_config(page_title="Cadastro de Currículo", page_icon="📄")

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

st.title("📄 Cadastro de Currículo")

with st.form("cadastro_curriculo"):
    st.subheader("Informações Pessoais")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nome = st.text_input("Nome Completo*", placeholder="Seu nome completo")
        email = st.text_input("E-mail*", placeholder="seu.email@exemplo.com")
        telefone = st.text_input("Telefone*", placeholder="+55 11 99999-9999")
    
    with col2:
        formacao = st.text_input("Formação Acadêmica*", placeholder="Ex: Bacharelado em Ciência da Computação")
        experiencia = st.text_input("Experiência Profissional*", placeholder="Ex: 3 anos como desenvolvedor")
    
    st.subheader("Competências")
    
    skills = st.text_area("Skills*",
                        placeholder="Liste suas habilidades técnicas separadas por vírgula\nEx: Python, React, SQL, Docker, AWS",
                        height=80)
    
    idiomas = st.text_input("Idiomas", placeholder="Ex: Português, Inglês, Espanhol")
    
    certificacoes = st.text_area("Certificações",
                               placeholder="Liste suas certificações",
                               height=60)
    
    st.subheader("Experiência Profissional")
    
    empresas_previas = st.text_area("Empresas Anteriores",
                                  placeholder="Liste empresas onde trabalhou anteriormente",
                                  height=60)
    
    resumo = st.text_area("Resumo Profissional*",
                        placeholder="Faça um resumo da sua carreira e objetivos...",
                        height=100)
    
    st.subheader("Preferências")
    
    col3, col4 = st.columns(2)
    
    with col3:
        tipo_contratacao_pref = st.multiselect("Tipos de Contratação de Interesse", [
            "CLT", "PJ", "Estágio", "Temporário", "Freelancer"
        ])
    
    with col4:
        pretensao_salarial = st.text_input("Pretensão Salarial", placeholder="R$ 0.000,00")
        localidade_pref = st.text_input("Localidade Preferida", placeholder="Cidade/Estado")
    
    submitted = st.form_submit_button("Salvar Currículo")
    
    if submitted:
        if not all([nome, email, telefone, formacao, experiencia, skills, resumo]):
            st.error("Por favor, preencha todos os campos obrigatórios (*)")
        else:
            st.success("Currículo cadastrado com sucesso!")
            st.balloons()