<p align="center">
  <img src="https://images.ctfassets.net/swt2dsco9mfe/2jKQC6i2BM1HNQIzau3Biv/01bee47c8170a7d7f3f54f79777c4f3e/158867_670x370.jpg" alt="Dungeons and Dragons" width="700"/>
</p>

# 🐉 Creador de Personajes para Dungeons & Dragons (D&D)

Este proyecto es una aplicación interactiva para crear personajes de D&D paso a paso, consultar información del manual del jugador y visualizar personajes guardados. Combina un backend en **FastAPI (contenedizado con Docker)** y una interfaz amigable construida con **Streamlit**.

---

## 📦 Repositorio

🔗 https://github.com/Krvelez92/Proyecto_D-D

---

## 🚀 ¿Qué puedes hacer?

✅ Crear personajes de D&D mediante conversación con un asistente IA  

✅ Consultar contenido del manual del jugador  

✅ Guardar automáticamente el personaje en una base de datos 

✅ Visualizar los personajes creados desde una pestaña del frontend  

---

## 🛠️ Tecnologías utilizadas

- 🐍 Python 3.10+
- ⚡ **FastAPI** — backend para manejar la conversación y guardar personajes
- 🐳 **Docker** — para desplegar la API de manera portátil
- 🌐 **Streamlit** — frontend interactivo
- 🧠 **LangChain + Gemini API** (Google) — agente conversacional
- 🗃 **SQLite** — base de datos para los personajes

---
## 📁 Estructura del proyecto

```
Proyecto_D-D/
│
├── api/ # Código del backend (FastAPI)
│ ├── main.py
│ └── bd
│      └── dnd.db # Base de datos en local
│
├── src/ # Agente, lógica de personaje y herramientas
│ ├── clases.py # Clases de personaje Creados
│ ├── memoria_agente.py # Funciones para configuracion de agentes
│ └── embeddings.py # Vectorizacion y embedding para documento de manual de usuario
│
├── app/ # Código Interfaz Streamlit (Front)
│ └── app.py
│
├── requirements.txt # Dependencias
│
├── docs/ # Documentos y presentaciones
│ └── Dungeons_and_Dragons_Players_Handbook_2024.pdf
│
├── notebooks/ # jupyter notebooks de prueba de los agentes
│ └── prueba.ipynb
│
└── README.md # Este archivo
```

**Extra**

Para el funcionamiento de todo esto, te recomendamos que uses un entorno virtual.
```
python -m venv entorno_virtual
.\entorno_virtual\Scripts\Activate       # En Windows
# source entorno_virtual/bin/activate    # En Mac/Linux
```
## 🧩 Instala Dependencias
```
pip install -r requirements.txt
```
## 🔐 Configura .env
Crea un archivo .env con tu clave de Google Gemini:
```
gemini_api_key=TU_CLAVE_SECRETA
```
## 🧪 Endpoints útiles
POST /chat-crear-personaje — conversa para crear un personaje

POST /chat-consulta-manual — consulta el manual del jugador

GET /all_bd — ver todos los personajes guardados

La documentación automática de la API está disponible en:
👉 http://localhost:8000/docs

## 🎲 ¡A jugar!
Usa este sistema para generar personajes, aprender las reglas y sumergirte en el mundo de Dungeons & Dragons con ayuda de la IA.

## 🤝 Contribuciones
¡Pull requests y sugerencias son bienvenidas!





🧙 **Autor**
Desarrollado por Krvelez92 🛡️

