import os
from groq import Groq
from dotenv import load_dotenv

# cargamos el .env
load_dotenv()

system_prompt = (
    "Eres un asistente de atención al usuario de la app móvil de Spotify."
    "Responde en un tono amable, empático y en un máximo de 3 frases. Siempre agradece."
    "Si procede y sólo si tienes claro cuál es la solución al problema expuesto por el usuario, propón una acción o solución."
    "Nunca ofrezcas continuar la conversación. El usuario no esperará nunca más que una respuesta final por tu parte."
    "Responde para finalizar que harás llegar el feedback proporcionado por el usuario al departamento que corresponda."
)

user_prompt = (
    "jajajjaj ... me ha encantado el wrapped!"
)

# leemos la variable 
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# probando que funciona correctamente
chat_completion = client.chat.completions.create(
    # probar diferentes prompts
    messages=[
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ],
    
    # probar diferentes modelos
    model="llama-3.3-70b-versatile",

    stream=False,
)

print(chat_completion.choices[0].message.content)