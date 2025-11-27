import streamlit as st
from private_pages.db import get_connection

def main():
    st.title("💼 Cadastro de Vaga")
    st.write("Preencha os dados abaixo para cadastrar uma nova vaga.")

    # =======================================================
    # Formulário
    # =======================================================
    with st.form("form_vaga"):
        titulo = st.text_input("Título da vaga")
        descricao = st.text_area("Descrição")
        empresa = st.text_input("Empresa")
        tipo_contratacao = st.text_input("Tipo de contratação (CLT, PJ etc.)")
        estado = st.text_input("Estado (UF)")
        cidade = st.text_input("Cidade")
        salario = st.number_input("Salário (R$)", min_value=0.0, step=100.0)
        skills_texto = st.text_input("Skills desejadas (separadas por vírgula)")

        submitted = st.form_submit_button("Cadastrar Vaga")

    if not submitted:
        return

    if not titulo or not empresa:
        st.error("Título e empresa são obrigatórios.")
        return

    conn = get_connection()
    cur = conn.cursor()

    # =======================================================
    # Ajustar SEQUENCE da tabela vaga
    # =======================================================
    cur.execute("SELECT setval('vaga_id_seq', (SELECT COALESCE(MAX(id),0) FROM vaga));")

    # =======================================================
    # Inserir vaga
    # =======================================================
    cur.execute("""
        INSERT INTO vaga
        (titulo, descricao, empresa, tipo_contratacao, estado, cidade, salario)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        RETURNING id;
    """, (titulo, descricao, empresa, tipo_contratacao, estado, cidade, salario))

    id_vaga = cur.fetchone()[0]

    # =======================================================
    # TRATAR SKILLS
    # =======================================================
    skills_lista = [s.strip() for s in skills_texto.split(",") if s.strip()]

    # Atualizar a sequence da tabela skill
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
            # 2. Se já existia, buscar ID
            cur.execute("SELECT id FROM skill WHERE nome = %s;", (sk,))
            id_skill = cur.fetchone()[0]

        # Vincular skill
        cur.execute("""
            INSERT INTO vaga_skill (id_vaga, id_skill)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
        """, (id_vaga, id_skill))

    conn.commit()
    conn.close()

    st.success("Vaga cadastrada com sucesso!")
    st.info(f"ID da vaga: {id_vaga}")
