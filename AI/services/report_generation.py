# LOCAL IMPORTS
from config.logging_info import setup_logger
from config.llm_setup import GeminiChat 
from models.report import LLMResponse

# Third Party
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# Setting up the logger file
logger = setup_logger(name=__name__)


# Class the handle the report generation process
class ChatService:
    """"Service for handling report generation
    TODO: ADD RAG using Pinecone
    """
    
    def __init__(self):
        """Initialize report generartion service with required dependencies"""
        try:
            # Initialize Gemini using default config settings
            logger.info("Initializing LLM service...")
            self.llm = GeminiChat()
            
            logger.info("Initializing AGENT (with memory)...")
            memory = MemorySaver()
            self.llm_graph = create_react_agent(
                model=self.llm.llm,  # Use the .llm property of GeminiChat
                response_format=LLMResponse,  # Changed parameter name to match LangGraph
                checkpointer=memory
            )
            
            # Initialize the pinecone db
            logger.info("Initializing vectorstore...")
            
        except Exception as e:
            logger.error(f"Error initializing chat service: {str(e)}")
            raise  # Re-raise to properly handle the error
            
    def process_chat(self, message, thread_id="default"):
        """Process a chat message through the LLM graph with memory
        
        Args:
            message (str): The user message to process
            thread_id (str): The thread ID for maintaining conversation context
            
        Returns:
            dict: Response from the LLM graph
        """
        try:
            # Create config with thread_id for memory persistence
            config = {"configurable": {"thread_id": thread_id}}
            
            # Create input format expected by the agent
            inputs = {"messages": [("user", message)]}
            
            # Process through graph
            logger.info(f"Processing message with thread_id: {thread_id}")
            response = self.llm_graph.invoke(inputs, config=config)
            
            return response
        except Exception as e:
            logger.error(f"Error processing chat: {str(e)}")
            return {"error": str(e)}
        
    def get_context_from_vectorstore(self, patient_data):
        """Optimized context retrieval using direct vectorstore search."""
        pass


# For testing the agent functionality
def main():
    """Test function to verify the LangGraph agent's functionality"""
    print("Initializing ChatService...")
    chat_service = ChatService()
    
    # First message
    thread_id = "test_thread_123"
    first_message = "What are the symptoms of diabetes?"
    print(f"\nUser: {first_message}")
    
    response = chat_service.process_chat(first_message, thread_id)
    print("\nAI Response:")
    print(response["messages"][-1][1])  # Assuming the response is in this format
    
    # Follow-up message to test memory
    follow_up = "What treatments are available for it?"
    print(f"\nUser: {follow_up}")
    
    response = chat_service.process_chat(follow_up, thread_id)
    print("\nAI Response (with memory context):")
    print(response["messages"][-1][1])  # Should reference diabetes without explicitly mentioning it
    
    
if __name__ == "__main__":
    main()
