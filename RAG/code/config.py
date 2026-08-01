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
HUGGINGFACE_EMBEDDINGS = 'sentence-transformers/all-mpnet-base-v2'
