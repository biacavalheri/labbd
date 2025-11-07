import streamlit as st
st.set_page_config(page_title="Cadastro de Usuário", page_icon="📝")

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


st.title("📝 Cadastro de Usuário")

with st.form("cadastro_usuario"):
    st.subheader("Dados Pessoais")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nome = st.text_input("Nome Completo*", placeholder="Digite seu nome completo")
        email = st.text_input("E-mail*", placeholder="seu.email@exemplo.com")
        telefone = st.text_input("Telefone", placeholder="(11) 99999-9999")
    
    with col2:
        data_nascimento = st.date_input("Data de Nascimento")
        tipo_usuario = st.selectbox("Tipo de Usuário*", ["Candidato", "Recrutador"])
    
    st.subheader("Dados de Acesso")
    
    col3, col4 = st.columns(2)
    
    with col3:
        usuario = st.text_input("Nome de Usuário*", placeholder="Escolha um nome de usuário")
    
    with col4:
        senha = st.text_input("Senha*", type="password", placeholder="Crie uma senha forte")
        confirmar_senha = st.text_input("Confirmar Senha*", type="password", placeholder="Repita a senha")
    
    # Termos e condições
    aceitar_termos = st.checkbox("Aceito os termos e condições de uso*")
    
    submitted = st.form_submit_button("Cadastrar Usuário")
    
    if submitted:
        if not all([nome, email, usuario, senha, confirmar_senha, tipo_usuario]):
            st.error("Por favor, preencha todos os campos obrigatórios (*)")
        elif senha != confirmar_senha:
            st.error("As senhas não coincidem!")
        elif not aceitar_termos:
            st.error("Você deve aceitar os termos e condições!")
        else:
            st.success("Usuário cadastrado com sucesso!")
            st.info("Redirecionando para a página de login...")
