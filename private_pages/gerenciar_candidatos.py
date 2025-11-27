import streamlit as st
from private_pages.db import get_connection

def main():
    st.title("📋 Gerenciar Candidatos")

    st.write("Selecione uma vaga para visualizar os candidatos inscritos.")

    # -----------------------------------------
    # Carregar vagas
    # -----------------------------------------
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, titulo, empresa
        FROM vaga
        ORDER BY empresa, titulo;
    """)
    vagas_rows = cur.fetchall()

    if not vagas_rows:
        st.warning("Nenhuma vaga cadastrada ainda.")
        return

    vagas = {f"{v[1]} ({v[2]}) — ID {v[0]}": v[0] for v in vagas_rows}

    vaga_escolhida = st.selectbox("Selecione a vaga:", list(vagas.keys()))
    vaga_id = vagas[vaga_escolhida]

    # -----------------------------------------
    # Buscar candidatos da vaga
    # -----------------------------------------
    cur.execute("""
        SELECT c.id, c.nome, c.formacao, c.experiencia,
               ca.origem, ca.data
        FROM candidatura ca
        JOIN curriculo c ON c.id = ca.id_curriculo
        WHERE ca.id_vaga = %s
        ORDER BY ca.data DESC;
    """, (vaga_id,))

    candidatos = cur.fetchall()
    conn.close()

    # -----------------------------------------
    # Exibir resultados
    # -----------------------------------------
    st.subheader("👥 Candidatos inscritos")

    if not candidatos:
        st.info("Nenhum candidato inscrito ainda.")
        return

    for cand in candidatos:
        cid, nome, formacao, exp, origem, data = cand

        with st.expander(f"{nome} — {formacao}"):
            st.write(f"**Experiência:** {exp}")
            st.write(f"**Origem da candidatura:** {'🟦 Candidato' if origem=='candidato' else '🟥 Empresa'}")
            st.write(f"**Data:** {data}")
            st.write(f"**ID do currículo:** {cid}")
