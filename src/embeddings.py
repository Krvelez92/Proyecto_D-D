##########################################
#####          LIBRERIAS             #####
##########################################

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import pdfplumber
from langchain.schema import Document

#----------------------------------------------------------------------------------------------------------------------------------

def load_pdf_text(filepath:str) -> list:
    ''' 
    Función para leer el pdf y extraer datos página por página.

    Inputs:
        filepath:str
    
    Output:
        docs:list    
    '''
    docs = []
    with pdfplumber.open(filepath) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and len(text.strip()) > 0:
                docs.append(Document(page_content=text, metadata={"page": i + 1}))
    return docs

#----------------------------------------------------------------------------------------------------------------------------------

docs = load_pdf_text('./docs/Dungeons_and_Dragons_Players_Handbook_2024.pdf') # Cargamos el documento desde la carpeta docs y pasamos por función load_pdf_text.

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200) # Dividimos en chunks el documento para poder cargarlo y dividirlo.
chunks = splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2") # Usamos embeddings de HuggingFace pro que google no tiene el suyo aun.

vector_store = FAISS.from_documents(docs, embeddings) # Vectorizar con FAISS

vector_store.save_local("src/faiss_index") # Guardamos la bbdd vertorizada del documento.


print('Una instancia de la BBDD de vectores se ha cargado en "faiss_index".')