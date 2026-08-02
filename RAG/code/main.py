from indexing import Indexing 
from retrieval import Retrieval
from augmentation_generation import AugmentationGeneration
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq 
from config import DIR_PATH, COLLECTION_NAME, OLLAMA_MODEL, GROQ_MODEL, HUGGINGFACE_EMBEDDINGS
from rich.console import Console 
from rich.panel import Panel




# Clase muy sencilla, para establecer una pequeña interfaz de terminal 
class PrettyTerminal:

    def __init__(self, local=False):
        if local:
            self.model = ChatOllama(model=OLLAMA_MODEL)
            self.model_name = OLLAMA_MODEL
        else:
            self.model = ChatGroq(model=GROQ_MODEL)
            self.model_name = GROQ_MODEL
        self.embeddings_name = HUGGINGFACE_EMBEDDINGS
        self.console = Console()

    
    # Metodo para obtener la query que el usuario quiere hacer al sistema RAG
    def get_user_query(self):
        user_query = self.console.input(
            '\n[bold cyan]Obsidian RAG[/] [bold white]> [/]'
        )
        return user_query


    # Metodo para mostrar informacion del proyecto antes de empezar
    def show_init_info(self):
        self.console.print(
            Panel.fit(
                "[bold cyan]📚 rnoguer22's RAG[/]\n\n"
                f"[green]Model[/]      {self.model_name}\n"
                f"[green]Embeddings[/] {self.embeddings_name}\n"
                "[green]Retriever[/]  Hybrid (BM25 + Dense)"
            )
        )



if __name__ == '__main__':


    pretty_terminal = PrettyTerminal(local=False)
    pretty_terminal.show_init_info()

    # 1) Indexing 
    indexing = Indexing(DIR_PATH, COLLECTION_NAME, debug=False)
    vectorstore = indexing.load_vectorstore()
    dense_retriever = indexing.get_dense_retriever(vectorstore)
    sparse_retriever = indexing.get_sparse_retriever(vectorstore)

    # 2) Retrieval 
    retrieval = Retrieval(dense_retriever, sparse_retriever)  

    # 3) Augmentation 
    augmentation_generation = AugmentationGeneration(local=True)
    rag_chain_with_source = augmentation_generation.define_chain(retrieval)

    # Bucle infinito para que el usuario haga las preguntas que quiera 
    while True:
        try:
            # Obtenemos la query del usuario 
            user_query = pretty_terminal.get_user_query()
            if user_query:
                # 4) Generation 
                context, answer = augmentation_generation.generate_response(rag_chain_with_source, user_query)
                augmentation_generation.save_context_in_file(context)

        except KeyboardInterrupt as e:
            print('\nBye!')
            break
