from langchain_google_genai import ChatGoogleGenerativeAI
from settings import config
from typing import Any, List, Optional
from AI.config.logging_info import setup_logger

class GeminiChat:
    """
    A wrapper for ChatGoogleGenerativeAI with logging and error handling.
    
    This class provides:
    - Langfuse integration for observability
    - Proper error handling
    """
    
    def __init__(
        self,
        model: str = None,
        temperature: float = None,
        max_tokens: Optional[int] = None,
        timeout: Optional[int] = None,
        max_retries: int = None,
        google_api_key: str = None,
        custom_callbacks: List[Any] = None
    ):
        """
        Initialize the GeminiChat wrapper.
        
        Args:
            model: Model name to use (defaults to value in config)
            temperature: Temperature for generation (defaults to value in config)
            max_tokens: Maximum tokens to generate (defaults to value in config)
            timeout: Request timeout in seconds (defaults to value in config)
            max_retries: Maximum number of retries (defaults to value in config)
            google_api_key: Google API key (defaults to value in config)
            custom_callbacks: Additional callback handlers
        """
        # Initialize logger
        self.logger = setup_logger(__name__)
        self.logger.info("Initializing GeminiChat wrapper")
        
        # Use provided values or fall back to config
        self.model = model or config.model_name
        self.temperature = temperature if temperature is not None else config.temperature
        self.max_tokens = max_tokens if max_tokens is not None else config.max_tokens
        self.timeout = timeout if timeout is not None else config.timeout
        self.max_retries = max_retries if max_retries is not None else config.max_retries
        self.api_key = google_api_key or config.google_api_key
        
        # Set up callbacks
        self.callbacks = custom_callbacks or []
        if config.langfuse_handler:
            self.callbacks.append(config.langfuse_handler)
        
        # Validate essential parameters
        if not self.api_key:
            self.logger.error("Missing Google API key")
            raise ValueError("Google API key must be provided either directly or via config")
        
        self.logger.info(f"Using model: {self.model}, temperature: {self.temperature}")
        
        # Initialize LLM
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                timeout=self.timeout,
                max_retries=self.max_retries,
                google_api_key=self.api_key,
            )
            self.logger.info("LLM initialization successful")
        except Exception as e:
            self.logger.error(f"Failed to initialize LLM: {str(e)}")
            raise ValueError(f"Failed to initialize LLM: {str(e)}")
    
    def flush_langfuse(self):
        """Flush any pending Langfuse events."""
        if config.langfuse_handler:
            config.flush_langfuse()
            self.logger.info("Flushed Langfuse events")