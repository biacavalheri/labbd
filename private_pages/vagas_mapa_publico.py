import streamlit as st
from private_pages.db import get_connection
import pandas as pd
import pydeck as pdk

# ==============================
# FUNÇÃO PARA CARREGAR COORDENADAS
# ==============================
@st.cache_data
def carregar_coordenadas():
    df = pd.read_csv("private_pages/data/cidades_brasil.csv")
    df["chave"] = df["cidade"] + "-" + df["estado"]
    return df.set_index("chave")[["lat", "lon"]].to_dict("index")


def main():
    st.title("🗺️ Distribuição Geográfica das Vagas")
    st.write("Explore o mapa interativo com detalhes das vagas ao clicar nos pontos.")

    # Carrega dicionário completo (5.568 cidades)
    COORDENADAS = carregar_coordenadas()

    # Carregar vagas do banco
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, titulo, empresa, cidade, estado, tipo_contratacao, salario, descricao
        FROM vaga
        ORDER BY id DESC;
    """)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        st.warning("Nenhuma vaga cadastrada para exibir no mapa.")
        return

    df = pd.DataFrame(rows, columns=[
        "ID", "Título", "Empresa", "Cidade", "Estado",
        "Tipo", "Salário", "Descrição"
    ])

    pontos = []
    cidades_sem_coord = []

    # Criar lista de pontos
    for _, row in df.iterrows():
        chave = f"{row['Cidade']}-{row['Estado']}"

        if chave in COORDENADAS:
            lat = float(COORDENADAS[chave]["lat"])
            lon = float(COORDENADAS[chave]["lon"])

            pontos.append({
                "lat": lat,
                "lon": lon,
                "Título": row["Título"],
                "Empresa": row["Empresa"],
                "Cidade": row["Cidade"],
                "Estado": row["Estado"],
                "Tipo": row["Tipo"],
                "Salário": str(row["Salário"]),
                "Descrição": row["Descrição"],
            })
        else:
            cidades_sem_coord.append(chave)

    # Aviso discreto sobre cidades não encontradas
    if cidades_sem_coord:
        st.warning(
            "Algumas cidades não têm coordenadas cadastradas: "
            + ", ".join(set(cidades_sem_coord))
        )

    if not pontos:
        st.error("Nenhuma vaga pôde ser plotada no mapa.")
        return

    coords_df = pd.DataFrame(pontos)

    # CONFIGURAÇÃO DO MAPA
    view_state = pdk.ViewState(
        latitude=coords_df["lat"].mean(),
        longitude=coords_df["lon"].mean(),
        zoom=4,
        pitch=30,
    )

    layer = pdk.Layer(
        "ScatterplotLayer",
        coords_df,
        get_position=["lon", "lat"],
        get_radius=25000,
        get_color=[30, 136, 229, 200],
        pickable=True,
        auto_highlight=True,
    )

    tooltip = {
        "html": """
        <b>{Título}</b><br>
        <b>Empresa:</b> {Empresa}<br>
        <b>Cidade:</b> {Cidade}/{Estado}<br>
        <b>Tipo:</b> {Tipo}<br>
        <b>Salário:</b> R$ {Salário}<br>
        """,
        "style": {"backgroundColor": "rgba(30, 30, 30, 0.9)", "color": "white"}
    }

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="mapbox://styles/mapbox/light-v9",
    )

    st.pydeck_chart(deck)
