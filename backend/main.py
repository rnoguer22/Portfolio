import shutil
import random 
import uuid
from fastapi import FastAPI, APIRouter, Form, File, UploadFile, Request, Response, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from ai.agents.portfolio_agent import *
from ai.rag.code.indexing_file import IndexingFile 
from ai.rag.code.retrieval import Retrieval 
from ai.rag.code.augmentation_generation import AugmentationGeneration
from ai.helpers.email_verification import send_email_verification
from ai.config import OPENAI_MODEL, TEMP_DIR, COLLECTION_NAME, EMAIL_PASSWD



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Cuando estemos en pro, poner dominio (https://moyete.dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

# Local memory storage for the codes. ESTO LO PONDREMOS CON UNA BD SQLITE MEJOR
otp_storage = {}
verified_sessions = set()

class EmailRequest(BaseModel):
    email: str

class VerifyRequest(BaseModel):
    code: str 



# Function to manage the user cookie 
async def get_set_user_cookie(request: Request, response: Response):
    user_cookie = request.cookies.get("user_cookie")
    # If the cookie doesnt exists (its the first the user access to the web in this device), we just create it
    if not user_cookie:
        user_cookie = str(uuid.uuid4())
        response.set_cookie(
            key="user_cookie",
            value=user_cookie, 
            max_age=60*60*24*30, # 60 hours, 60 min, 24h, 30 days = A whole month 
            httponly=True,
            samesite="lax"
        )
    return user_cookie



# Endpoint to check if the user has verified its email. We can check this with the cookie
@router.get("/auth/status")
async def check_auth_status(user_cookie: str = Depends(get_set_user_cookie)):
    is_verified = user_cookie in verified_sessions
    return {"verified": is_verified}


@router.post("/agent")
async def ask_agent(prompt: str = Form(...), 
                    file: UploadFile = File(None), 
                    user_cookie: str = Depends(get_set_user_cookie) # With Depends we inject dependencies in FastAPI
):
    # Addtional verification 
    if user_cookie not in verified_sessions:
        return {"error": "Please verify your email to enjoy the AI agent! Refresh the page to continue..."}

    print("\nReceived prompt: ", prompt)

    # ME GUSTARIA ALMACENAR LA COOKIE DEL USUARIO Y SU EMAIL EN UNA BD SQLITE, PARA ACCEDER PONER COLLECTION_NAME=USER_EMAIL
    # Aqui pondriamos una verificaicon que existe el correo asociado a la cookie en la bd, recuperamos el correo en funcion de la cookie y lo asignamos a collection_name
    # PERO PRIMERO VAMOS A VERIFICAR QUE FUNCIONA TODO CORRECTAMENTE
   
    # init the RAG Indexing phase, so that we can retrieve docs from the vectorstore and provide a precise answer to the user 
    indexing = IndexingFile(collection_name=user_cookie, debug=True)

    if file:
        print(f"Received file: {file.filename}")
        # We copy the file in our system so we can read it
        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR, exist_ok=True)
        temp_file_path = os.path.join(TEMP_DIR, file.filename)

        with open(temp_file_path, "wb") as buffer:
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
    if "error" in llm_response:
        error = llm_response["error"]
        print("\n[!] Error en el sistema: ", error)
        return {"error", error}

    elif "messages" in llm_response: 
        # By using inputs = {"messages": ...} format, we can not return {"message": llm_response} directly, we need to access to the response, which is the value of the "message" key
        latest_message = llm_response["messages"][-1]
        if latest_message.type == "ai" and latest_message.content:
            print("\nAgent: ", latest_message.content)
            return {"message": latest_message.content}
    else:
        return {"error": "Error: Unexpected error. Please try again later..."}



# Endpoint to send the verification code to the user 
@router.post("/auth/request-code")
async def request_code(data: EmailRequest, user_cookie: str = Depends(get_set_user_cookie)):
    email = data.email.strip()
    
    # Generate the code 
    code = str(random.randint(100000, 999999))
    # Storate it temporarly in memory (we will change this to a database)
    otp_storage[user_cookie] = {
        "email": email,
        "code": code 
    }

    # Finally send the verification code with the funcion defined in email_verification file
    success = send_email_verification(email, code)
    if not success:
        return {"error": "Could not send the code verification email. Please check SMTP config"}
    return {"message": "Verification code successfully sent!"}
    

@router.post("/auth/verify-code")
async def verify_code(data: VerifyRequest, user_cookie: str = Depends(get_set_user_cookie)):
    # Get the user"s data 
    user_data = otp_storage.get(user_cookie)
    if not user_data:
        return {"error": "There is no verification active request for this session."}
    if data.code.strip() != user_data["code"]:
        return {"error": "Invalid code. Please try again."}

    verified_email = user_data["email"]

    # La conexion ha tenido exito y aqui vinculariamos el correo con la cookie del usuario en la bbdd
    # Ya estableceriamos un limite en la base de datos de prompts pendientes (10 por ejemplo)
    # PENDIENTE POR HACER 
    
    # Add the user_cookie to the verified sessions 
    verified_sessions.add(user_cookie)
    del otp_storage[user_cookie]

    return {
        "success": True,
        "message": f"{verified_email} verified successfully! Granted access!"
    }



app.include_router(router)
