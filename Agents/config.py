import os 
from dotenv import load_dotenv

# Fichero con constantes
# Cargamos las variables del fichero .env 
load_dotenv()

OLLAMA_MODEL = 'qwen3'
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# Para IA agentica, usamos uno de los modelos de OpenAI, ya que no da errores de formato al llamar a las tools, que me pasaba con los modelos de llama 
# Ademas, llama-3.1-8b-instant y llama-3.3-70b-versatile estan deprecated, y se recomienda cambiarlos por 'openai/gpt-oss-20b' y 'openai/gpt-oss-120b' respectivamente
# GROQ_MODEL = 'openai/gpt-oss-20b'
# GROQ_MODEL = 'openai/gpt-oss-120b'
# GROQ_MODEL = 'qwen/qwen3.6-27b'
GROQ_MODEL = 'llama-3.3-70b-versatile'
GOOGLE_MODEL = 'gemini-3.5-flash' 
OPENAI_MODEL = 'gpt-5-nano'
# OPENAI_MODEL = 'gpt-4o-mini'
