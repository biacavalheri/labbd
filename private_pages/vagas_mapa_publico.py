import streamlit as st
from private_pages.db import get_connection
import pandas as pd
import pydeck as pdk
from geopy.geocoders import Nominatim

def main():
    st.title("🗺️ Distribuição Geográfica das Vagas")
    st.write("Explore o mapa interativo com detalhes das vagas ao clicar nos pontos.")

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

    st.info("⚠️ Geocodificação automática.")

    # Geocodificação
    geolocator = Nominatim(user_agent="vaga_mapa_interativo")
    coords = []

    for _, row in df.iterrows():
        try:
            loc = geolocator.geocode(f"{row['Cidade']}, {row['Estado']}, Brasil")
            if loc:
                coords.append({
                    "lat": loc.latitude,
                    "lon": loc.longitude,
                    "ID": row["ID"],
                    "Título": row["Título"],
                    "Empresa": row["Empresa"],
                    "Cidade": row["Cidade"],
                    "Estado": row["Estado"],
                    "Tipo": row["Tipo"],
                    "Salário": row["Salário"],
                    "Descrição": row["Descrição"]
                })
        except:
            pass

    if not coords:
        st.error("Nenhuma coordenada pôde ser gerada.")
        return

    coords_df = pd.DataFrame(coords)

    # -------------------------
    # CONFIGURAÇÃO DO MAPA
    # -------------------------

    view_state = pdk.ViewState(
        latitude=coords_df["lat"].mean(),
        longitude=coords_df["lon"].mean(),
        zoom=4,
        pitch=20,
    )

    # Camada dos pontos
    layer = pdk.Layer(
        "ScatterplotLayer",
        coords_df,
        get_position=["lon", "lat"],
        get_radius=30000,
        get_color=[0, 100, 255, 160],
        pickable=True,
        auto_highlight=True,
    )

    # Tooltip estilizado
    tooltip = {
        "html": """
        <b>{Título}</b><br>
        <b>Empresa:</b> {Empresa}<br>
        <b>Local:</b> {Cidade}/{Estado}<br>
        <b>Tipo:</b> {Tipo}<br>
        <b>Salário:</b> R$ {Salário}<br>
        """,
        "style": {
            "backgroundColor": "rgba(30, 30, 30, 0.8)",
            "color": "white"
        }
    }

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="mapbox://styles/mapbox/light-v9",
    )

    st.pydeck_chart(r)

    st.divider()
    st.subheader("📋 Vagas carregadas no mapa")
    st.dataframe(coords_df, use_container_width=True)
