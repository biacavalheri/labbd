import streamlit as st
from private_pages.db import get_connection

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


def main():
    st.title("🔍 Vagas Abertas")

    # Selecionar currículo
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome FROM curriculo ORDER BY nome;")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        st.error("Nenhum currículo cadastrado.")
        return

    curriculos_dict = {f"{n} — ID {i}": i for i, n in rows}
    nome_escolhido = st.selectbox("Selecione o currículo:", curriculos_dict.keys())
    id_curriculo = curriculos_dict[nome_escolhido]

    st.divider()
    st.subheader("Filtros")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT estado FROM vaga ORDER BY estado;")
    estados = [e[0] for e in cur.fetchall() if e[0]]

    cur.execute("SELECT DISTINCT cidade FROM vaga ORDER BY cidade;")
    cidades = [c[0] for c in cur.fetchall() if c[0]]

    cur.execute("SELECT DISTINCT tipo_contratacao FROM vaga ORDER BY tipo_contratacao;")
    tipos = [t[0] for t in cur.fetchall() if t[0]]

    cur.execute("SELECT nome FROM skill ORDER BY nome;")
    skills = [s[0] for s in cur.fetchall()]

    conn.close()

    palavra = st.text_input("Buscar por texto")
    estado = st.selectbox("Estado", ["Todos"] + estados)
    cidade = st.selectbox("Cidade", ["Todos"] + cidades)
    tipo = st.selectbox("Tipo de contratação", ["Todos"] + tipos)
    skill = st.selectbox("Skill desejada", ["Todas"] + skills)

    salario_min = st.number_input("Salário mínimo", min_value=0.0, value=0.0)
    salario_max = st.number_input("Salário máximo", min_value=0.0, value=0.0)

    # Buscar vagas
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT 
            v.id, v.titulo, v.empresa, v.cidade, v.estado,
            v.tipo_contratacao, v.salario, v.descricao,
            COALESCE(string_agg(s.nome, ', '), '') AS skills
        FROM vaga v
        LEFT JOIN vaga_skill vs ON vs.id_vaga = v.id
        LEFT JOIN skill s ON s.id = vs.id_skill
        WHERE 1=1
    """
    params = []

    if palavra:
        like = f"%{palavra}%"
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
                SELECT 1 FROM vaga_skill x
                JOIN skill y ON y.id = x.id_skill
                WHERE x.id_vaga = v.id AND y.nome = %s
            )
        """
        params.append(skill)

    query += " GROUP BY v.id ORDER BY v.id;"

    cur.execute(query, tuple(params))
    vagas_rows = cur.fetchall()
    conn.close()

    # Ordenar por match score
    ranking = []
    for row in vagas_rows:
        vid, titulo, empresa, cidade, estado, tipo, salario, desc, skills = row
        score = calcular_match(id_curriculo, vid)
        ranking.append((score, row))

    ranking.sort(reverse=True)

    # Exibir
    for score, row in ranking:
        vid, titulo, empresa, cidade, estado, tipo, salario, desc, skills = row

        with st.expander(f"{titulo} — {empresa} (Match Score: {score})"):

            st.write(f"**Local:** {cidade}/{estado}")
            st.write(f"**Tipo:** {tipo}")
            st.write(f"**Salário:** R$ {salario}")
            st.write(f"**Skills:** {skills}")
            st.write(f"**Descrição:** {desc}")

            # Verificar candidatura
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT 1 FROM candidatura
                WHERE id_curriculo = %s AND id_vaga = %s
            """, (id_curriculo, vid))
            ja_candidatado = cur.fetchone() is not None
            conn.close()

            if ja_candidatado:
                st.info("📌 Já está inscrito.")
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
