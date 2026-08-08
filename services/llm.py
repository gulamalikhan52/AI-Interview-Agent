from dotenv import load_dotenv
import os

from langchain_mistralai import ChatMistralAI

load_dotenv()

llm = ChatMistralAI(
    model="mistral-small-latest",
    temperature=0.2,
    api_key=os.getenv("MISTRAL_API_KEY"),
)