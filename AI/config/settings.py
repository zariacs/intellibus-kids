import os
from typing import Dict, List, Optional, Union, Any
from dotenv import load_dotenv
from pathlib import Path
from langfuse.callback import CallbackHandler


class Config:
    """
    Configuration manager for application settings.
    Implements singleton pattern to ensure only one config instance exists.
    """
    _instance = None
    
    def __new__(cls, env_file: Optional[Union[str, Path]] = None):
        """
        Create a new Config instance if one doesn't exist yet.
        
        Args:
            env_file: Optional path to .env file
        """
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, env_file: Optional[Union[str, Path]] = None):
        """
        Initialize configuration by loading environment variables.
        
        Args:
            env_file: Optional path to .env file
        """
        if self._initialized:
            return
            
        # Load environment variables
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()
            
        # API Keys
        self._gemini_api_key = os.getenv("GEMINI_API_KEY")
        self._pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self._langfuse_public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
        self._langfuse_secret_key = os.getenv("LANGFUSE_SECRET_KEY")
        
        # LLM Configuration
        self._model_name = "gemini-1.5-pro"
        self._temperature = 0.5
        self._max_tokens = None
        self._timeout = None
        self._max_retries = 2
        
        # Pinecone Configuration
        self._pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
        self._pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", "intellibus-kids-index")
        
        # Debug settings
        self._debug = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
        self._log_level = os.getenv("LOG_LEVEL", "INFO")
        
        # System Prompts
        self._default_system_prompt = """
        You are an AI model for the platform called NutriLab.
        Your goal is to provide detailed responses that are:
        - Useful for persons who are suffering from IBS

        Always explain concepts in simple terms and use examples where appropriate.
        """
        
        # API Configuration
        self._cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
        self._api_rate_limit = int(os.getenv("API_RATE_LIMIT", "100"))  # Requests per minute
        
        # Initialize Langfuse handler if keys are available
        self._langfuse_handler = None
        if self._langfuse_public_key and self._langfuse_secret_key:
            try:
                self._langfuse_handler = CallbackHandler(
                    public_key=self._langfuse_public_key,
                    secret_key=self._langfuse_secret_key
                )
            except Exception as e:
                print(f"Failed to initialize Langfuse handler: {str(e)}")
        
        self._initialized = True
    
    # API Keys properties
    @property
    def google_api_key(self) -> Optional[str]:
        """Get Google API key."""
        return self._gemini_api_key
    
    @property
    def pinecone_api_key(self) -> Optional[str]:
        """Get Pinecone API key."""
        return self._pinecone_api_key
    
    @property
    def langfuse_public_key(self) -> Optional[str]:
        """Get Langfuse public key."""
        return self._langfuse_public_key
    
    @property
    def langfuse_secret_key(self) -> Optional[str]:
        """Get Langfuse secret key."""
        return self._langfuse_secret_key
    
    # LLM Configuration properties
    @property
    def model_name(self) -> str:
        """Get LLM model name."""
        return self._model_name
    
    @model_name.setter
    def model_name(self, value: str) -> None:
        """Set LLM model name."""
        self._model_name = value
    
    @property
    def temperature(self) -> float:
        """Get LLM temperature."""
        return self._temperature
    
    @temperature.setter
    def temperature(self, value: float) -> None:
        """Set LLM temperature."""
        if not 0 <= value <= 1:
            raise ValueError("Temperature must be between 0 and 1")
        self._temperature = value
    
    @property
    def max_tokens(self) -> Optional[int]:
        """Get max tokens."""
        return self._max_tokens
    
    @max_tokens.setter
    def max_tokens(self, value: Optional[int]) -> None:
        """Set max tokens."""
        if value is not None and value <= 0:
            raise ValueError("Max tokens must be greater than 0")
        self._max_tokens = value
    
    @property
    def timeout(self) -> Optional[int]:
        """Get timeout in seconds."""
        return self._timeout
    
    @timeout.setter
    def timeout(self, value: Optional[int]) -> None:
        """Set timeout in seconds."""
        self._timeout = value
    
    @property
    def max_retries(self) -> int:
        """Get maximum number of retries."""
        return self._max_retries
    
    @max_retries.setter
    def max_retries(self, value: int) -> None:
        """Set maximum number of retries."""
        if value < 0:
            raise ValueError("Max retries must be non-negative")
        self._max_retries = value
    
    # Pinecone Configuration properties
    @property
    def pinecone_environment(self) -> Optional[str]:
        """Get Pinecone environment."""
        return self._pinecone_environment
    
    @property
    def pinecone_index_name(self) -> str:
        """Get Pinecone index name."""
        return self._pinecone_index_name
    
    # Debug settings properties
    @property
    def debug(self) -> bool:
        """Get debug mode."""
        return self._debug
    
    @debug.setter
    def debug(self, value: bool) -> None:
        """Set debug mode."""
        self._debug = value
    
    @property
    def log_level(self) -> str:
        """Get log level."""
        return self._log_level
    
    @log_level.setter
    def log_level(self, value: str) -> None:
        """Set log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if value not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        self._log_level = value
    
    # System Prompts properties
    @property
    def default_system_prompt(self) -> str:
        """Get default system prompt."""
        return self._default_system_prompt
    
    @default_system_prompt.setter
    def default_system_prompt(self, value: str) -> None:
        """Set default system prompt."""
        self._default_system_prompt = value
    
    # API Configuration properties
    @property
    def cors_origins(self) -> List[str]:
        """Get CORS origins."""
        return self._cors_origins
    
    @property
    def api_rate_limit(self) -> int:
        """Get API rate limit."""
        return self._api_rate_limit
    
    # Add Langfuse handler property
    @property
    def langfuse_handler(self):
        """Get Langfuse callback handler."""
        return self._langfuse_handler
    
    def flush_langfuse(self):
        """Flush Langfuse events."""
        if self._langfuse_handler:
            self._langfuse_handler.flush()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        Useful for serialization.
        
        Returns:
            Dict containing all configuration values
        """
        return {
            "google_api_key": self._gemini_api_key,
            "pinecone_api_key": self._pinecone_api_key,
            "langfuse_public_key": self._langfuse_public_key,
            "langfuse_secret_key": self._langfuse_secret_key,
            "model_name": self._model_name,
            "temperature": self._temperature,
            "max_tokens": self._max_tokens,
            "timeout": self._timeout,
            "max_retries": self._max_retries,
            "pinecone_environment": self._pinecone_environment,
            "pinecone_index_name": self._pinecone_index_name,
            "debug": self._debug,
            "log_level": self._log_level,
            "cors_origins": self._cors_origins,
            "api_rate_limit": self._api_rate_limit
        }
    
    def validate(self) -> List[str]:
        """
        Validate the configuration and return any issues found.
        
        Returns:
            List of validation error messages (empty if no issues)
        """
        errors = []
        
        # Check required API keys
        if not self._gemini_api_key:
            errors.append("GEMINI_API_KEY is not set")
        
        if not self._pinecone_api_key:
            errors.append("PINECONE_API_KEY is not set")
            
        if not self._pinecone_environment:
            errors.append("PINECONE_ENVIRONMENT is not set")
            
        return errors


# Create a default instance for easy importing
config = Config() 