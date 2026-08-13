from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document 
from langchain_community.retrievers import BM25Retriever
from langchain_chroma import Chroma 
from langchain_huggingface import HuggingFaceEmbeddings
from rich.console import Console 
from config import DIR_PATH, COLLECTION_NAME, CHROMADB_PATH, K, THRESHOLD, HUGGINGFACE_EMBEDDINGS 



# Indexing
# Fase donde se cargan los documentos, se dividen en chunks, se generan los embeddings y se almacenan en Chroma 
class Indexing:

    def __init__(self, dir_path, collection_name, cosine=True, knn=True, debug=False, console=Console()):
        self.dir_path = dir_path
        self.collection_name = collection_name

        with console.status('[bold cyan]Loading embeddings model...\n[/]', spinner='dots'):
            self.embedding_function = HuggingFaceEmbeddings(model_name=HUGGINGFACE_EMBEDDINGS)
        self.debug = debug 
        self.console = console

        self.vectorstore_metadata = {}
        # Configuracion de la base de datos
        if cosine:
            # Podemos asignar similitud de coseno para medir el angulo entre los embeddings
            self.vectorstore_metadata['hnsw:space'] = 'cosine'
        else:
            # O podemos usar la distancia euclidea l2 para medir la distancia entre embeddings (comportamiento por defecto, pero me gusta dejarlo aclarado)
            self.vectorstore_metadata['hnsw:space'] = 'l2'
        if knn: 
            # Con flat implementamos el algoritmo KNN en lugar de ANN 
            # Esto es util si tenemos pocos chunks 
            self.vectorstore_metadata['chroma:hnsw_impl'] = 'flat'

    
    # Metodo para cargar todos los ficheros del directorio en la base de datos
    def create_vectorstore(self, vectorstore_path):
        path = Path(self.dir_path)
        # Hacemos una busqueda de todos los ficheros dentro del directorio en funcion de su extension
        extensions = ['*.py', '*.json', '*.html', '*.css', '*.js' , '*.jsx', '*.ts', '*.tsx', '*.yaml', '*.yml', '*.conf', '*.sh', '*.txt', '*.md', '*.lua']
        # Ignoramos algunos directorios usuales que aportan ruido 
        ignored_dirs = ('.venv', '.git', 'node_modules', '__pycache__', '.idea', '.vscode', 'dist', 'build')
        raw_documents = []
    
        for ext in extensions:
            for file_path in path.rglob(ext):
                 # Troceamos la ruta con .parts (/home/user/) -> ('/', 'home', 'user') y si estan en la lista negra pasamos al siguiente fichero
                if any(ignored in file_path.parts for ignored in ignored_dirs):
                    continue

                try:
                    # Obtenemos el texto del fichero con TextLoader
                    loader = TextLoader(str(file_path), encoding='utf-8')
                    # Los agregamos a la lista 
                    raw_documents.extend(loader.load())
                    self.console.print(f"[green]Loaded {file_path}[/]")
                except Exception as e:
                    # Si algún fichero da error de codificación o permisos, lo pasamos 
                    self.console.print(f"[bold red]ERROR --> {file_path}: {e}[/]")
                    continue

        if not raw_documents:
            raise ValueError(f"No se ha encontrado ningun documento valido en:  {self.dir_path}")

        # Ahora si, dividimos en chunks
        splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', '. ', ' ', ''],
            chunk_size=1000,
            chunk_overlap=200,
        )
        docs = splitter.split_documents(raw_documents)

        # Asignamos un ID a cada chunk 
        for i, doc in enumerate(docs):
            doc.metadata['id'] = str(i)

        if self.debug:
            self.console.print('Total chunks: ', len(docs))
            self.console.print('Creating database...')

        # Por ultimo guardamos los datos en Chroma, convirtiendolos en embeddings previamente
        vectorstore = Chroma.from_documents(
            documents=docs, 
            embedding=self.embedding_function,
            collection_name=self.collection_name,
            persist_directory=CHROMADB_PATH,
            collection_metadata=self.vectorstore_metadata
        )
        if self.debug:
            self.console.print('Created database in disk!')

        return vectorstore


    # Metodo para conectarnos a una base de datos de Chroma ya existente en disco 
    # Necesitamos el modelo que genera los embeddings para las nuevas queries del usuario 
    def load_vectorstore(self):
        # De esta manera obtenemos los chunks en forma de embeddings (vectores)
        if self.debug:
            self.console.print('Loading database...')
        vectorstore = Chroma(
            collection_name=self.collection_name, 
            embedding_function=self.embedding_function,
            persist_directory=CHROMADB_PATH,
            collection_metadata=self.vectorstore_metadata
        )
        if self.debug:
            self.console.print('Loaded database!')
        return vectorstore


    # Metodo para obtener el dense retriever 
    # Dense (denso) --> busca los k chunks mas similares en funcion de su significado (las palabras clave no tienen que coincidir exactamente)
    # (de todas formas, no estamos llamando a invoke(), por lo que solo estamos inicializando el retriever y no estamos buscando los k chunks mas proximos)
    def get_dense_retriever(self, vectorstore, similarity_score_threshold=False, mmr=False):
        # Usamos similarity_score_threshold para descartar aquellos chunks cuya puntuacion este por debjo del umbral 
        if similarity_score_threshold and not mmr:
            return vectorstore.as_retriever(
                search_type='similarity_score_threshold',
                search_kwargs={
                    'score_threshold': THRESHOLD,
                    'k': K
                }
            )
        # Tambien podemos usar MMR para descartar chunks similares entre si y evitar redundancia
        elif mmr and not similarity_score_threshold:
            return vectorstore.as_retriever(
                search_type='mmr',
                search_kwargs={'k': K}
            )
        else:
            return vectorstore.as_retriever(
                search_kwargs={'k': K}
        )
    

    # Sparse retriever 
    # Sparse (disperso) --> usa modelos estadisticos para encontrar las mayores coincidencias (exactas) de las palabras claves de la query del usuario
    # (de todas formas, no estamos llamando a invoke(), por lo que solo estamos inicializando el retriever y no estamos buscando los k chunks mas proximos)
    def get_sparse_retriever(self, vectorstore):
        # No podemos añadir todos los elementos de la base de datos en memoria del tiron, especialmente si son muchos chunks (22871 en mi caso)
        # Entonces los vamos añadiendo poco a poco, de 5000 en 5000, para no saturar el sistema 
        documents = []
        limit = 5000
        offset = 0
        # Obtenemos el total de elementos de la base de datos
        total = vectorstore._collection.count()
        
        while offset < total:
            # Con .get() obtemos los chunks con el texto original, sin la transformacion en vectores
            data = vectorstore._collection.get(
                limit=limit,
                offset=offset,
                include=['documents', 'metadatas']
            )
            if not data['documents']:
                break
            # Obtenemos la tanda de chunks en objetos Document     
            batch_docs = [
                Document(page_content=text, metadata=metadata)
                for text, metadata in zip(data['documents'], data['metadatas'])
            ]
            # Añadimos los documentos e incrementamos el offset, y seguimos con la siguiente tanda de 5000 chunks 
            documents.extend(batch_docs)
            offset += limit

        return BM25Retriever.from_documents(
            documents, 
            k=K
        )





if __name__ == '__main__':

    indexing = Indexing(DIR_PATH, COLLECTION_NAME, debug=True)
    vectorstore = indexing.create_vectorstore(CHROMADB_PATH)
    # vectorstore = indexing.load_vectorstore()
    dense_retriever = indexing.get_dense_retriever(vectorstore)
    sparse_retriever = indexing.get_sparse_retriever(vectorstore)

    print('\n')
    print('-'*50)
    print('Dense retriever: ', dense_retriever)
    print('Sparse retriever: ', sparse_retriever)
