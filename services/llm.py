import os

from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI


# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()


# ==========================================================
# GET MISTRAL API KEY
# ==========================================================

MISTRAL_API_KEY = os.getenv(
    "MISTRAL_API_KEY"
)


# ==========================================================
# VALIDATE API KEY
# ==========================================================

if not MISTRAL_API_KEY:

    raise RuntimeError(
        "MISTRAL_API_KEY is not set. "
        "Add MISTRAL_API_KEY to your .env file locally "
        "and to Render Environment Variables in production."
    )


# ==========================================================
# CREATE LLM
# ==========================================================

llm = ChatMistralAI(

    model="mistral-small-latest",

    temperature=0.7,

    api_key=MISTRAL_API_KEY,
)