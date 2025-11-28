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
    st.write("Explore o mapa interativo e veja todas as vagas por cidade.")

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

    # AGRUPAR vagas por cidade
    agrupado = df.groupby(["Cidade", "Estado"])

    pontos = []

    for (cidade, estado), grupo in agrupado:
        chave = f"{cidade}-{estado}"

        if chave not in COORDENADAS:
            continue

        coord = COORDENADAS[chave]

        # Montar tooltip com todas as vagas daquela cidade
        vagas_html = "<br>".join(
            [f"• {row['Título']} — {row['Empresa']}" for _, row in grupo.iterrows()]
        )

        tooltip_html = f"""
        <b>{cidade} - {estado}</b><br>
        ----------------------------------<br>
        {vagas_html}
        """

        pontos.append({
            "lat": float(coord["lat"]),
            "lon": float(coord["lon"]),
            "tooltip": tooltip_html
        })

    if not pontos:
        st.error("Nenhuma cidade válida para exibir no mapa.")
        return

    coords_df = pd.DataFrame(pontos)

    # Centraliza no Brasil
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
        get_radius=30000,
        get_color=[30, 136, 229, 200],
        pickable=True,
        auto_highlight=True,
        get_tooltip="tooltip"
    )

    # Tooltip custom
    tooltip = {
        "html": "{tooltip}",
        "style": {"backgroundColor": "rgba(20,20,20,0.9)", "color": "white"}
    }

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
    )

    st.pydeck_chart(deck)
