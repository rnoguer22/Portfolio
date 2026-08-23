from fastapi import FastAPI, APIRouter, Form, File, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from ai.agents.search_agent import *
from ai.config import OPENAI_MODEL 



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Cuando estemos en pro, poner dominio (https://moyete.dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()



@router.post('/agent')
async def ask_agent(prompt: str = Form(...), file: UploadFile = File(None)):

    print("Received prompt: ", prompt)
    if file:
        print(f"Received file: {file.filename}")
        content = await file.read()
        print(f"Size: {file.size} bytes")
        try:
            text = content.decode('utf-8')
            print('File content: ', text)
        except UnicodeDecodeError:
            print('Binary file (PDF, img) and cannot be read (for now jeje)')

    search_web = Search_Agent(ollama=False)
    app = search_web.define_graph(AgentState)

    inputs = {
        'messages': [
            HumanMessage(content=prompt)
        ]
    }
    llm_response = app.invoke(inputs)

    latest_message = llm_response['messages'][-1]
    if latest_message.type == 'ai' and latest_message.content:
        print('\nAgente: ', latest_message.content)
        return {"message": latest_message.content}



app.include_router(router)
