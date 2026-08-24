import shutil
from fastapi import FastAPI, APIRouter, Form, File, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from ai.agents.search_agent import *
from ai.rag.code.indexing_file import IndexingFile 
from ai.config import OPENAI_MODEL, TEMP_DIR



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
        # We copy the file in our system so we can read it
        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR, exist_ok=True)
        temp_file_path = os.path.join(TEMP_DIR, file.filename)

        with open(temp_file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"File saved temporarily in {temp_file_path}")

        indexing = IndexingFile(debug=True)
        indexing.process_file(temp_file_path)

    '''
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
    '''


'''
@router.post('/upload')
async def upload_document(file: UploadFile = File(...)):
    print('Uploadiing ', file.filename, '...')
    try:
        indexing = Indexing(DIR_PATH, COLLECTION_NAME, debug=True)
        vectorstore = indexing.load_vectorstore()
'''


app.include_router(router)
