from dotenv import load_dotenv
import os
from groq import Groq, APIError

# cargamos el .env
load_dotenv()

# leemos la api key de groq y resto de variables
API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL_NAME", "mixtral-8x7b-32768") # si no existe, 'mixtral'

client = Groq(api_key=API_KEY)

# system prompt
SYSTEM_MSG = (
    "Eres un asistente de atención al usuario de la app móvil de Spotify."
    "Responde en un tono amable, empático y en un máximo de 3 frases. Siempre agradece."
    "Si procede y sólo si tienes claro cuál es la solución al problema expuesto por el usuario, propón una acción o solución."
    "Nunca ofrezcas continuar la conversación. El usuario no esperará nunca más que una respuesta final por tu parte."
    "Responde para finalizar que harás llegar el feedback proporcionado por el usuario al departamento que corresponda."
)

def responder_llm(texto: str) -> str:
    """Envía el feedback del usuario a Groq y devuelve la respuesta del LLM en texto plano."""
    
    mensajes = [
        {"role": "system", "content": SYSTEM_MSG},
        {"role": "user", "content": texto}
    ]

    try:
        respuesta = client.chat.completions.create(
            model=MODEL,
            messages=mensajes,
            max_completion_tokens=200,
        )
        return respuesta.choices[0].message.content.strip()
    
    # manejo de errores
    except APIError as e:
        raise RuntimeError(f"Groq APIError: {e}") from e # errores de API
    except Exception as e:
        raise RuntimeError(f"Eeror al llamar a Groq: {e}") from e # red caída, json mal formado, timeout, etc.
    
