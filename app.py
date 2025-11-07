import streamlit as st

st.set_page_config(
    page_title="Sistema de Recrutamento",
    page_icon="💼",
    layout="wide"
)

# CSS personalizado com tema azul escuro
st.markdown("""
<style>
    /* Cores do tema azul escuro */
    :root {
        --primary-blue: #1e3a8a;
        --secondary-blue: #3b82f6;
        --dark-blue: #1e40af;
        --light-blue: #dbeafe;
        --accent-blue: #60a5fa;
    }
    
    /* Título principal */
    h1 {
        color: var(--primary-blue) !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 2rem !important;
        font-size: 2.5rem !important;
        border-bottom: 3px solid var(--secondary-blue);
        padding-bottom: 15px;
    }
    
    /* Subtítulo */
    h2 {
        color: var(--dark-blue) !important;
        font-weight: 600 !important;
        text-align: center;
        margin-bottom: 2rem !important;
        font-size: 1.8rem !important;
    }
    
    /* Botões personalizados */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--dark-blue) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--dark-blue) 0%, #1e3a8a 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(30, 58, 138, 0.4) !important;
    }
    
    /* Inputs personalizados */
    .stTextInput > div > div > input {
        border: 2px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 12px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--secondary-blue) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* Labels dos inputs */
    label {
        color: var(--primary-blue) !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    /* Mensagens de sucesso */
    .stSuccess {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%) !important;
        border: 1px solid #22c55e !important;
        border-radius: 10px !important;
        color: #166534 !important;
    }
    
    /* Mensagens de erro */
    .stError {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%) !important;
        border: 1px solid #ef4444 !important;
        border-radius: 10px !important;
        color: #991b1b !important;
    }
    
    /* Container do formulário */
    .main .block-container {
        padding-top: 3rem !important;
    }
    
    /* Melhorar o espaçamento geral */
    .stForm {
        border: 2px solid var(--light-blue) !important;
        border-radius: 15px !important;
        padding: 2rem !important;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
        box-shadow: 0 10px 30px rgba(30, 58, 138, 0.1) !important;
        max-width: 500px !important;
        margin: 0 auto !important;
    }
    
    /* Colunas dentro do form */
    .stForm .row-widget.stColumns {
        margin-top: 1.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("💼 Sistema de Recrutamento")
        
    # Formulário SIMPLES sem colunas complexas
    with st.form("login_form"):
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        
        # Botões lado a lado - maneira mais simples
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
