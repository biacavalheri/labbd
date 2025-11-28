import streamlit as st
import importlib

st.set_page_config(
    page_title="Sistema de Recrutamento",
    page_icon="💼",
    layout="wide"
)

# Usuários do sistema
USERS = {
    "empregador": {"senha": "123", "permissao": "vagas"},
    "candidato": {"senha": "123", "permissao": "curriculos"},
    "admin": {"senha": "123", "permissao": "admin"},
}

# Páginas principais por permissão
PAGES = {
    "vagas": {
        "Cadastrar Nova Vaga": "cadastro_vagas",
        "Visualizar Currículos": "curriculos_ativos",
        "Gerenciar Candidatos": "gerenciar_candidatos",
    },
    "curriculos": {
        "Cadastrar Novo Currículo": "cadastro_curriculos",
        "Visualizar Vagas": "vagas_abertas",
        "Minhas Candidaturas": "minhas_candidaturas",
    },
    "admin": {
        "Cadastrar Nova Vaga": "cadastro_vagas",
        "Cadastrar Novo Currículo": "cadastro_curriculos",
        "Visualizar Vagas": "vagas_abertas",
        "Visualizar Currículos": "curriculos_ativos",
        "Gerenciar Match Score": "match_score_admin",
    }
}

# ---------------------------------------------------------------
# Páginas públicas (sem login)
# ---------------------------------------------------------------
PAGES_PUBLIC = {
    "vagas_publicas": "vagas_publicas",
    "vagas_mapa_publico": "vagas_mapa_publico"
}

def load_page(page_name):
    module = importlib.import_module(f"private_pages.{page_name}")
    module.main()

def main():
    st.title("💼 Sistema de Recrutamento")

    # ----------------------------------------------------
    # LOGIN OU ACESSO PÚBLICO
    # ----------------------------------------------------
    if "usuario" not in st.session_state:

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔍 Ver vagas abertas"):
                st.session_state["page"] = "vagas_publicas"
                st.rerun()

        with col2:
            if st.button("🗺️ Ver distribuição geográfica das vagas"):
                st.session_state["page"] = "vagas_mapa_publico"
                st.rerun()

        # ------------------------------------------
        # FORMULÁRIO DE LOGIN
        # ------------------------------------------
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

        # Caso tenha página pública selecionada
        if "page" in st.session_state:
            if st.session_state["page"] in PAGES_PUBLIC:
                load_page(st.session_state["page"])
                return

        return  # evita carregar o restante da interface logada

    # ----------------------------------------------------
    # HOME LOGADO
    # ----------------------------------------------------
    perm = st.session_state["permissao"]

    st.sidebar.success(f"Logado como: **{st.session_state['usuario']}**")
    st.sidebar.divider()

    # Botões do menu lateral
    for label, page in PAGES[perm].items():
        if st.sidebar.button(label):
            st.session_state["page"] = page

    if st.sidebar.button("Sair"):
        st.session_state.clear()
        st.rerun()

    # Carrega página escolhida
    if "page" in st.session_state:
        load_page(st.session_state["page"])
        return


if __name__ == "__main__":
    main()
