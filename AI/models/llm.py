from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from AI.config.settings import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE, MAX_TOKENS, DEFAULT_SYSTEM_PROMPT
from typing import List, Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMModel:
    """
    Class that handles integration with the Large Language Model.
    """
    
    def __init__(self):
        """
        Initialize the LLM model with configuration from settings.
        """
        if not OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY not found in environment variables.")
        
        # Initialize the ChatOpenAI model
        self.llm = ChatOpenAI(
            model_name=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            openai_api_key=OPENAI_API_KEY
        )
        
        # Default system prompt
        self.system_prompt = DEFAULT_SYSTEM_PROMPT
    
    def generate_response(self, query: str, context: Optional[str] = None, custom_system_prompt: Optional[str] = None) -> str:
        """
        Generate a response using the LLM based on the query and optional context.
        
        Args:
            query: The user's query or question
            context: Optional context from RAG retrieval to help guide the response
            custom_system_prompt: Optional custom system prompt to override the default
            
        Returns:
            The generated response as a string
        """