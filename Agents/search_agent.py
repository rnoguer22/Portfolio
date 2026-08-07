import os
from typing import Literal
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from tavily import TavilyClient
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from config import GROQ_API_KEY, TAVILY_API_KEY, GROQ_MODEL



tavily_client = TavilyClient(TAVILY_API_KEY)

@tool 
def web_search(query: str) -> str:
    "Busca información actualizada en la web utilizando Tavily AI. Úsala cuando necesites datos de actualidad o recientes."
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
        return 'Error: Reached searches limit from Tavily, Try again later'


# Definimos las herramientas del agente
tools = [web_search]


# Iniciamos el LLM con Groq y le añadimos las herramientas 
llm = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY)
llm_with_tools = llm.bind_tools(tools)

# Definimos el estado del grafo mediante la clase AgentState
class AgentState(TypedDict):
    messages: list 


# A continuacion definimos los nodos del grafo 
# 1) Nodo del agente (cuando el LLM esta pensando)
def call_model(state: AgentState):
    messages = state['messages']
    system_prompt = SystemMessage(content=(
        "Eres un asistente de investigación web autónomo y preciso. "
        "Usa la herramienta 'web_search' cuando necesites datos recientes. "
        "No repitas búsquedas que ya se hayan realizado. "
        "Cuando tengas información suficiente, responde al usuario."
    ))
    # Inyectamos el prompt del sistema y llamamos al modelo 
    response = llm_with_tools.invoke([system_prompt] + messages)
    return {'messages': [response]}

# 2) Nodo condicional (deciede si llamar a las herramientas (tools) o terminar con la respuesta final)
def should_continue(state: AgentState) -> Literal['tools', END]:
    messages = state['messages']
    last_message = messages[-1]

    # Si el llm ha decidido ejecutar alguna de las herramientas, vamos al nodo "tools"
    if last_message.tool_calls:
        return 'tools'
    # Si por el contrario no hay llamadas a ninguna herramienta, el agente ha termiado 
    return END 


# Ahora construimos el StateGraph 
workflow = StateGraph(AgentState)

# Añadimos los nodos principales que hemos definido anteriormente
workflow.add_node('agent', call_model)
workflow.add_node('tools', ToolNode(tools))

# Definimos el punto de entrada del grafo 
workflow.set_entry_point('agent')
# Y las aristas condicionales y los ciclos del bucle ReAct 
workflow.add_conditional_edges(
    'agent',
    should_continue
)

# Despues de ejecutar las herramientas tenemos que tener una arista que vuelva a 'agent' para procesar el resultado
workflow.add_edge('tools', 'agent')

# Y compilamos el grafo para poder ejecutarlo y responder a las querys del usuario 
app = workflow.compile()





if __name__ == '__main__':

    query = 'Que ha pasado recientemente en Ceuta?'
    print('User: ', query)

    # Invocamos el grafo con la query del usario 
    inputs = {'messages': [HumanMessage(content=query)]}

    # Ejecutamos el grafo en modo streaming para ir viendo las decisiones y pasos del agente 
    for event in app.stream(inputs, stream_mode='values'):
        latest_message = event['messages'][-1]
        # Mostramos la conversacion con el agente 
        if latest_message.type == 'ai' and latest_message.content:
            print('Agente: ', latest_message.content)
