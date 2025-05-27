##########################################
#####            Librerias           #####
##########################################

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from src.clases import DnDPersonaje, save_character_to_db
from unidecode import unidecode
import os

#----------------------------------------------------------------------------------------------------------------------------------

# Creamos las variables para iniciar el proceso
#config = dotenv_values(".env")

config = {"gemini_api_key": os.environ.get("gemini_api_key")}

if not config["gemini_api_key"]:
    raise RuntimeError("Falta la variable de entorno 'gemini_api_key'")


personaje = DnDPersonaje()
paso_actual = {"etapa": "inicio"}

# Llamamos al la base de datos vectorizada
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local("src/faiss_index", embedding_model, allow_dangerous_deserialization=True)
retriever = db.as_retriever(search_kwargs={"k": 3})

#----------------------------------------------------------------------------------------------------------------------------------

#**********************************************************************************
def consulta_manual(text: str) -> str:
    '''
    Responde consultas basadas únicamente en el Manual del Jugador de Dungeons & Dragons.
    La entrada es una pregunta en texto y la salida es una respuesta relevante basada solo en el manual.
    Si esta herramienta devuelve una respuesta satisfactoria, no se debe usar ninguna otra herramienta ni conocimiento externo.
    '''
    docs = retriever.get_relevant_documents(text)
    contexto = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""Responde a la siguiente pregunta usando exclusivamente la información del Manual del Jugador de Dungeons & Dragons.
            No inventes ni agregues nada fuera del contenido proporcionado.

            Contenido del manual:
            ---------------------
            {contexto}

            Pregunta:
            {text}

            Respuesta:"""
    chat = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=config['gemini_api_key'])
    return chat.invoke(prompt).content.strip()

#**********************************************************************************

def crear_personaje_pasoa_paso(_):
    etapa = paso_actual["etapa"]

    if etapa == "inicio":
        paso_actual["etapa"] = "raza"
        return "Vamos a crear tu personaje. Primero, elige una raza: Humano, Elfo, Enano, Mediano, Tiefling u Orco."

    elif etapa == "raza":
        paso_actual["etapa"] = "clase"
        return "Genial. Ahora elige una clase: Guerrero, Mago, Clérigo, Pícaro, Druida o Bardo."

    elif etapa == "clase":
        paso_actual["etapa"] = "final"
        save_character_to_db({
            "raza": personaje.raza,
            "clase": personaje.clase
        })
        personaje.guardado = True
        return f"Personaje guardado:\nRaza: {personaje.raza}\nClase: {personaje.clase}"

    else:
        return "Ya creaste el personaje. Si deseas empezar de nuevo, puedes reiniciar."

#**********************************************************************************
def eliminar_acentos(texto: str) -> str:
    ''' 
    Función para quitar los acentos y hacer minúsculas.
    '''
    if isinstance(texto, str):
        return unidecode(texto.lower())
    return texto


def actualizar_datos_personaje(mensaje, personaje):
    mensaje = eliminar_acentos(mensaje)
    

    razas = ["humano", "elfo", "enano", "mediano", "tiefling", "orco"]
    clases = ["guerrero", "mago", "clerigo", "picaro", "druida", "bardo"]

    for r in razas:
        if r in mensaje:
            raza = r
            personaje.raza = raza.capitalize()
            break

    for m in clases:
        if m in mensaje:
            clase = m
            personaje.clase = clase.capitalize()
            break
            
            
    if personaje.raza and personaje.clase and not personaje.guardado:
        save_character_to_db({
            "raza": personaje.raza,
            "clase": personaje.clase
        })
        personaje.guardado = True
        
#**********************************************************************************

#----------------------------------------------------------------------------------------------------------------------------------

# Con toda esta info creamos a los agentes para cada endpoint.

#**********************************************************************************
def ag_personaje():
    chat = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=config['gemini_api_key'], temperature=0)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    def reiniciar_personaje(mensaje:str) -> str:
        nonlocal memory
        global personaje, paso_actual
        personaje = DnDPersonaje()
        paso_actual = {"etapa": "inicio"}
        memory.clear()
        return "Proceso reiniciado. ¿Quieres crear un nuevo personaje?"

    tools_personaje = [
    Tool(
        name="CrearPersonajePasoAPaso",
        func=crear_personaje_pasoa_paso,
        description="Guía al usuario para crear un personaje paso por paso."),
    Tool(
    name="ReiniciarPersonaje",
    func=reiniciar_personaje,
    description="Reinicia el flujo de creación del personaje actual")]
    
    agent_personaje = initialize_agent(
    tools=tools_personaje,
    llm=chat,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True)
    return agent_personaje


#**********************************************************************************

def ag_manual():
    chat = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=config['gemini_api_key'])
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    tools_manual = [
    Tool(
        name="ConsultarManualDND",
        func=consulta_manual,
        description="Consulta el Manual del Jugador de D&D para responder preguntas del manual como razas, clases, reglas, etc."
    )]
    agent_manual = initialize_agent(
    tools=tools_manual,
    llm=chat,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True)
    return agent_manual

print('Agentes han sido creados.')