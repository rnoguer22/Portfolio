import os 
from dotenv import load_dotenv

# Fichero con constantes
# Cargamos las variables del fichero .env 
load_dotenv()

DIR_PATH = os.getenv('DIR_PATH')
CONTEXT_FILE_PATH = os.getenv('CONTEXT_FILE_PATH')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')
CHROMADB_PATH = os.getenv('CHROMADB_PATH')
K = 10
THRESHOLD = 0.5
OLLAMA_MODEL = 'qwen3'
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_MODEL = 'llama-3.1-8b-instant' # Durante el desarrollo, al ofrecer mas tokens y requests / dia
# GROQ_MODEL = 'llama-3.3-70b-versatile' # Cuando haya terminado el proyecto, ya se supone que es el que va mejor (gratuitamente con groq)
# GROQ_MODEL = 'qwen3.6-27b' # Alternativa al anterior, comparar las respuestas y ver cual funciona mejor. Si no, puede ser buena alternativa para tests 
HUGGINGFACE_EMBEDDINGS = 'sentence-transformers/all-mpnet-base-v2'
