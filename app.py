import streamlit as st
import importlib

st.set_page_config(
    page_title="Sistema de Recrutamento",
    page_icon="💼",
    layout="wide"
)

# Usuários do sistema
USERS = {
    "admin_vagas": {"senha": "123", "permissao": "vagas"},
    "admin_curriculos": {"senha": "123", "permissao": "curriculos"},
}

# Páginas principais por permissão
PAGES = {
    "vagas": {
        "Cadastrar Nova Vaga": "cadastro_vagas",
        "Visualizar Currículos": "curriculos_ativos",
        "Gerenciar Candidatos": "gerenciar_candidatos",
        "Gerenciar Match Score": "match_score_admin",
    },
    "curriculos": {
        "Cadastrar Novo Currículo": "cadastro_curriculos",
        "Visualizar Vagas": "vagas_abertas",
        "Minhas Candidaturas": "minhas_candidaturas",
    }
}

def load_page(page_name):
    module = importlib.import_module(f"private_pages.{page_name}")
    module.main()

def main():
    st.title("💼 Sistema de Recrutamento")

    # ----------------------------------------------------
    # LOGIN
    # ----------------------------------------------------
    if "usuario" not in st.session_state:
        with st.form("login_form"):
            usuario = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")
            login_btn = st.form_submit_button("Entrar")

            if login_btn:
                if usuario in USERS and USERS[usuario]["senha"] == senha:
                    st.session_state["usuario"] = usuario
                    st.session_state["permissao"] = USERS[usuario]["permissao"]
                    st.rerun()
                else:
                    st.error("Credenciais inválidas.")
        return
    
    # ----------------------------------------------------
    # HOME LOGADO
    # ----------------------------------------------------
    perm = st.session_state["permissao"]

    st.sidebar.success(f"Logado como: **{st.session_state['usuario']}**")
    st.sidebar.divider()

    # Botões do menu
    for label, page in PAGES[perm].items():
        if st.sidebar.button(label):
            st.session_state["page"] = page

    if st.sidebar.button("Sair"):
        st.session_state.clear()
        st.rerun()

    # Carrega página escolhida
    if "page" in st.session_state:
        load_page(st.session_state["page"])

if __name__ == "__main__":
    main()
