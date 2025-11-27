import streamlit as st
from private_pages.db import get_connection

def main():
    st.title("💼 Minhas Candidaturas")

    st.write("Selecione um currículo para visualizar as vagas inscritas.")

    # -----------------------------------------
    # Carregar currículos
    # -----------------------------------------
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, nome
        FROM curriculo
        ORDER BY nome;
    """)
    curriculos_rows = cur.fetchall()

    if not curriculos_rows:
        st.warning("Nenhum currículo cadastrado ainda.")
        return

    curriculos = {f"{c[1]} — ID {c[0]}": c[0] for c in curriculos_rows}

    curriculo_escolhido = st.selectbox("Selecione o currículo:", list(curriculos.keys()))
    curriculo_id = curriculos[curriculo_escolhido]

    # -----------------------------------------
    # Buscar candidaturas do currículo
    # -----------------------------------------
    cur.execute("""
        SELECT v.id, v.titulo, v.empresa, v.tipo_contratacao,
               ca.origem, ca.data
        FROM candidatura ca
        JOIN vaga v ON v.id = ca.id_vaga
        WHERE ca.id_curriculo = %s
        ORDER BY ca.data DESC;
    """, (curriculo_id,))

    vagas = cur.fetchall()
    conn.close()

    # -----------------------------------------
    # Exibir resultados
    # -----------------------------------------
    st.subheader("📌 Vagas inscritas")

    if not vagas:
        st.info("Você ainda não se candidatou a nenhuma vaga.")
        return

    for vaga in vagas:
        vid, titulo, empresa, tipo, origem, data = vaga

        with st.expander(f"{titulo} — {empresa}"):
            st.write(f"**Tipo:** {tipo}")
            st.write(f"**Origem da candidatura:** {'🟦 Candidato' if origem=='candidato' else '🟥 Empresa'}")
            st.write(f"**Data:** {data}")
            st.write(f"**ID da vaga:** {vid}")
