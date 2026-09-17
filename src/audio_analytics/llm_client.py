import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(
    api_key=GEMINI_API_KEY,
)

model = "gemini-3-flash-preview"

generation_config = {
    'temperature': 1,
    'max_output_tokens': 1000,
    'top_p': 0.95,
    'thinking_level': 'low',
}

history = []

chat = client.chats.create(
    model=random.choice(models),
    history=history
)

while True:
    query = input(">>> ")
    if query.lower() == "/exit":
        print("Exiting...")
        break
    response = chat.send_message(query)
    history.append({"role": "user", "content": query})
    history.append({"role": "assistant", "content": response.text})
    print(response.text)

print(history)