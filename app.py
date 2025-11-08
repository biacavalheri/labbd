import streamlit as st

st.set_page_config(
    page_title="Sistema de Recrutamento",
    page_icon="💼",
    layout="wide"
)

# CSS MÍNIMO para fundo branco
st.markdown("""
<style>
    .stApp {
        background-color: white !important;
    }
    body {
        background-color: white !important;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("💼 Sistema de Recrutamento")
    st.subheader("Login")
    
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
