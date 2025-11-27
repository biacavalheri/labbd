import streamlit as st
from private_pages.db import get_connection

def main():
    st.title("🔍 Vagas Abertas")

    # =============================================================
    # 1) SELEÇÃO DO CURRÍCULO
    # =============================================================
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome FROM curriculo ORDER BY nome;")
    curriculos_rows = cur.fetchall()
    conn.close()

    if not curriculos_rows:
        st.error("Nenhum currículo cadastrado.")
        return

    curriculos_dict = {f"{row[1]} — ID {row[0]}": row[0] for row in curriculos_rows}
    curriculo_selecionado = st.selectbox("Selecione o currículo candidato:", list(curriculos_dict.keys()))
    id_curriculo = curriculos_dict[curriculo_selecionado]

    st.divider()
    st.subheader("⚙️ Filtros de Busca")

    # =============================================================
    # 2) CARREGAR LISTAS PARA FILTROS
    # =============================================================
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT estado FROM vaga ORDER BY estado;")
    estados = [x[0] for x in cur.fetchall() if x[0]]

    cur.execute("SELECT DISTINCT cidade FROM vaga ORDER BY cidade;")
    cidades = [x[0] for x in cur.fetchall() if x[0]]

    cur.execute("SELECT DISTINCT tipo_contratacao FROM vaga ORDER BY tipo_contratacao;")
    tipos = [x[0] for x in cur.fetchall() if x[0]]

    cur.execute("SELECT nome FROM skill ORDER BY nome;")
    skills = [x[0] for x in cur.fetchall()]

    conn.close()

    # =============================================================
    # 3) INTERFACE DOS FILTROS
    # =============================================================
    palavra_chave = st.text_input("Buscar por palavras (título, empresa, descrição)")

    col1, col2 = st.columns(2)
    with col1:
        estado = st.selectbox("Estado", ["Todos"] + estados)
    with col2:
        cidade = st.selectbox("Cidade", ["Todos"] + cidades)

    col3, col4 = st.columns(2)
    with col3:
        salario_min = st.number_input("Salário mínimo", min_value=0.0, value=0.0)
    with col4:
        salario_max = st.number_input("Salário máximo", min_value=0.0, value=0.0)

    tipo = st.selectbox("Tipo de contratação", ["Todos"] + tipos)
    skill = st.selectbox("Skill desejada", ["Todas"] + skills)

    # =============================================================
    # 4) CONSULTAR VAGAS
    # =============================================================
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT v.id, v.titulo, v.empresa, v.cidade, v.estado,
               v.tipo_contratacao, v.salario, v.descricao,
               COALESCE(string_agg(s.nome, ', '), '') AS skills
        FROM vaga v
        LEFT JOIN vaga_skill vs ON vs.id_vaga = v.id
        LEFT JOIN skill s ON s.id = vs.id_skill
        WHERE 1=1
    """
    params = []

    if palavra_chave:
        like = f"%{palavra_chave}%"
        query += " AND (v.titulo ILIKE %s OR v.empresa ILIKE %s OR v.descricao ILIKE %s)"
        params += [like, like, like]

    if estado != "Todos":
        query += " AND v.estado = %s"
        params.append(estado)

    if cidade != "Todos":
        query += " AND v.cidade = %s"
        params.append(cidade)

    if tipo != "Todos":
        query += " AND v.tipo_contratacao = %s"
        params.append(tipo)

    if salario_min > 0:
        query += " AND v.salario >= %s"
        params.append(salario_min)

    if salario_max > 0:
        query += " AND v.salario <= %s"
        params.append(salario_max)

    if skill != "Todas":
        query += """
            AND EXISTS (
                SELECT 1 FROM vaga_skill a
                JOIN skill b ON b.id = a.id_skill
                WHERE a.id_vaga = v.id AND b.nome = %s
            )
        """
        params.append(skill)

    query += " GROUP BY v.id ORDER BY v.id;"

    cur.execute(query, tuple(params))
    vagas_rows = cur.fetchall()
    conn.close()

    # =============================================================
    # 5) EXIBIR VAGAS
    # =============================================================
    for r in vagas_rows:
        vid, titulo, empresa, cidade_v, estado_v, tipo_v, salario, descricao, skills_v = r

        with st.expander(f"{titulo} — {empresa}"):

            st.write(f"**Descrição:** {descricao}")
            st.write(f"**Skills necessárias:** {skills_v}")
            st.write(f"**Local:** {cidade_v}/{estado_v}")
            st.write(f"**Tipo:** {tipo_v}")
            st.write(f"**Salário:** R$ {salario}")

            # TOP MATCHES
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT c.nome, ms.match_score
                FROM match_score ms
                JOIN curriculo c ON c.id = ms.id_curriculo
                WHERE ms.id_vaga = %s
                ORDER BY ms.match_score DESC
                LIMIT 2;
            """, (vid,))
            top = cur.fetchall()
            conn.close()

            st.subheader("🔥 Top 2 currículos mais aderentes:")
            if not top:
                st.write("Ainda não há match_score para esta vaga.")
            else:
                for nome_c, score in top:
                    st.write(f"**{nome_c}** — Score: {score}")

            # Verificar candidatura
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT 1 FROM candidatura
                WHERE id_curriculo = %s AND id_vaga = %s
                LIMIT 1;
            """, (id_curriculo, vid))
            ja_candidatado = cur.fetchone() is not None
            conn.close()

            if ja_candidatado:
                st.info("📌 Você já está inscrito nesta vaga.")
            else:
                if st.button("Candidatar-se", key=f"cand_{vid}"):
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO candidatura (id_curriculo, id_vaga, origem)
                        VALUES (%s, %s, 'candidato');
                    """, (id_curriculo, vid))
                    conn.commit()
                    conn.close()
                    st.success("Candidatura registrada!")
                    st.rerun()
