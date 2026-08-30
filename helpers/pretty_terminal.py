from rich.console import Console 
from rich.panel import Panel



# Clase muy sencilla, para establecer una pequeña interfaz de terminal 
class PrettyTerminal:

    def __init__(self):
        self.console = Console()

    def get_console(self):
        return self.console 


    # Metodo para obtener la query que el usuario quiere hacer al sistema RAG
    def get_user_query(self, name):
        user_query = self.console.input(
            f"\n[bold cyan]{name}[/] [bold white]> [/]"
        )
        return user_query


    # Metodo para mostrar informacion del proyecto antes de empezar
    def show_rag_init_info(self, model_name, embeddings_name):
        self.console.print(
            Panel.fit(
                "[bold cyan]📚 rnoguer22's RAG[/]\n\n"
                f"[green]Model[/]      {model_name}\n"
                f"[green]Embeddings[/] {embeddings_name}\n"
                "[green]Retriever[/]  Hybrid (BM25 + Dense)"
            )
        )

    def show_agent_init_info(self, model_name, web_search_provider):
        self.console.print(
            Panel.fit(
                "[bold cyan]📚 rnoguer22's Search Agent[/]\n\n"
                f"[green]Model[/]      {model_name}\n"
                f"[green]Web Search[/] {web_search_provider}\n"
            )
        )
