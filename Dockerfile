# PYTHON
FROM python:3.13-alpine

# dentro del contenedor voy a crear una carpeta que se llama /app 
WORKDIR /app-dnd

#Comando lo que estoy haciendo es pasar todo lo que tengo en el directorio en el que se 
#encuentra el Dockerfile (CON EL PRIMER PUNTO) al contenedor en el directorio que le hemos creado (EL SEGUNDO PUNTO)
COPY api/ /api/
COPY app/ /app/
COPY docs/ /docs/
COPY src/ /src/
COPY __init__.py . 
COPY README.md . 
COPY .env . 
COPY requirements.txt . 

# Instalar librerias de python
RUN pip install --no-cache-dir -r requirements.txt

# Puertos
EXPOSE 8000
EXPOSE 8501

# Ejecutar FastAPI y Streamlit al mismo tiempo
CMD uvicorn api.main:app --host 0.0.0.0 --port 8000 & streamlit run /app/app.py --server.port 8501 --server.address 0.0.0.0
