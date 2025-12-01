import streamlit as st
from private_pages.db import get_connection

# ==========================================================
# Função utilitária: chama match_final() no PostgreSQL
# ==========================================================
def calcular_match(curriculo_id, vaga_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT match_final(%s, %s);", (curriculo_id, vaga_id))
    score = cur.fetchone()[0]
    conn.close()
    return score or 0.0


# ==========================================================
# Página principal
# ==========================================================
def main():
    st.title("🔍 Vagas Abertas")
    st.write("Veja as vagas disponíveis e filtre por skills, faixa salarial, tipo de contratação e muito mais.")

    # ---------------------------------------------------------
    # 1. Selecionar currículo
    # ---------------------------------------------------------
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome FROM curriculo ORDER BY nome;")
    curriculos = cur.fetchall()
    conn.close()

    if not curriculos:
        st.error("Nenhum currículo cadastrado.")
        return

    curriculo_dict = {f"{c[1]} — ID {c[0]}": c[0] for c in curriculos}
    curriculo_str = st.selectbox("Selecione seu currículo:", list(curriculo_dict.keys()))
    curriculo_id = curriculo_dict[curriculo_str]

    st.divider()

    # ---------------------------------------------------------
    # 2. Buscar vagas
    # ---------------------------------------------------------
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            v.id,
            v.titulo,
            v.empresa,
            v.cidade,
            v.estado,
            v.tipo_contratacao,
            v.salario,
            v.descricao,
            COALESCE(string_agg(s.nome, ', '), '') AS skills
        FROM vaga v
        LEFT JOIN vaga_skill vs ON vs.id_vaga = v.id
        LEFT JOIN skill s ON s.id = vs.id_skill
        GROUP BY v.id
        ORDER BY v.id DESC;
    """)
    vagas = cur.fetchall()
    conn.close()

    if not vagas:
        st.warning("Nenhuma vaga disponível.")
        return

    # ---------------------------------------------------------
    # 3. Filtros
    # ---------------------------------------------------------
    st.subheader("🔎 Filtros de busca")

    col1, col2, col3 = st.columns(3)
    texto_busca = col1.text_input("Busca por texto (nome / empresa / cidade):")
    filtro_skill = col2.text_input("Filtrar por skill:")
    filtro_tipo = col3.text_input("Tipo de contratação (ex: CLT)")

    col4, col5 = st.columns(2)
    salario_min, salario_max = col4.slider("Faixa salarial:", 0, 50000, (0, 50000))
    filtro_estado = col5.text_input("Filtrar por estado (UF):")

    st.divider()

    # ---------------------------------------------------------
    # 4. Aplicar filtros
    # ---------------------------------------------------------
    def passa_filtro(v):
        vid, titulo, empresa, cidade, estado, tipo, salario, desc, skills = v

        if texto_busca:
            t = texto_busca.lower()
            if t not in titulo.lower() and t not in empresa.lower() and t not in cidade.lower():
                return False

        if filtro_skill:
            if filtro_skill.lower() not in skills.lower():
                return False

        if filtro_tipo:
            if filtro_tipo.lower() not in tipo.lower():
                return False

        if filtro_estado:
            if filtro_estado.lower() not in estado.lower():
                return False

        if not (salario_min <= salario <= salario_max):
            return False

        return True

    vagas_filtradas = [v for v in vagas if passa_filtro(v)]

    if not vagas_filtradas:
        st.warning("Nenhuma vaga encontrada com os filtros aplicados.")
        return

    # ---------------------------------------------------------
    # 5. Calcular match apenas nas filtradas
    # ---------------------------------------------------------
    ranking = []
    for v in vagas_filtradas:
        vid = v[0]
        score = calcular_match(curriculo_id, vid)
        ranking.append((score, v))

    ranking.sort(reverse=True, key=lambda x: x[0])

    # ---------------------------------------------------------
    # 6. Exibir
    # ---------------------------------------------------------
    st.subheader("📊 Vagas ordenadas por aderência")

    for score, v in ranking:
        vid, titulo, empresa, cidade, estado, tipo, salario, desc, skills = v

        with st.expander(f"{titulo} — {empresa}"):

            st.markdown(f"### 🔥 Match: **{score:.2f}%**")
            st.progress(min(score / 100, 1))

            st.markdown(f"""
            **📍 Local:** {cidade}/{estado}  
            **🏷 Tipo:** {tipo}  
            **💰 Salário:** R$ {salario:.2f}  
            """)

            st.markdown("#### 🧩 Skills desejadas")
            st.write(skills or "Nenhuma skill cadastrada")

            st.markdown("#### 📝 Descrição da vaga")
            st.write(desc or "Sem descrição")

            # Verificar candidatura
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT 1 FROM candidatura
                WHERE id_curriculo = %s AND id_vaga = %s;
            """, (curriculo_id, vid))
            existe = cur.fetchone()
            conn.close()

            if existe:
                st.info("📌 Você já se candidatou a esta vaga.")
            else:
                if st.button("Candidatar-se", key=f"candid_{vid}"):
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO candidatura (id_curriculo, id_vaga, origem)
                        VALUES (%s, %s, 'candidato');
                    """, (curriculo_id, vid))
                    conn.commit()
                    conn.close()
                    st.success("Candidatura registrada!")
                    st.rerun()
