import streamlit as st
from private_pages.db import get_connection

def main():
    st.title("📝 Cadastro de Currículo")
    st.write("Preencha os dados abaixo para cadastrar um novo currículo.")

    # =======================================================
    # Formulário
    # =======================================================
    with st.form("form_curriculo"):
        nome = st.text_input("Nome completo")
        email = st.text_input("E-mail")
        telefone = st.text_input("Telefone")
        formacao = st.text_area("Formação")
        experiencia = st.text_area("Experiência")
        resumo = st.text_area("Resumo profissional")
        empresas_previas = st.text_area("Empresas anteriores")
        idiomas = st.text_input("Idiomas (separados por vírgula)")
        certificacoes = st.text_area("Certificações")
        skills_texto = st.text_input("Skills (separadas por vírgula)")

        submitted = st.form_submit_button("Cadastrar Currículo")

    if not submitted:
        return

    if not nome or not email:
        st.error("Nome e email são obrigatórios.")
        return

    conn = get_connection()
    cur = conn.cursor()

    # =======================================================
    # Ajustar SEQUENCE da tabela curriculo
    # =======================================================
    cur.execute("SELECT setval('curriculo_id_seq', (SELECT COALESCE(MAX(id),0) FROM curriculo));")

    # =======================================================
    # Inserir currículo
    # =======================================================
    cur.execute("""
        INSERT INTO curriculo 
        (nome, email, telefone, formacao, experiencia, resumo, empresas_previas, idiomas, certificacoes)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id;
    """, (nome, email, telefone, formacao, experiencia, resumo, empresas_previas, idiomas, certificacoes))

    id_curriculo = cur.fetchone()[0]

    # =======================================================
    # TRATAR SKILLS
    # =======================================================
    skills_lista = [s.strip() for s in skills_texto.split(",") if s.strip()]

    # Atualizar sequence da tabela skill
    cur.execute("SELECT setval('skill_id_seq', (SELECT COALESCE(MAX(id),0) FROM skill));")

    for sk in skills_lista:
        # 1. Tentar inserir
        cur.execute("""
            INSERT INTO skill (nome)
            VALUES (%s)
            ON CONFLICT (nome) DO NOTHING
            RETURNING id;
        """, (sk,))

        result = cur.fetchone()

        if result:
            id_skill = result[0]  # Inseriu agora
        else:
            # 2. Já existia → buscar ID existente
            cur.execute("SELECT id FROM skill WHERE nome = %s;", (sk,))
            id_skill = cur.fetchone()[0]

        # Vincular skill ao currículo
        cur.execute("""
            INSERT INTO curriculo_skill (id_curriculo, id_skill)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
        """, (id_curriculo, id_skill))

    conn.commit()
    conn.close()

    st.success("Currículo cadastrado com sucesso!")
    st.info(f"ID gerado: {id_curriculo}")
