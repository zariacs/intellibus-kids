from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import config
from typing import Any, List, Optional, Union, Tuple
from config.logging_info import setup_logger
from langchain_openai import ChatOpenAI as LangchainChatOpenAI
import time


class OpenAIChat:
    """
    Industry-grade wrapper for OpenAI's chat models with robust error handling and observability.
    
    Features:
    - Langfuse integration for tracking and monitoring
    - Comprehensive error handling with retries
    - Support for tool calling
    - Performance optimization
    """
    
    # Models that don't support temperature parameter
    NO_TEMPERATURE_MODELS = ["o3-mini-2025-01-31"]
    
    def __init__(
        self,
        model: str = None,
        temperature: float = None,
        max_tokens: Optional[int] = None,
        timeout: Optional[Union[float, Tuple[float, float]]] = None,
        max_retries: int = None,
        openai_api_key: str = None,
        custom_callbacks: List[Any] = None,
        streaming: bool = False,
        verbose: bool = False
    ):
        """
        Initialize the OpenAIChat wrapper with configuration.
        
        Args:
            model: Model name to use (defaults to value in config)
            temperature: Temperature for generation (defaults to value in config)
            max_tokens: Maximum tokens to generate (defaults to value in config)
            timeout: Request timeout in seconds (defaults to value in config)
            max_retries: Maximum number of retries (defaults to value in config)
            openai_api_key: OpenAI API key (defaults to value in config)
            custom_callbacks: Additional callback handlers
            streaming: Whether to enable streaming responses
            verbose: Whether to enable verbose logging
        """
        # Initialize logger
        self.logger = setup_logger(__name__)
        self.logger.info("Initializing OpenAIChat wrapper")
        
        # Use provided values or fall back to config
        self.model = model or config.model_name
        self.temperature = temperature if temperature is not None else config.temperature
        self.max_tokens = max_tokens if max_tokens is not None else config.max_tokens
        self.timeout = timeout if timeout is not None else config.timeout
        self.max_retries = max_retries if max_retries is not None else config.max_retries
        self.openai_api_key = openai_api_key or config.openai_api_key
        self.streaming = streaming
        self.verbose = verbose
        
        # Set up callbacks with Langfuse integration
        self.callbacks = custom_callbacks or ([config.langfuse_handler] if config.langfuse_handler else [])
        
        # Validate essential parameters
        if not self.openai_api_key:
            self.logger.error("Missing OpenAI API key")
            raise ValueError("OpenAI API key must be provided either directly or via config")
        
        self.logger.info(f"Using model: {self.model}, temperature: {self.temperature}")
        
        # Initialize LLM with error handling
        try:
            # Create kwargs dict to handle model-specific parameters
            llm_kwargs = {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "timeout": self.timeout,
                "max_retries": self.max_retries,
                "openai_api_key": self.openai_api_key,
                "streaming": self.streaming,
                "verbose": self.verbose,
                "callbacks": self.callbacks
            }
            
            # Only add temperature if the model supports it
            if self.model not in self.NO_TEMPERATURE_MODELS:
                llm_kwargs["temperature"] = self.temperature
            else:
                self.logger.info(f"Model {self.model} doesn't support temperature parameter, skipping")
            
            self.llm = LangchainChatOpenAI(**llm_kwargs)
            self.logger.info("OpenAI LLM initialization successful")
        except Exception as e:
            self.logger.error(f"Failed to initialize OpenAI LLM: {str(e)}")
            raise ValueError(f"Failed to initialize OpenAI LLM: {str(e)}")
    
    def invoke(self, messages, **kwargs):
        """
        Invoke the OpenAI chat model with robust error handling and performance tracking.
        
        Args:
            messages: List of messages to send to the model
            **kwargs: Additional parameters to pass to the model
            
        Returns:
            The model's response
        """
        start_time = time.time()
        retry_count = 0
        max_retries = kwargs.pop('max_retries', self.max_retries)
        
        # Remove temperature parameter if model doesn't support it
        if self.model in self.NO_TEMPERATURE_MODELS and 'temperature' in kwargs:
            self.logger.info(f"Removing unsupported temperature parameter for model {self.model}")
            kwargs.pop('temperature')
        
        while retry_count <= max_retries:
            try:
                self.logger.info(f"Invoking OpenAI model: {self.model}")
                response = self.llm.invoke(messages, **kwargs)
                
                # Log performance metrics
                elapsed_time = time.time() - start_time
                self.logger.info(f"OpenAI response received in {elapsed_time:.2f}s")
                
                # Check if response time exceeds threshold (10s)
                if elapsed_time > 10:
                    self.logger.warning(f"Response time exceeded threshold: {elapsed_time:.2f}s")
                
                return response
                
            except Exception as e:
                retry_count += 1
                self.logger.warning(f"Error invoking OpenAI (attempt {retry_count}/{max_retries+1}): {str(e)}")
                
                # If we've exhausted retries, raise the exception
                if retry_count > max_retries:
                    self.logger.error(f"Failed to get response after {max_retries+1} attempts: {str(e)}")
                    raise
                
                # Exponential backoff with jitter
                backoff_time = min(2 ** retry_count + (0.1 * retry_count), 60)
                self.logger.info(f"Retrying in {backoff_time:.2f}s...")
                time.sleep(backoff_time)
    
    def bind_tools(self, tools, **kwargs):
        """
        Bind tools to the OpenAI model for function/tool calling.
        
        Args:
            tools: List of tools to bind to the model
            **kwargs: Additional parameters for tool binding
            
        Returns:
            A new instance of the model with tools bound
        """
        try:
            self.logger.info(f"Binding {len(tools)} tools to OpenAI model")
            
            # Remove temperature parameter if model doesn't support it
            if self.model in self.NO_TEMPERATURE_MODELS and 'temperature' in kwargs:
                self.logger.info(f"Removing unsupported temperature parameter for model {self.model}")
                kwargs.pop('temperature')
                
            return self.llm.bind_tools(tools, **kwargs)
        except Exception as e:
            self.logger.error(f"Failed to bind tools to OpenAI model: {str(e)}")
            raise ValueError(f"Failed to bind tools to OpenAI model: {str(e)}")
    
    def get_num_tokens(self, text):
        """
        Get the number of tokens in a text string.
        
        Args:
            text: The text to tokenize
            
        Returns:
            The number of tokens in the text
        """
        try:
            return self.llm.get_num_tokens(text)
        except Exception as e:
            self.logger.error(f"Failed to get token count: {str(e)}")
            # Fallback to approximate token count (1 token ≈ 4 chars)
            return len(text) // 4
    
    def get_num_tokens_from_messages(self, messages):
        """
        Get the number of tokens in a list of messages.
        
        Args:
            messages: The messages to tokenize
            
        Returns:
            The number of tokens in the messages
        """
        try:
            return self.llm.get_num_tokens_from_messages(messages)
        except Exception as e:
            self.logger.error(f"Failed to get token count from messages: {str(e)}")
            
            # More sophisticated fallback for token counting
            # For models that don't support get_num_tokens_from_messages
            total_text = ""
            for message in messages:
                if hasattr(message, "content"):
                    # Add role prefix to better approximate token count
                    role = getattr(message, "type", "unknown")
                    total_text += f"{role}: {message.content}\n\n"
            
            # Estimate: 1 token ≈ 4 characters for English text
            estimated_tokens = len(total_text) // 4
            self.logger.info(f"Estimated token count using fallback method: {estimated_tokens}")
            return estimated_tokens
    
    def flush_langfuse(self):
        """Flush any pending Langfuse events."""
        if config.langfuse_handler:
            config.flush_langfuse()
            self.logger.info("Flushed Langfuse events")


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
        Initialize the GeminiChat wrapper with/without config default values.
        
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
        self.google_api_key = google_api_key or config.google_api_key
        
        # Set up callbacks
        self.callbacks = custom_callbacks or ([config.langfuse_handler] if config.langfuse_handler else [])
        
        # Validate essential parameters
        if not self.google_api_key:
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
                google_api_key=self.google_api_key,
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