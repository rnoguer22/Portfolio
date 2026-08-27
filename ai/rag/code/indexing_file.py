import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredExcelLoader, UnstructuredPowerPointLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma 
from ai.config import COLLECTION_NAME
from ai.rag.code.indexing import Indexing 





# IndexingFile
# Clase similar a Indexing pero adaptada para el portfolio web, pensada para recibir un documento y añadirlo / crear base de datos 
class IndexingFile(Indexing):

    def __init__(self, collection_name=COLLECTION_NAME, cosine=True, knn=True, debug=False):
        super().__init__(dir_path=None, collection_name=collection_name, cosine=cosine, knn=knn, debug=debug)


    # Auxiliar method to load a file and split it in chunks
    def get_file_content(self, file_path):
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        # Load the file 
        file_type = path.suffix.lower()
        if file_type == '.pdf':
            loader = PyPDFLoader(str(path))
        elif file_type in ['.doc', '.docx']:
            loader = Docx2txtLoader(str(path))
        elif file_type in ['.xls', '.xlsx']:
            loader = UnstructuredExcelLoader(str(path))
        elif file_type in ['.ppt', '.pptx']:
            loader = UnstructuredPowerPointLoader(str(path))
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
            doc.metadata['id'] = f"{path.name}_chunk_{i}"

        return docs


    # Add file chunks to an existing database 
    def add_file(self, file_path):
        docs = self.get_file_content(file_path)

        if self.debug:
            self.console.print(f"Adding [bold white]({len(docs)})[/] chunks from file [bold cyan]{file_path}[/] to existing db...")
        if docs:
            # Add the documents to the existing vectorstore
            self.vectorstore.add_documents(docs)
            if self.debug:
                self.console.print("[green]Chunks added successfully![/]")
        else:
            print("Could not read file: ", file_path)

        return self.vectorstore
