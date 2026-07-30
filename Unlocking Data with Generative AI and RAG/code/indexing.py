from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document 
from langchain_core.output_parsers import StrOutputParser 
from langchain_community.retrievers import BM25Retriever
import chromadb
from langchain_chroma import Chroma 
from langchain_huggingface import HuggingFaceEmbeddings
from config import PDF_PATH, COLLECTION_NAME, K



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
        pdf_reader = PdfReader(self.pdf_path)
        for page in pdf_reader.pages:
            self.text += page.extract_text()
        return self.text 


    # Metodo para dividir el contenido en chunks
    # Devuelve una instancia de Document 
    def get_documents(self, local=True):
        # if not local:
            # splitter = SemanticChunker(OpenAIEmbeddings())
            # splits = text_splitter.split_documents(docs)
        splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', '. ', ' ', ''],
            chunk_size=1000,
            chunk_overlap=200   # Solapamiento entre entre chunks, para evitar romper cosas importantes de repente
        )
        splits = splitter.split_text(self.text)
        print(len(splits))
        documents = [Document(page_content=split_text, metadata={
            'id': str(i)}) for i, split_text in enumerate(splits)
        ]
        return documents 


    # HACER ESTA FUNCION MEJOR 
    # PARA QUE ALMACENE LOS DATOS EN UNA BASE DE DATOS COMO DIOS MANDA
    def get_vectorstore(self, documents):
        # Estamos guardando los datos directamente en memoria. En un entorno mas sofisticado,
        # deberiamos guardar los embeddings en una propia vectorstore mas permanente
        chroma_client = chromadb.Client()
        # Cargamos el modelo que nos va a hacer los embeddings (muy similar a embeddings.py)
        embedding_function = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=embedding_function,
            collection_name=self.collection_name,
            client=chroma_client
        )
        return vectorstore


    # Metodo para obtener el dense retriever 
    # Dense (denso) --> busca los k chunks mas similares en funcion de su significado (las palabras clave no tienen que coincidir exactamente)
    # (de todas formas, no estamos llamando a invoke(), por lo que solo estamos inicializando el retriever y no estamos buscando los k chunks mas proximos)
    def get_dense_retriever(self, vectorstore):
        return vectorstore.as_retriever(
            search_kwargs={'k': K}
        )
    

    # Sparse retriever 
    # Sparse (disperso) --> usa modelos estadisticos para encontrar las mayores coincidencias (exactas) de las palabras claves de la query del usuario
    # (de todas formas, no estamos llamando a invoke(), por lo que solo estamos inicializando el retriever y no estamos buscando los k chunks mas proximos)
    def get_sparse_retriever(self, documents):
        return BM25Retriever.from_documents(
            documents, 
            k=K
        )



if __name__ == '__main__':

    pdf_path = PDF_PATH
    collection_name = COLLECTION_NAME

    indexing = Indexing(pdf_path, collection_name)
    indexing.extract_text()
    docs = indexing.get_documents()
    vectorstore = indexing.get_vectorstore(docs)
    dense_retriever = indexing.get_dense_retriever(vectorstore)
    sparse_retriever = indexing.get_sparse_retriever(docs)

    print('\n')
    print('-'*50)
    print('Dense retriever: ', dense_retriever)
    print('Sparse retriever: ', sparse_retriever)
