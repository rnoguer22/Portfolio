import shutil
from time import sleep
from fastapi import FastAPI, APIRouter, Form, File, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from ai.agents.portfolio_agent import *
from ai.rag.code.indexing_file import IndexingFile 
from ai.rag.code.retrieval import Retrieval 
from ai.rag.code.augmentation_generation import AugmentationGeneration
from ai.config import OPENAI_MODEL, TEMP_DIR, COLLECTION_NAME



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Cuando estemos en pro, poner dominio (https://moyete.dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()



@router.post("/agent")
async def ask_agent(prompt: str = Form(...), file: UploadFile = File(None)):

    print("\nReceived prompt: ", prompt)
    # CHANGE THIS IN FUTURE SO THAT WE RECEIVE A COOKIE WITH A USER ID 
    user_cookie = "test"
    # init the RAG Indexing phase, so that we can retrieve docs from the vectorstore and provide a precise answer to the user 
    indexing = IndexingFile(collection_name=user_cookie, debug=True)

    if file:
        print(f"Received file: {file.filename}")
        # We copy the file in our system so we can read it
        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR, exist_ok=True)
        temp_file_path = os.path.join(TEMP_DIR, file.filename)

        with open(temp_file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"File saved temporarily in {temp_file_path}")

        # Store the file in the vectorstore
        indexing.add_file(temp_file_path)
        
    # A continuacion definimos el agente 
    agent = Portfolio_Agent(indexing_instance=indexing, ollama=False)
    app = agent.define_graph(AgentState)
    inputs = {
        "messages": [
            HumanMessage(content=prompt)
        ]
    }
    llm_response = app.invoke(inputs)

    # Check if we got an error 
    if 'error' in llm_response:
        error = llm_response['error']
        print("\n[!] Error en el sistema: ", error)
        return {'error', error}

    elif 'messages' in llm_response: 
        # By using inputs = {'messages': ...} format, we can not return {'message': llm_response} directly, we need to access to the response, which is the value of the 'message' key
        latest_message = llm_response['messages'][-1]
        if latest_message.type == 'ai' and latest_message.content:
            print('\nAgent: ', latest_message.content)
            return {'message': latest_message.content}
    else:
        return {'error': 'Error: Unexpected error. Please try again later...'}



app.include_router(router)



