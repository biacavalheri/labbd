import psycopg2
import streamlit as st

def get_connection():
    try:
        return psycopg2.connect(
            host=st.secrets["db"]["host"],
            dbname=st.secrets["db"]["dbname"],
            user=st.secrets["db"]["user"],
            password=st.secrets["db"]["password"],
            port=st.secrets["db"]["port"],
            sslmode="require"
        )
    except Exception as e:
        st.error(f"Erro ao conectar no banco: {e}")
        return None
