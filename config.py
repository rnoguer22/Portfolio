import os
from pathlib import Path 
from dotenv import load_dotenv

# Fichero con constantes
# Cargamos las variables del fichero .env 
load_dotenv()

DIR_PATH = Path(__file__).resolve().parent
GRAPH_PATH = os.path.join(DIR_PATH, os.getenv("GRAPH_PATH"))
COLLECTION_NAME = os.path.join(DIR_PATH, os.getenv("COLLECTION_NAME"))
CHROMADB_PATH = os.path.join(DIR_PATH, os.getenv("CHROMADB_PATH"))
TEMP_DIR = os.path.join(DIR_PATH, os.getenv("TEMP_DIR"))

K = 10
THRESHOLD = 0.5
OLLAMA_MODEL = "qwen3"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GROQ_MODEL = "qwen3.6-27b" 

GOOGLE_MODEL = "gemini-3.5-flash" 
OPENAI_MODEL = "gpt-5-nano"
HUGGINGFACE_EMBEDDINGS = "sentence-transformers/all-mpnet-base-v2"

# GROQ_MODEL = "openai/gpt-oss-20b"
# GROQ_MODEL = "openai/gpt-oss-120b"
# GROQ_MODEL = "qwen/qwen3.6-27b"
# OPENAI_MODEL = "gpt-4o-mini"


# EMAIL = "rnoguer.portfolio@gmail.com"
RESEND_EMAIL = "noreply@rnoguer.com"
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

DB_PATH = os.path.join(DIR_PATH, os.getenv("DB_PATH"))
SQLITE_FILE_PATH = os.path.join(DIR_PATH, os.getenv("SQLITE_FILE_PATH"))

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
