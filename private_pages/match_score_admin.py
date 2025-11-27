import streamlit as st
from private_pages.db import get_connection

def main():
    st.title("🎯 Gerenciar Match Score")

    st.write("Selecione uma vaga e um currículo para atribuir um score de aderência.")

    conn = get_connection()
    cur = conn.cursor()

    # Carregar vagas
    cur.execute("SELECT id, titulo, empresa FROM vaga ORDER BY empresa, titulo;")
    vagas_rows = cur.fetchall()
    vagas = {f"{v[1]} ({v[2]}) - ID {v[0]}": v[0] for v in vagas_rows}

    # Carregar currículos
    cur.execute("SELECT id, nome FROM curriculo ORDER BY nome;")
    curr_rows = cur.fetchall()
    curriculos = {f"{c[1]} - ID {c[0]}": c[0] for c in curr_rows}

    conn.close()

    vaga_selecionada = st.selectbox("Vaga:", list(vagas.keys()))
    curriculo_selecionado = st.selectbox("Currículo:", list(curriculos.keys()))

    match = st.slider("Match Score (0 a 100)", min_value=0, max_value=100, value=50)

    if st.button("Salvar Match Score"):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO match_score (id_curriculo, id_vaga, match_score)
            VALUES (%s, %s, %s)
            ON CONFLICT (id_curriculo, id_vaga)
            DO UPDATE SET match_score = EXCLUDED.match_score;
        """, (curriculos[curriculo_selecionado], vagas[vaga_selecionada], match))

        conn.commit()
        conn.close()

        st.success("Match score salvo com sucesso!")
