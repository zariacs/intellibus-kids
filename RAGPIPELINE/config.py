import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Config")

# Load environment variables from .env file if it exists
loaded = load_dotenv()
if loaded:
    logger.info("Loaded environment variables from .env file")
else:
    logger.warning("No .env file found or unable to load environment variables")

# AstraDB configuration
ASTRA_DB_TOKEN = os.getenv("ASTRA_DB_TOKEN", "")
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT", "")
ASTRA_DB_NAMESPACE = os.getenv("ASTRA_DB_NAMESPACE", "default_namespace")
ASTRA_DB_COLLECTION = os.getenv("ASTRA_DB_COLLECTION", "document_collection")

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Document processing settings
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "2000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "300"))

# Download settings
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "RAGPIPELINE/downloads")

# Client ID for AstraDB
ASTRA_DB_CLIENT_ID = os.getenv("ASTRA_DB_CLIENT_ID", "")

# Log configuration values (without sensitive information)
logger.info(f"AstraDB API Endpoint configured: {'Yes' if ASTRA_DB_API_ENDPOINT else 'No'}")
logger.info(f"AstraDB Token configured: {'Yes' if ASTRA_DB_TOKEN else 'No'}")
logger.info(f"AstraDB Client ID configured: {'Yes' if ASTRA_DB_CLIENT_ID else 'No'}")
logger.info(f"AstraDB Namespace: {ASTRA_DB_NAMESPACE}")
logger.info(f"AstraDB Collection: {ASTRA_DB_COLLECTION}")
logger.info(f"OpenAI API Key configured: {'Yes' if OPENAI_API_KEY else 'No'}")
logger.info(f"Chunk Size: {CHUNK_SIZE}")
logger.info(f"Chunk Overlap: {CHUNK_OVERLAP}")
logger.info(f"Download Directory: {DOWNLOAD_DIR}")

# Verify critical configuration
if not ASTRA_DB_TOKEN:
    logger.error("ASTRA_DB_TOKEN is not set. Please set it in your .env file.")

if not ASTRA_DB_API_ENDPOINT:
    logger.error("ASTRA_DB_API_ENDPOINT is not set. Please set it in your .env file.")

if not OPENAI_API_KEY:
    logger.warning("OPENAI_API_KEY is not set. Embeddings will fail without this.")
