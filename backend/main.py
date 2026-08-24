import shutil
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

        # 1) Indexing
        indexing = IndexingFile(debug=True)
        vectorstore = indexing.process_file(temp_file_path)
        dense_retriever = indexing.get_dense_retriever(vectorstore)
        sparse_retriever = indexing.get_sparse_retriever(vectorstore)

        # 2) Retrieval 
        retrieval = Retrieval(dense_retriever, sparse_retriever)  

        # 3) Augmentation 
        augmentation_generation = AugmentationGeneration(local=False)
        rag_chain_with_source = augmentation_generation.define_chain(retrieval)

        # 4) Generation 
        context, llm_response = augmentation_generation.generate_response(rag_chain_with_source, prompt)
        # collection_name will be replaced with an user id (maybe email, or similar), but for now we define it as a constant while developing
        collection_name = COLLECTION_NAME
        augmentation_generation.save_context_in_file(context, collection_name)
        print('\nResponse: ', llm_response)
        return {'message': llm_response}

    else:
        agent = Portfolio_Agent(ollama=False)
        app = agent.define_graph(AgentState)
        inputs = {
            'messages': [
                HumanMessage(content=prompt)
            ]
        }
        llm_response = app.invoke(inputs)
        # By using inputs = {'messages': ...} format, we can not return {'message': llm_response} directly, we need to access to the response, which is the value of the 'message' key
        latest_message = llm_response['messages'][-1]
        if latest_message.type == 'ai' and latest_message.content:
            print('\nAgent: ', latest_message.content)
            return {'message': latest_message.content}



app.include_router(router)
