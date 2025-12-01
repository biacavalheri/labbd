import streamlit as st

def main():
    st.title("🎯 Match Score Automático (FTS Ativado)")

    st.info("""
    O sistema de Match Score agora é calculado **automaticamente** usando
    Full-Text Search do PostgreSQL (TSVECTOR / TSQUERY).

    Portanto, não é mais necessário atribuir scores manualmente.
    O painel antigo foi descontinuado.
    """)

    st.code("""
    SELECT ts_rank_cd(v.documento_tsv, c.documento_tsv) AS score
    FROM curriculo c
    JOIN vaga v ON v.id = {id_vaga}
    WHERE c.id = {id_curriculo};
    """, language="sql")
