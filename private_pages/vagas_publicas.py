import streamlit as st
from private_pages.db import get_connection
import pandas as pd

def main():
    st.title("🌎 Vagas Abertas (Acesso Público)")
    st.write("Visualize todas as vagas disponíveis, sem necessidade de login.")

    # --------------------------------------------
    # Carregar vagas
    # --------------------------------------------
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, titulo, empresa, cidade, estado,
               tipo_contratacao, salario, descricao
        FROM vaga
        ORDER BY id DESC;
    """)

    rows = cur.fetchall()
    conn.close()

    if not rows:
        st.info("Nenhuma vaga cadastrada ainda.")
        return

    # --------------------------------------------
    # Exibição estruturada das vagas
    # --------------------------------------------
    st.subheader("📄 Lista de vagas")

    for r in rows:
        vid, titulo, empresa, cidade, estado, tipo, salario, descricao = r

        with st.expander(f"{titulo} — {empresa}"):
            st.markdown(f"""
            **📌 Empresa:** {empresa}  
            **📍 Local:** {cidade}/{estado}  
            **🏷️ Tipo de contratação:** {tipo}  
            **💰 Salário:** R$ {salario:.2f}  
            """)
            st.write("**📝 Descrição da vaga:**")
            st.write(descricao)

    st.divider()