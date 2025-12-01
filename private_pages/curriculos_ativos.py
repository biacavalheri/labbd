import streamlit as st
from private_pages.db import get_connection

# ======================================================================
# Função: chama o match_final() direto do PostgreSQL
# ======================================================================
def calcular_match(curriculo_id, vaga_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT match_final(%s, %s);", (curriculo_id, vaga_id))
    score = cur.fetchone()[0]

    conn.close()
    return score or 0.0


# ======================================================================
# Página principal
# ======================================================================
def main():
    st.title("👥 Currículos Ativos")
    st.write("Veja os currículos e seus níveis de aderência à vaga selecionada.")

    # ---------------------------------------------------------
    # 1. Seleção da vaga
    # ---------------------------------------------------------
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, titulo, empresa 
        FROM vaga
        ORDER BY empresa, titulo;
    """)
    vagas = cur.fetchall()
    conn.close()

    if not vagas:
        st.error("Nenhuma vaga cadastrada.")
        return

    vagas_dict = {f"{v[1]} ({v[2]}) — ID {v[0]}": v[0] for v in vagas}
    vaga_str = st.selectbox("Selecione uma vaga:", list(vagas_dict.keys()))
    vaga_id = vagas_dict[vaga_str]

    st.divider()

    # ---------------------------------------------------------
    # 2. Carregar currículos
    # ---------------------------------------------------------
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            c.id,
            c.nome,
            c.formacao,
            c.experiencia,
            c.resumo,
            c.idiomas,
            COALESCE(string_agg(s.nome, ', '), '') AS skills
        FROM curriculo c
        LEFT JOIN curriculo_skill cs ON cs.id_curriculo = c.id
        LEFT JOIN skill s ON s.id = cs.id_skill
        GROUP BY c.id
        ORDER BY c.nome;
    """)
    curriculos = cur.fetchall()
    conn.close()

    if not curriculos:
        st.warning("Nenhum currículo cadastrado.")
        return

    # ---------------------------------------------------------
    # 3. Calcular match de todos os currículos
    # ---------------------------------------------------------
    lista = []
    for c in curriculos:
        cid, nome, formacao, exp, resumo, idiomas, skills = c
        score = calcular_match(cid, vaga_id)
        lista.append((score, c))

    # Ordenar por match
    lista.sort(reverse=True, key=lambda x: x[0])

    # ---------------------------------------------------------
    # 4. Exibir currículos com visual melhorado
    # ---------------------------------------------------------
    st.subheader("📊 Currículos ordenados por aderência")

    for score, c in lista:
        cid, nome, formacao, exp, resumo, idiomas, skills = c

        with st.expander(f"{nome} — {formacao}"):
            
            st.markdown(f"### 🔥 Match: **{score:.2f}%**")
            st.progress(min(score / 100, 1))

            st.markdown("#### 🧩 Skills")
            st.write(skills or "Nenhuma skill cadastrada")

            st.markdown("#### 🎯 Experiência")
            st.write(exp or "Sem experiência informada")

            st.markdown("#### 📝 Resumo profissional")
            st.write(resumo or "Sem resumo")

            st.markdown("#### 🌐 Idiomas")
            st.write(idiomas or "Não informado")

            # Verificar se já existe candidatura
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT 1 FROM candidatura 
                WHERE id_curriculo = %s AND id_vaga = %s
            """, (cid, vaga_id))
            existe = cur.fetchone()
            conn.close()

            if existe:
                st.info("📌 Já existe candidatura ou oferta para esta vaga.")
            else:
                if st.button("Oferecer vaga", key=f"offer_{cid}"):
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO candidatura (id_curriculo, id_vaga, origem)
                        VALUES (%s, %s, 'empresa');
                    """, (cid, vaga_id))
                    conn.commit()
                    conn.close()
                    st.success("Oferta enviada!")
                    st.rerun()

