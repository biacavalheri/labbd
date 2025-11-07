import streamlit as st
st.set_page_config(page_title="Cadastro de Vaga", page_icon="💼")

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


st.title("💼 Cadastrar Nova Vaga")

with st.form("cadastro_vaga"):
    st.subheader("Informações da Vaga")
    
    titulo = st.text_input("Título da Vaga*", placeholder="Ex: Desenvolvedor Full Stack")
    
    col1, col2 = st.columns(2)
    
    with col1:
        empresa = st.text_input("Empresa*", placeholder="Nome da empresa")
        cidade = st.text_input("Cidade*", placeholder="Cidade da vaga")
        estado = st.selectbox("Estado*", [
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", 
            "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", 
            "RS", "RO", "RR", "SC", "SP", "SE", "TO"
        ])
    
    with col2:
        tipo_contratacao = st.selectbox("Tipo de Contratação*", [
            "CLT", "PJ", "Estágio", "Temporário", "Freelancer"
        ])
        salario = st.text_input("Salário", placeholder="R$ 0.000,00")
    
    st.subheader("Descrição e Requisitos")
    
    descricao = st.text_area("Descrição da Vaga*", 
                           placeholder="Descreva as responsabilidades e atribuições...",
                           height=100)
    
    skills = st.text_area("Skills Requeridas*",
                        placeholder="Liste as skills necessárias separadas por vírgula\nEx: Python, SQL, React, AWS",
                        height=80)
    
    st.subheader("Informações Adicionais")
    
    col3, col4 = st.columns(2)
    
    with col3:
        beneficios = st.text_area("Benefícios", 
                               placeholder="Liste os benefícios oferecidos",
                               height=80)
    
    with col4:
        requisitos_adicionais = st.text_area("Requisitos Adicionais",
                                          placeholder="Outros requisitos ou informações",
                                          height=80)
    
    submitted = st.form_submit_button("Publicar Vaga")
    
    if submitted:
        if not all([titulo, empresa, cidade, estado, tipo_contratacao, descricao, skills]):
            st.error("Por favor, preencha todos os campos obrigatórios (*)")
        else:
            st.success("Vaga cadastrada com sucesso!")
            st.balloons()