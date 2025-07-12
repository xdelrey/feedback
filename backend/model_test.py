import os
from groq import Groq
from dotenv import load_dotenv

# cargamos el .env
load_dotenv()

# leemos la variable 
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# probando que funciona correctamente
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "no me ha gustado nada esta aplicación",
        }
    ],
    model="llama-3.3-70b-versatile",
    stream=False,
)

print(chat_completion.choices[0].message.content)