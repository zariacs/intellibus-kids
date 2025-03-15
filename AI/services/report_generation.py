# LOCAL IMPORTS
from config.logging_info import setup_logger
from AI.config.llm_setup import GeminiChat 

# Setting up the logger file
logger = setup_logger(name=__name__)


# Class the handle the report generation process
class ChatService:
    """"Service for handling report generation
    TODO: ADD RAG 
    """
    
    def __init__(self):
        """Initialize report generartion service with required dependencies"""
        try:
            # Initializing Gemini
            logger.info("Initializing LLM service...")
            self.llm = GeminiChat()  # Initialize Gemini using default config settings
            
            # TODO: Initialize the pinecone db
            logger.info("Initializing vectorstore...")
            
            
            
        except Exception as e:
                logger.error(f"Error extracting filters: {str(e)}")
                return {}