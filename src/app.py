##########################################
#####            Librerias           #####
##########################################

import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Creador de Personaje D&D", layout="centered", page_icon=':game_die:')

st.title("🧙 Creador de Personajes de D&D")

tab1, tab2, tab3 = st.tabs(["🧙 Crear Personaje", "📖 Consultar Manual", "📜 Personajes Guardados"])


# -------------------------------------------------------------------------

with tab1:
    st.header("🧝 Creador de Personaje")

    st.image(
    "https://i.ytimg.com/vi/H9GI9HHbBao/maxresdefault.jpg",
    caption="Dungeons & Dragons", use_container_width=True, width=150)

    mensaje_personaje = st.text_input("💬 Escribe tu mensaje para crear un personaje", "")

    if mensaje_personaje:
        with st.spinner("Creando personaje..."):
            response = requests.post(
                f"{API_URL}/chat-crear-personaje",
                json={"message": mensaje_personaje}
            )
            if response.status_code == 200:
                data = response.json()
                st.markdown("### 🤖 Respuesta:")
                st.success(data["response"]["output"])

                if "etapa" in data:
                    st.markdown(f"**Etapa actual:** {data['etapa'].capitalize()}")
            else:
                st.error("Error al conectar con la API.")

# -------------------------------------------------------------------------
with tab2:
    st.header("📚 Consultar el Manual de Jugador")

    st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://www.pixartprinting.it/blog/wp-content/uploads/2024/07/IMMAGINE-9-779x1024.jpeg" 
             width="250" />
        <p><em>Manual</em></p>
    </div>
    """,
    unsafe_allow_html=True)


    consulta_manual = st.text_input("🔍 ¿Qué quieres saber?", "")

    if consulta_manual:
        with st.spinner("Buscando en el manual..."):
            response = requests.post(
                f"{API_URL}/chat-consulta-manual",
                json={"message": consulta_manual}
            )
            if response.status_code == 200:
                st.markdown("### 📘 Respuesta del Manual:")
                st.info(response.json()["response"]["output"])
            else:
                st.error("Error al consultar el manual.")

# -------------------------------------------------------------------------

with tab3:
    st.header("📜 Lista de Personajes Guardados")

    if st.button("🔄 Cargar personajes"):
        response = requests.get(f"{API_URL}/all_bd")
        if response.status_code == 200:
            personajes = response.json()["characters"]
            if personajes:
                for i, p in enumerate(personajes, 1):
                    st.markdown(f"**{i}.** 🧝 Raza: `{p['raza']}` | 🛡️ Clase: `{p['clase']}`")
            else:
                st.info("No hay personajes aún.")
        else:
            st.error("No se pudo recuperar la base de datos.")