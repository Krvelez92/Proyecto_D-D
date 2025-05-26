##########################################
#####            Librerias           #####
##########################################


from fastapi import FastAPI
from pydantic import BaseModel
from src.memoria_agente import ag_personaje, actualizar_datos_personaje, ag_manual
from src.clases import DnDPersonaje
import sqlite3

#------------------------------------------------------------

app = FastAPI()

#------------------------------------------------------------

@app.get("/")
async def inicio():
    return {"Inicio": "Bienvenidos a la API de D&D."}

#------------------------------------------------------------

@app.post("/crear_bd")
def crear_base_datos():
    try:
        conn = sqlite3.connect("./api/bd/dnd.db")
        cursor = conn.cursor()

        cursor.execute('DROP TABLE IF EXISTS characters;')



        cursor.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                raza TEXT,
                clase TEXT );
        ''')

        conn.commit()
        conn.close()

        return {"mensaje": "Base de datos y tabla creada correctamente."}

    except Exception as e:
        return {"error": str(e)}

#------------------------------------------------------------

agente1 = ag_personaje()
personaje = DnDPersonaje()
paso_actual = {"etapa": "inicio"}


class Message(BaseModel):
    message: str

@app.post("/chat-crear-personaje")
def chat(msg: Message):
    mensaje = msg.message
    respuesta = agente1.invoke(mensaje)
    actualizar_datos_personaje(mensaje, personaje)
    return {"response": respuesta}

#------------------------------------------------------------

@app.get("/all_bd")
def mirar_bd():
    conn = sqlite3.connect("./api/bd/dnd.db")
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    rows = cursor.execute('select * from characters;').fetchall()
    conn.close()
    result = [dict(row) for row in rows]
    return {'characters': result}

#------------------------------------------------------------

agente2 = ag_manual()

@app.post('/chat-consulta-manual')
def consulta_chat(msg:Message):
    mensaje = msg.message
    respuesta = agente2.invoke(mensaje)    
    return {"response": respuesta}