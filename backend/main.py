from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Cuando estemos en pro, poner dominio (https://moyete.dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

# Con esta clase definimos el formato de los datos que provienen del front
class QueryRequest(BaseModel):
    prompt: str 


@router.post('/agent')
async def ask_agent(data: QueryRequest):
    response = f"You've asked: {data.prompt}"
    return {"message": response}


app.include_router(router)
