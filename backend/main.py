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
from helpers.email_verification import send_email_verification
from helpers.telegram_alert import send_telegram_alert
from helpers.sqlite3_db import Sqlite3_Db 
from config import OPENAI_MODEL, TEMP_DIR, COLLECTION_NAME, EMAIL_PASSWD



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.1.65:3000",
                   "http://localhost:3000",
                   "http://127.0.0.1:3000"], # Cuando estemos en pro, poner dominio (https://moyete.dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

# Initialize the database 
db = Sqlite3_Db()
db.init_db()

# Local memory storage for the codes
codes = {}
MAX_FILE_SIZE = 5 * 1024 * 1024


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
    print('User cookie: ', user_cookie)
    return user_cookie



# Endpoint to check if the user has verified its email. We can check this with the cookie
@router.get("/auth/status")
async def check_auth_status(user_cookie: str = Depends(get_set_user_cookie)):
    is_verified = db.is_cookie_verified(user_cookie)
    return {"verified": is_verified}


@router.post("/agent")
async def ask_agent(prompt: str = Form(...), 
                    file: UploadFile = File(None), 
                    user_cookie: str = Depends(get_set_user_cookie) # With Depends we inject dependencies in FastAPI
):
    # Addtional verification 
    if not db.is_cookie_verified(user_cookie):
        return {"error": "Access denied. Please verify your email to continue. Refresh the page..."}
    # Requests left verification 
    if db.get_requests_left(user_cookie) == 0:
        return {"error": "You have reached the requests limit. Thank you for using rnoguer's Portfolio! Contact Ruben to provide objective feedback about your experience!"}

    print("\nReceived prompt: ", str(prompt), " --> ", prompt)
    # init the RAG Indexing phase, so that we can retrieve docs from the vectorstore and provide a precise answer to the user 
    indexing = IndexingFile(collection_name=user_cookie, debug=True)

    if file:
        print(f"Received file: {file.filename}")
        # Check the file size
        if file.size > MAX_FILE_SIZE:
            return {"error": f"Error: {file.filename} exceeds the maximum file size (5 MB). Please attach a smaller file..."}

        # We copy the file in our system so we can read it
        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR, exist_ok=True)
        temp_file_path = os.path.join(TEMP_DIR, file.filename)

        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"File saved temporarily in {temp_file_path}")

        # Store the file in the vectorstore
        indexing.add_file(temp_file_path)

        # Add the users prompt and file name to the db
        db.add_message(user_cookie, "user", prompt, file.filename)
    else:
        db.add_message(user_cookie, "user", prompt)
        
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
            agent_response = latest_message.content
            print("\nAgent: ", agent_response)
            # Add the agent response to the db, and update the prompts limit left 
            db.add_message(user_cookie, "agent", agent_response)
            db.decrement_requests(user_cookie)
            return {"message": agent_response}
    else:
        return {"error": "Error: Unexpected error. Please try again later..."}



# Endpoint to send the verification code to the user 
@router.post("/auth/request-code")
async def request_code(data: EmailRequest, user_cookie: str = Depends(get_set_user_cookie)):
    email = data.email.strip()
    # Generate the code 
    code = str(random.randint(100000, 999999))
    # Storate it temporarly in memory (we will change this to a database)
    codes[user_cookie] = {
        "email": email,
        "code": code 
    }
    try:
        # Finally send the verification code with the funcion defined in email_verification file
        success = send_email_verification(email, code)
    except Exception as e:
        send_telegram_alert(f"Error sending the email verification: {e}")
        return {"error": "Error sending the code. Please try again..."}

    if not success:
        return {"error": "Could not send the code verification email. Please check SMTP config"}
    return {"message": "Verification code successfully sent!"}
    

@router.post("/auth/verify-code")
async def verify_code(data: VerifyRequest, user_cookie: str = Depends(get_set_user_cookie)):
    # Get the user"s data 
    user_data = codes.get(user_cookie)
    if not user_data:
        return {"error": "There is no verification active request for this session."}
    if data.code.strip() != user_data["code"]:
        return {"error": "Invalid code. Please try again."}
    
    try:
        verified_email = user_data["email"]
        # Add the user_cookie to the database 
        db.save_verified_cookie(verified_email, user_cookie)
        del codes[user_cookie]
        # Send a message to the administrator
        message = f"{verified_email} verified successfully! Granted access!"
        send_telegram_alert(message)
        return {
            "success": True,
            "message": message
        }
    except Exception as e:
        send_telegram_alert(f"Verification code error: {e}")
        return {"error": "Unexpected error. Please try again later"}


@router.get("/chat/history")
async def get_chat_history(user_cookie: str = Depends(get_set_user_cookie)):
    # Endpoint to get the chat history from the database 
    if not db.is_cookie_verified(user_cookie):
        return {"messages": []}
    messages = db.get_messages(user_cookie)
    return {"messages": messages}



app.include_router(router)
