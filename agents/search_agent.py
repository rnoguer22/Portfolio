import os
from typing import Literal
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama 
from langchain_openai import ChatOpenAI 
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import Annotated 
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
import pprint

from config import GROQ_API_KEY, TAVILY_API_KEY, GROQ_MODEL, OLLAMA_MODEL, GOOGLE_MODEL, GOOGLE_API_KEY, OPENAI_API_KEY, OPENAI_MODEL, GRAPH_PATH





tavily_client = TavilyClient(TAVILY_API_KEY)

@tool 
def web_search(query: str) -> str:
    'Search the web for recent information'
    print(f"\n[🛠️ LangGraph Ejecutando Tavily Tool para: '{query}']")
    try:
        # Respuesta basica, ya que tenemos limitaciones con el llm de groq que no puede acumular mucho contexto 
        response = tavily_client.search(
            query=query,
            search_depth='basic',
            max_results=3
        )
        results = response.get('results', [])
        if not results:
            return 'Error: Information not found'

        cleaned_response = []
        for result in results:
            title = result.get('title')
            url = result.get('url')
            score = result.get('score')
            # Lo mismo, limitamos el content a 1000 caracteres para evitar saturar el contexto del modelo 
            content = result.get('content')[:1000]
            cleaned_response.append(f"Title: {title}\nURL: {url}\nScore: {score}\nContent: {content}\n")
        return '\n---\n'.join(cleaned_response)

    except Exception as e:
        return 'Error: Reached searches limit for Tavily, Try again later'



# Definimos el estado del grafo mediante la clase AgentState, la cual hereda la estructura de TypedDict 
# TypedDict es un diccionario con claves fijas, de manera que AgentState sera un diccionario (de TypedDict) que siempre tendra una key 'messages'
class AgentState(TypedDict):
    # Usamos Annotated y add_messages para no sobreescribir los metadatos del agente, manteniendo la memoria de todo el flujo del agente 
    # Se gestiona automaticamente con Langraph y add_messages, cogiendo cualquier diccionario con key 'messages' que devuelva 
    # cualquier nodo del grafo (en este caso 'agent' con call_model) y los fusiona progresivamente
    messages: Annotated[list, add_messages]



class Search_Agent:

    def __init__(self, ollama=False):
        self.tools = [web_search]
        if ollama:
            llm = ChatOllama(model=OLLAMA_MODEL)
        else:
            llm = ChatOpenAI(
                model=OPENAI_MODEL,
                api_key=OPENAI_API_KEY,
                max_tokens=2000, # Limite de tokens en la salida, ahora que estamos incluyendo modelos die pago 
                reasoning_effort='low' # Lo mismo, para que piense menos el modelo y gaste menos tokens
            )
        self.llm_with_tools = llm.bind_tools(self.tools)
        

    # A continuacion definimos los nodos del grafo 
    # 1) Nodo del agente (cuando el LLM esta pensando)
    def call_model(self, state: AgentState):
        messages = state['messages']
        system_prompt = SystemMessage(content=(
            "Usa la tool web_search para responder preguntas sobre información actual. "
            "Llama a la tool usando el mecanismo de function calling, nunca escribas la llamada como texto."
            "IMPORTANTE: Si ya tienes resultados de una búsqueda anterior en la conversación, "
            "NO vuelvas a buscar lo mismo. Usa esos resultados para responder directamente al usuario en texto."
        ))
        # Inyectamos el prompt del sistema y llamamos al modelo 
        response = self.llm_with_tools.invoke([system_prompt] + messages)
        return {'messages': [response]}


    # 2) Nodo condicional (deciede si llamar a las herramientas (tools) o terminar con la respuesta final)
    def should_continue(self, state: AgentState) -> Literal['tools', END]:
        messages = state['messages']
        last_message = messages[-1]
        # Si el llm ha decidido ejecutar alguna de las herramientas, vamos al nodo "tools"
        if last_message.tool_calls:
            return 'tools'
        # Si por el contrario no hay llamadas a ninguna herramienta, el agente ha termiado 
        return END 


    # Metodo para construir el grafo 
    # Implementa el patron ReAct -> el llm razona sobre la query del usuario, decide si debe usar una herramienta o no antes de dar la respuesta final 
    def define_graph(self, state: AgentState):
        workflow = StateGraph(state)
        # El primer nodo es la funcion call_model, para que el llm decida si debe ejecutar la herramienta o no 
        workflow.add_node('agent', self.call_model)
        # El segundo nodo es el nodo de herramientas (de momento solo se puede hacer una busqueda en internet)
        workflow.add_node('tools', ToolNode(self.tools))
        # Definimos el punto de entrada del grafo 
        workflow.set_entry_point('agent')
        # Y las aristas condicionales para el bucle ReAct 
        # Con esto tras el nodo 'agent' se ejecuta la herramienta o se finaliza el flujo del agente generando una respuesta. Depende de lo que haya decidido el agente en call_model 
        workflow.add_conditional_edges(
            'agent',
            self.should_continue 
        )
        # Añadimos una arista para volver al nodo 'agent' automaticamente despues del nodo 'tool', 
        # para evaluar si ya se tiene el contexto necesario o hay que ejecutar algo mas 
        workflow.add_edge('tools', 'agent')
        # Y compilamos el grafo para poder ejecutarlo y responder a las querys del usuario 
        app = workflow.compile()
        
        return app 


    # Metodo para dibujar el grafo en una imagen
    def draw_graph(self, app):
        color = 'green'
        try:
            png_bytes = app.get_graph().draw_mermaid_png()
            with open(GRAPH_PATH, "wb") as f:
                f.write(png_bytes)
            text = f"\n[✔] Imagen del grafo guardada con éxito en '{GRAPH_PATH}'"
        except Exception as e:
            color = 'red'
            text = f"\n[!] No se pudo generar la imagen: {e}"
        return color, text
