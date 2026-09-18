from audio_analytics.config import settings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama


ollama_model = ChatOllama(
            model=settings.model,
            temperature=settings.temperature,
            max_tokens=settings.max_output_tokens
        )

google_model = ChatGoogleGenerativeAI(
    model="",
    max_tokens=max_output_tokens
)

response = model.invoke("Hi! How are you?")
print(response.content)