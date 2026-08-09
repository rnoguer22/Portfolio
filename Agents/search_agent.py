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

from config import GROQ_API_KEY, TAVILY_API_KEY, GROQ_MODEL, OLLAMA_MODEL, GOOGLE_MODEL, GOOGLE_API_KEY, OPENAI_API_KEY, OPENAI_MODEL





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



# Definimos el estado del grafo mediante la clase AgentState
class AgentState(TypedDict):
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
    def define_graph(self, state: AgentState):
        workflow = StateGraph(state)
        # Añadimos los nodos principales que hemos definido anteriormente
        workflow.add_node('agent', self.call_model)
        workflow.add_node('tools', ToolNode(self.tools))
        # Definimos el punto de entrada del grafo 
        workflow.set_entry_point('agent')
        # Y las aristas condicionales y los ciclos del bucle ReAct 
        workflow.add_conditional_edges(
            'agent',
            self.should_continue 
        )
        # Despues de ejecutar las herramientas tenemos que tener una arista que vuelva a 'agent' para procesar el resultado
        workflow.add_edge('tools', 'agent')
        # Y compilamos el grafo para poder ejecutarlo y responder a las querys del usuario 
        app = workflow.compile()
        return app 
