import streamlit as st
from private_pages.db import get_connection

def main():
    st.title("👥 Currículos Ativos")

    # =============================================================
    # 1) SELEÇÃO DA VAGA
    # =============================================================
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, titulo, empresa 
        FROM vaga 
        ORDER BY empresa, titulo;
    """)
    vagas_rows = cur.fetchall()
    conn.close()

    if not vagas_rows:
        st.error("Nenhuma vaga cadastrada.")
        return

    vagas_dict = {f"{v[1]} ({v[2]}) — ID {v[0]}": v[0] for v in vagas_rows}
    vaga_selecionada = st.selectbox(
        "Selecione a vaga para visualizar currículos:",
        list(vagas_dict.keys())
    )
    id_vaga = vagas_dict[vaga_selecionada]

    st.divider()
    st.subheader("⚙️ Filtros de Busca")

    # =============================================================
    # 2) LISTAS DE FILTROS
    # =============================================================
    conn = get_connection()
    cur = conn.cursor()

    # IDIOMAS
    cur.execute("""
        SELECT DISTINCT unnest(string_to_array(idiomas, ',')) AS idioma
        FROM curriculo
        WHERE idiomas IS NOT NULL AND idiomas <> '';
    """)
    idiomas_rows = cur.fetchall()
    idiomas = sorted({row[0].strip() for row in idiomas_rows if row[0] and row[0].strip()})

    # SKILLS
    cur.execute("SELECT nome FROM skill ORDER BY nome;")
    skills = [row[0] for row in cur.fetchall()]

    conn.close()

    # =============================================================
    # 3) INTERFACE DE FILTROS
    # =============================================================
    palavra_chave = st.text_input(
        "Buscar por palavras (nome, formação, resumo, experiência)"
    )

    col1, col2 = st.columns(2)
    with col1:
        idioma = st.selectbox("Idioma", ["Todos"] + idiomas)
    with col2:
        skill = st.selectbox("Skill", ["Todas"] + skills)

    # =============================================================
    # 4) CONSULTAR CURRÍCULOS
    # =============================================================
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT 
            c.id, 
            c.nome, 
            c.formacao, 
            c.experiencia,
            COALESCE(string_agg(s.nome, ', '), '') AS skills,
            c.idiomas, 
            c.resumo, 
            c.empresas_previas
        FROM curriculo c
        LEFT JOIN curriculo_skill cs ON cs.id_curriculo = c.id
        LEFT JOIN skill s ON s.id = cs.id_skill
        WHERE 1=1
    """

    params = []

    if palavra_chave:
        like = f"%{palavra_chave}%"
        query += """
            AND (
                c.nome ILIKE %s OR
                c.formacao ILIKE %s OR
                c.experiencia ILIKE %s OR
                c.resumo ILIKE %s
            )
        """
        params += [like, like, like, like]

    if idioma != "Todos":
        query += " AND c.idiomas ILIKE %s"
        params.append(f"%{idioma}%")

    if skill != "Todas":
        query += """
            AND EXISTS (
                SELECT 1
                FROM curriculo_skill x
                JOIN skill y ON y.id = x.id_skill
                WHERE x.id_curriculo = c.id AND y.nome = %s
            )
        """
        params.append(skill)

    query += """
        GROUP BY c.id
        ORDER BY c.id;
    """

    cur.execute(query, tuple(params))
    rows = cur.fetchall()
    conn.close()

    # =============================================================
    # 5) EXIBIR RESULTADOS
    # =============================================================
    for r in rows:
        cid, nome, formacao, exp, skills_list, idiomas_list, resumo, empresas = r

        with st.expander(f"{nome} — {formacao}"):

            st.write(f"**Experiência:** {exp}")
            st.write(f"**Resumo:** {resumo}")
            st.write(f"**Skills:** {skills_list}")
            st.write(f"**Idiomas:** {idiomas_list}")

            # =============================================================
            # 🔥 TOP 2 VAGAS MAIS ADERENTES
            # =============================================================
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                SELECT 
                    v.id, 
                    v.titulo, 
                    v.empresa, 
                    ms.match_score
                FROM match_score ms
                JOIN vaga v ON v.id = ms.id_vaga
                WHERE ms.id_curriculo = %s
                ORDER BY ms.match_score DESC
                LIMIT 2;
            """, (cid,))

            top_vagas = cur.fetchall()
            conn.close()

            st.subheader("🔥 Top 2 Vagas Mais Aderentes")

            if not top_vagas:
                st.write("Nenhum match registrado ainda.")
            else:
                for vvg in top_vagas:
                    st.write(f"**{vvg[1]} ({vvg[2]})** — score: **{vvg[3]}**")

            # =============================================================
            # VERIFICAR SE JÁ EXISTE UMA OFERTA
            # =============================================================
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                SELECT 1 FROM candidatura
                WHERE id_curriculo = %s AND id_vaga = %s
                LIMIT 1;
            """, (cid, id_vaga))

            ja_ofertado = cur.fetchone() is not None
            conn.close()

            # Botão
            if ja_ofertado:
                st.info("📌 Já existe oferta ou candidatura para este currículo.")
            else:
                if st.button("Oferecer vaga", key=f"offer_{cid}"):

                    conn = get_connection()
                    cur = conn.cursor()

                    cur.execute("""
                        INSERT INTO candidatura (id_curriculo, id_vaga, origem)
                        VALUES (%s, %s, 'empresa');
                    """, (cid, id_vaga))

                    conn.commit()
                    conn.close()

                    st.success("Vaga oferecida!")
                    st.rerun()
