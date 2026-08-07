import os 
from dotenv import load_dotenv

# Fichero con constantes
# Cargamos las variables del fichero .env 
load_dotenv()

OLLAMA_MODEL = 'qwen3'
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
GROQ_MODEL = 'llama-3.1-8b-instant' # Durante el desarrollo, al ofrecer mas tokens y requests / dia
# GROQ_MODEL = 'llama-3.3-70b-versatile' # Cuando haya terminado el proyecto, ya se supone que es el que va mejor (gratuitamente con groq)
# GROQ_MODEL = 'qwen3.6-27b' # Alternativa al anterior, comparar las respuestas y ver cual funciona mejor. Si no, puede ser buena alternativa para tests 
