import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")

# LLM Configuration
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))

# Pinecone Configuration
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "intellibus-kids-index")

# Debug settings
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# System Prompts
DEFAULT_SYSTEM_PROMPT = """
You are an AI teaching assistant for the Intellibus Kids platform. 
Your goal is to provide educational responses that are:
1. Age-appropriate for elementary school children
2. Accurate and educational
3. Engaging and easy to understand
4. Safe and appropriate for children

Always explain concepts in simple terms and use examples where appropriate.
"""

# API Configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
API_RATE_LIMIT = int(os.getenv("API_RATE_LIMIT", "100"))  # Requests per minute 