import os
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma 
from ai.config import COLLECTION_NAME, CHROMADB_PATH
from ai.rag.code.indexing import Indexing 





# IndexingFile
# Clase similar a Indexing pero adaptada para el portfolio web, pensada para recibir un documento y añadirlo / crear base de datos 
class IndexingFile(Indexing):

    def __init__(self, collection_name=COLLECTION_NAME, cosine=True, knn=True, debug=False):
        super().__init__(dir_path=None, collection_name=collection_name, cosine=cosine, knn=knn, debug=debug)

        self.vectorstore_path = Path(CHROMADB_PATH) / collection_name
        self.vectorstore_path.mkdir(parents=True, exist_ok=True)
   

    # Auxiliar method to load a file and split it in chunks
    def _process_file(self, file_path):
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        # Load the file 
        if path.suffix.lower() == '.pdf':
            loader = PyPDFLoader(str(path))
        else:
            loader = TextLoader(str(path), encoding='utf-8')
        raw_documents = loader.load()

        # Split the document in chunks 
        splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', '. ', ' ', ''],
            chunk_size=1000,
            chunk_overlap=200,
        )
        docs = splitter.split_documents(raw_documents)

        # We add source file metadata to know its origin
        for i, doc in enumerate(docs):
            doc.metadata['id'] = path.name 

        return docs


    # Method to create the vectorstore and add file embeddings to it
    def create_vectorstore_from_file(self, file_path):
        docs = self._process_file(file_path)

        if self.debug:
            self.console.print(f"Creating database with file: [bold cyan]{file_path}[/] [bold white]({len(docs)})[/] chunks...")

        # With Chroma we get the embeddings and we save them in a vector database 
        vectorstore = Chroma.from_documents(
            documents=docs, 
            embedding=self.embedding_function,
            collection_name=self.collection_name,
            persist_directory=self.vectorstore_path,
            collection_metadata=self.vectorstore_metadata
        )
        if self.debug:
            self.console.print('[green]Created database in disk![/]')
        return vectorstore


    # Add file chunks to an existing database 
    def add_file(self, file_path):
        docs = self._process_file(file_path)

        # Load the existing vectorstore from its parent class 
        vectorstore = self.load_vectorstore(vectorstore_path=self.vectorstore_path)
        if self.debug:
            self.console.print(f"Adding [bold white]({len(docs)})[/] chunks from file [bold cyan]{file_path}[/] to existing db...")

        vectorstore.add_documents(docs)
        if self.debug:
            self.console.print("[green]Chunks added successfully![/]")
        return vectorstore


    # Method to check if the vectorstore is created
    def process_file(self, file_path):
        if os.path.exists(self.vectorstore_path) and os.listdir(self.vectorstore_path):
            return self.add_file(file_path)
        else:
            return self.create_vectorstore_from_file(file_path)
