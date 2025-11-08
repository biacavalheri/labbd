import streamlit as st

st.set_page_config(
    page_title="Sistema de Recrutamento",
    page_icon="💼",
    layout="wide"
)

# CSS para FORÇAR tema claro e fundo branco
st.markdown("""
<style>
    /* Forçar tema claro */
    .main {
        background-color: #ffffff !important;
    }
    
    .stApp {
        background-color: #ffffff !important;
    }
    
    /* Título principal */
    h1 {
        color: #1e3a8a !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 2rem !important;
        font-size: 2.5rem !important;
    }
    
    /* Subtítulo */
    h2 {
        color: #1e40af !important;
        font-weight: 600 !important;
        text-align: center;
        margin-bottom: 2rem !important;
    }
    
    /* Botões */
    .stButton > button {
        background-color: #1e3a8a !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    
    .stButton > button:hover {
        background-color: #1e40af !important;
    }
    
    /* Inputs com fundo branco */
    .stTextInput > div > div > input {
        background-color: white !important;
        color: black !important;
        border: 1px solid #ccc !important;
    }
    
    /* Garantir que todo o fundo seja branco */
    body {
        background-color: #ffffff !important;
    }
    
    /* Remover qualquer fundo escuro */
    section.main {
        background-color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("💼 Sistema de Recrutamento")
    
    st.subheader("Login")
    
    # Formulário
    with st.form("login_form"):
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        
        col1, col2 = st.columns(2)
        
        with col1:
            login_btn = st.form_submit_button("Entrar")
        with col2:
            cadastro_btn = st.form_submit_button("Cadastrar")
        
        if login_btn:
            if usuario and senha:
                st.success(f"Bem-vindo (a), {usuario}!")
            else:
                st.error("Preencha usuário e senha!")
        
        if cadastro_btn:
            st.switch_page("pages/1_Cadastro_Usuario.py")

if __name__ == "__main__":
    main()
