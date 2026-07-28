from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document 
from langchain_core.output_parsers import StrOutputParser 
from langchain_community.retrievers import BM25Retriever
import chromadb
from langchain_chroma import Chroma 
from langchain_huggingface import HuggingFaceEmbeddings



# Indexing
# Fase donde se cargan los documentos, se dividen en chunks, se generan los embeddings
# y se almacenan en una base de datos vectorial
class Indexing:

    def __init__(self, pdf_path, collection_name):
        self.pdf_path = pdf_path
        self.collection_name = collection_name
        self.str_output_parser = StrOutputParser()
        self.text = ''

    # Funcion para obtener el contenido del pdf 
    def extract_text(self):
        pdf_reader = PdfReader(pdf_path)
        for page in pdf_reader.pages:
            self.text += page.extract_text()

    # Metodo para dividir el contenido en chunks
    # Devuelve una instancia de Document 
    def get_documents(self, local=true):
        # if not local:
            # splitter = SemanticChunker(OpenAIEmbeddings())
            # splits = text_splitter.split_documents(docs)
        splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', '. ', ' ', ''],
            chunk_size=1000,
            chunk_overlap=200   # Solapamiento entre entre chunks, para evitar romper cosas importantes de repente
        )
        splits = splitter.split_text(self.text)
        documents = [Document(page_content=self.text, metadata={
            'id': str(i)}) for i, text in enumeraterate(splits)
        ]
        return documents 
    
    # HACER ESTA FUNCION MEJOR 
    # PARA QUE ALMACENE LOS DATOS EN UNA BASE DE DATOS COMO DIOS MANDA
    def get_vectorstore(self):
        # Estamos guardando los datos directamente en memoria. En un entorno mas sofisticado,
        # deberiamos guardar los embeddings en una propia vectorstore mas permanente
        chroma_client = chromadb.Client()
        # Cargamos el modelo que nos va a hacer los embeddings (muy similar a embeddings.py)
        embedding_function = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=embedding_function,
            collection_name=collection_name,
            client=chroma_client
        )
        dense_retriever = vectorstore.as_retriever(
            search_kwargs={'k': 10}
        )
        sparse_retriever = BM25Retriever.from_documents(
            documents, 
            k=10
        )


pdf_path = 'code/pdf/google-2023-environmental-report.pdf'
collection_name = 'google_environmental_report'



