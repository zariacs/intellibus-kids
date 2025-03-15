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
MODEL_NAME = "gpt-4-turbo-preview"
TEMPERATURE = 0.5
MAX_TOKENS = 20_000

# Pinecone Configuration
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "intellibus-kids-index")

# Debug settings
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# System Prompts
DEFAULT_SYSTEM_PROMPT = """
You are an AI model for the platform called NutriLab.
Your goal is to provide detailed responses that are:
- Useful for persons who are suffering from IBS

Always explain concepts in simple terms and use examples where appropriate.
"""

# API Configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
API_RATE_LIMIT = int(os.getenv("API_RATE_LIMIT", "100"))  # Requests per minute 