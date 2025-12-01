import streamlit as st
from private_pages.db import get_connection

# ------------------------
# Função de Match Automático
# ------------------------
def calcular_match(curriculo_id, vaga_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            ts_rank_cd(
                v.documento_tsv,
                plainto_tsquery('portuguese', c.documento_tsv::text)
            )
        FROM curriculo c
        JOIN vaga v ON v.id = %s
        WHERE c.id = %s;
    """, (vaga_id, curriculo_id))

    result = cur.fetchone()
    conn.close()

    if not result or result[0] is None:
        return 0.0
    
    return round(result[0] * 100, 2)


# ------------------------
# Página Principal
# ------------------------
def main():
    st.title("👥 Currículos Ativos")

    # Carregar vagas
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
    vaga_selecionada = st.selectbox("Selecione a vaga:", list(vagas_dict.keys()))
    id_vaga = vagas_dict[vaga_selecionada]

    st.divider()
    st.subheader("⚙️ Filtros de Busca")

    # Carregar filtros
    conn = get_connection()
    cur = conn.cursor()

    # Idiomas
    cur.execute("""
        SELECT DISTINCT unnest(string_to_array(idiomas, ',')) AS idioma
        FROM curriculo
        WHERE idiomas IS NOT NULL AND idiomas <> '';
    """)
    idiomas = sorted({r[0].strip() for r in cur.fetchall() if r[0]})

    # Skills
    cur.execute("SELECT nome FROM skill ORDER BY nome;")
    skills = [r[0] for r in cur.fetchall()]

    conn.close()

    palavra_chave = st.text_input("Buscar por nomes, formação, resumo, experiência")

    col1, col2 = st.columns(2)
    with col1:
        idioma = st.selectbox("Idioma", ["Todos"] + idiomas)
    with col2:
        skill = st.selectbox("Skill", ["Todas"] + skills)

    # Consultar currículos
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
                c.nome ILIKE %s OR c.formacao ILIKE %s OR
                c.experiencia ILIKE %s OR c.resumo ILIKE %s
            )
        """
        params += [like, like, like, like]

    if idioma != "Todos":
        query += " AND c.idiomas ILIKE %s"
        params.append(f"%{idioma}%")

    if skill != "Todas":
        query += """
            AND EXISTS (
                SELECT 1 FROM curriculo_skill a
                JOIN skill b ON b.id = a.id_skill
                WHERE a.id_curriculo = c.id AND b.nome = %s
            )
        """
        params.append(skill)

    query += " GROUP BY c.id ORDER BY c.id;"

    cur.execute(query, tuple(params))
    rows = cur.fetchall()
    conn.close()

    # Exibir
    for r in rows:
        cid, nome, formacao, exp, skills_list, idiomas_list, resumo, empresas = r

        with st.expander(f"{nome} — {formacao}"):

            st.write(f"**Experiência:** {exp}")
            st.write(f"**Resumo:** {resumo}")
            st.write(f"**Skills:** {skills_list}")
            st.write(f"**Idiomas:** {idiomas_list}")

            st.subheader("🔥 Top 2 Vagas mais aderentes (FTS)")

            # Buscar todas vagas para calcular ranking
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, titulo, empresa FROM vaga ORDER BY id;")
            todas_vagas = cur.fetchall()
            conn.close()

            ranking = []
            for v in todas_vagas:
                vid, titulo, empresa = v
                score = calcular_match(cid, vid)
                ranking.append((score, vid, titulo, empresa))

            ranking.sort(reverse=True)
            top2 = ranking[:2]

            for score, vid, titulo_v, empresa_v in top2:
                st.write(f"**{titulo_v} ({empresa_v})** — Match Score: **{score}**")

            # Verificar candidatura
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                SELECT 1 FROM candidatura
                WHERE id_curriculo = %s AND id_vaga = %s
            """, (cid, id_vaga))

            ja_ofertado = cur.fetchone() is not None
            conn.close()

            if ja_ofertado:
                st.info("📌 Já existe oferta ou candidatura.")
            else:
                if st.button("Oferecer vaga", key=f"oferta_{cid}"):
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO candidatura (id_curriculo, id_vaga, origem)
                        VALUES (%s, %s, 'empresa');
                    """, (cid, id_vaga))
                    conn.commit()
                    conn.close()
                    st.success("Oferta enviada!")
                    st.rerun()
