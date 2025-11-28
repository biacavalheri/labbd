import streamlit as st
from private_pages.db import get_connection
import pandas as pd
import pydeck as pdk

@st.cache_data
def carregar_coordenadas():
    df = pd.read_csv("private_pages/data/cidades_brasil.csv")
    df["chave"] = df["cidade"] + "-" + df["estado"]
    return df.set_index("chave")[["lat", "lon"]].to_dict("index")


def main():
    st.title("🗺️ Distribuição Geográfica das Vagas")
    st.write("Explore o mapa interativo com detalhes das vagas ao clicar nos pontos.")

    # Coordenadas completas do Brasil
    COORDENADAS = carregar_coordenadas()

    # Carregar vagas
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

    pontos_validos = []

    # Criar lista de pontos (somente cidades válidas)
    for _, row in df.iterrows():
        chave = f"{row['Cidade']}-{row['Estado']}"
        if chave in COORDENADAS:
            coord = COORDENADAS[chave]
            pontos_validos.append({
                "lat": float(coord["lat"]),
                "lon": float(coord["lon"]),
                "Título": row["Título"],
                "Empresa": row["Empresa"],
                "Cidade": row["Cidade"],
                "Estado": row["Estado"],
                "Tipo": row["Tipo"],
                "Salário": str(row["Salário"]),
                "Descrição": row["Descrição"],
            })

    # Se nenhuma cidade válida for encontrada, mostrar aviso
    if not pontos_validos:
        st.error("Nenhuma vaga possui coordenadas válidas para plotar no mapa.")
        return

    coords_df = pd.DataFrame(pontos_validos)

    # SEMPRE CENTRALIZA NO BRASIL
    view_state = pdk.ViewState(
        latitude=-14.2350,
        longitude=-51.9253,
        zoom=4,
        pitch=30,
    )

    layer = pdk.Layer(
        "ScatterplotLayer",
        coords_df,
        get_position=["lon", "lat"],
        get_radius=28000,
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
