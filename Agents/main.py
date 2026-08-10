from Agents.search_agent import *
from helpers.pretty_terminal import PrettyTerminal
from config import OPENAI_MODEL 



if __name__ == '__main__':

    pretty_terminal = PrettyTerminal()
    pretty_terminal.show_agent_init_info(model_name=OPENAI_MODEL, web_search_provider='Tavily')
    console = pretty_terminal.get_console()

    search_web = Search_Agent(ollama=False)
    app = search_web.define_graph(AgentState)
    color, text = search_web.draw_graph(app)
    console.print(f"[{color}]{text}[/]")

    while True:
        try:
            user_query = pretty_terminal.get_user_query(
                name='Web Search Agent'
            )
            if user_query:
                
                # Definimos los valores de la clase AgentState  
                inputs = {
                    'messages': [
                        HumanMessage(content=user_query)
                    ]
                }

                # Ejecutamos el grafo en modo streaming para ir viendo las decisiones y pasos del agente 
                for event in app.stream(inputs, stream_mode='values'):
                    latest_message = event['messages'][-1]
                    # Mostramos la conversacion con el agente 
                    # if latest_message.type == 'ai' and latest_message.content:
                    if latest_message.type == 'ai' and latest_message.content:
                        console.print('\n[cyan]Agente:\n[white]', latest_message.content)

        except KeyboardInterrupt:
            console.print('\nBye!')
            break

