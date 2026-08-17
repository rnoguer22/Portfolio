from fastapi import APIRouter
from pydantic import BaseModel



router = APIRouter()

# Con esta clase definimos el formato de los datos que provienen del front
class QueryRequest(BaseModel):
    prompt: str 



@router.post('/agent')
async def ask_agent(data: QueryRequest):
    # Aqui llamariamos al agente, al rag, etc.
    # De momento no lo hacemos para enfocarnos en el html de la pagina 
    
