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
    st.write("Veja currículos filtrados e ordenados pela aderência à vaga selecionada.")

    # ---------------------------------------------------------
    # 1. Seleção da vaga
    # ---------------------------------------------------------
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, titulo, empresa, tipo_contratacao 
        FROM vaga
        ORDER BY empresa, titulo;
    """)
    vagas = cur.fetchall()
    conn.close()

    if not vagas:
        st.error("Nenhuma vaga cadastrada.")
        return

    vagas_dict = {f"{v[1]} ({v[2]}) — ID {v[0]}": v for v in vagas}
    vaga_str = st.selectbox("Selecione uma vaga:", list(vagas_dict.keys()))
    vaga_id, vaga_titulo, vaga_empresa, vaga_tipo = vagas_dict[vaga_str]

    st.divider()

    # ---------------------------------------------------------
    # 2. Carregar currículos + skills
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
    # 3. Filtros de busca
    # ---------------------------------------------------------
    st.subheader("🔎 Filtros de busca")

    col1, col2, col3 = st.columns(3)

    texto_busca = col1.text_input("Busca por texto (nome / formação / resumo):")
    filtro_idioma = col2.text_input("Filtrar por idioma (ex: inglês)")
    filtro_skill = col3.text_input("Filtrar por skill (ex: Python)")

    col4, col5 = st.columns(2)
    filtro_formacao = col4.text_input("Filtrar por formação:")
    filtro_experiencia = col5.text_input("Filtrar por experiência:")

    st.divider()

    # ---------------------------------------------------------
    # 4. Aplicar filtros antes do cálculo
    # ---------------------------------------------------------
    def passa_filtro(c):
        cid, nome, formacao, exp, resumo, idiomas, skills = c

        if texto_busca:
            t = texto_busca.lower()
            if t not in nome.lower() and t not in (formacao or '').lower() and t not in (resumo or '').lower():
                return False

        if filtro_idioma:
            if filtro_idioma.lower() not in (idiomas or '').lower():
                return False

        if filtro_skill:
            if filtro_skill.lower() not in (skills or '').lower():
                return False

        if filtro_formacao:
            if filtro_formacao.lower() not in (formacao or '').lower():
                return False

        if filtro_experiencia:
            if filtro_experiencia.lower() not in (exp or '').lower():
                return False

        return True

    curriculos_filtrados = [c for c in curriculos if passa_filtro(c)]

    if not curriculos_filtrados:
        st.warning("Nenhum currículo encontrado com os filtros aplicados.")
        return

    # ---------------------------------------------------------
    # 5. Calcular match só nos currículos filtrados
    # ---------------------------------------------------------
    lista = []
    for c in curriculos_filtrados:
        cid, *_ = c
        score = calcular_match(cid, vaga_id)
        lista.append((score, c))

    lista.sort(reverse=True, key=lambda x: x[0])

    # ---------------------------------------------------------
    # 6. Exibir resultados
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

            # Verificar candidatura
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
