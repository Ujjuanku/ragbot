import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI Config
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-3.5-turbo"

# Pinecone Config
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "acme-rag")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in environment variables")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is not set in environment variables")
