import os 
from dotenv import load_dotenv

# Fichero con constantes
# Cargamos las variables del fichero .env 
load_dotenv()

DIR_PATH = os.getenv('DIR_PATH')
GRAPH_PATH = os.getenv('GRAPH_PATH')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')
CHROMADB_PATH = os.getenv('CHROMADB_PATH')
TEMP_DIR = os.getenv('TEMP_DIR')

K = 10
THRESHOLD = 0.5
OLLAMA_MODEL = 'qwen3'
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
GROQ_MODEL = 'qwen3.6-27b' 

GOOGLE_MODEL = 'gemini-3.5-flash' 
OPENAI_MODEL = 'gpt-5-nano'
HUGGINGFACE_EMBEDDINGS = 'sentence-transformers/all-mpnet-base-v2'

# GROQ_MODEL = 'openai/gpt-oss-20b'
# GROQ_MODEL = 'openai/gpt-oss-120b'
# GROQ_MODEL = 'qwen/qwen3.6-27b'
# OPENAI_MODEL = 'gpt-4o-mini'



EMAIL = "rnoguer.portfolio@gmail.com"
EMAIL_PASSWD = os.getenv('EMAIL_PASSWD')
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SQLITE_FILE_PATH = os.getenv("SQLITE_FILE_PATH")
