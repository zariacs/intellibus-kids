# LOCAL IMPORTS
from config.logging_info import setup_logger
from config.llm_setup import GeminiChat 
from models.report import LLMResponse

# Third Party
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
import json

# Setting up the logger file
logger = setup_logger(name=__name__)

# Define tools as standalone functions outside the class
@tool
def get_context_from_vectorstore(patient_data: str) -> str:
    """Optimized context retrieval using direct vectorstore search."""
    logger.info(f"Retrieving context for patient data: {patient_data}")
    return "Diabetes is a chronic metabolic disorder characterized by elevated blood sugar levels over a prolonged period. There are several types including Type 1, Type 2, and gestational diabetes. Symptoms include increased thirst, frequent urination, hunger, fatigue, and blurred vision."


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
            
            # Define the tools list with our standalone function
            tools = [get_context_from_vectorstore]
            
            # Initialize the vectorstore db
            logger.info("Initializing vectorstore...")
            
            # Create the agent after tools are defined
            logger.info("Initializing AGENT (with memory)...")
            memory = MemorySaver()
            self.llm_graph = create_react_agent(
                model=self.llm.llm,  # Use the .llm property of GeminiChat
                response_format=LLMResponse,  # Changed parameter name to match LangGraph
                checkpointer=memory,
                tools=tools
            )
            
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
            
            # Create proper HumanMessage object instead of tuple
            user_message = HumanMessage(content=message)
            
            # System message to provide context
            system_message = SystemMessage(content="""You are an AI healthcare assistant focused on providing 
            accurate and helpful information about medical conditions. When responding to queries about specific 
            medical conditions, use information from your tools when available.""")
            
            # Log the input message
            logger.info(f"Input message: {message}")
            logger.info(f"Input message type: {type(message)}")
            
            # Create input format expected by the agent - including system message
            # Check if we already have messages in memory by examining the checkpointer
            try:
                # To check if this is the first message
                checkpoint = self.llm_graph.checkpointer.get(thread_id)
                if checkpoint and 'messages' in checkpoint and len(checkpoint['messages']) > 0:
                    # This is a follow-up message, so just add the new human message
                    logger.info(f"Found existing messages for thread {thread_id}, appending user message")
                    inputs = {"messages": [user_message]}
                else:
                    # First message, include the system message
                    logger.info(f"No existing messages found for thread {thread_id}, adding system message")
                    inputs = {"messages": [system_message, user_message]}
            except Exception as checkpoint_error:
                # If any error occurs, default to including system message
                logger.warning(f"Error checking checkpoint: {str(checkpoint_error)}, defaulting to including system message")
                inputs = {"messages": [system_message, user_message]}
            
            # Log the inputs for debugging
            logger.info(f"Input structure: {inputs}")
            
            # Process through graph
            logger.info(f"Processing message with thread_id: {thread_id}")
            response = self.llm_graph.invoke(inputs, config=config)
            
            # Log the response structure for debugging
            logger.info(f"Response keys: {response.keys()}")
            if 'messages' in response:
                msg_types = [type(msg).__name__ for msg in response['messages']]
                logger.info(f"Message types in response: {msg_types}")
                for i, msg in enumerate(response['messages']):
                    if hasattr(msg, 'content'):
                        content_preview = str(msg.content)[:100] + "..." if len(str(msg.content)) > 100 else str(msg.content)
                        logger.info(f"Message {i} content: {content_preview}")
            
            return response
        except Exception as e:
            logger.error(f"Error processing chat: {str(e)}")
            return {"error": str(e)}

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
    
    # Handle response format correctly
    if "error" in response:
        print(f"Error: {response['error']}")
    else:
        # Print the structured response if available
        if 'structured_response' in response:
            result = response['structured_response']
            print(f"Structured Response:")
            if hasattr(result, 'meal_plan') and result.meal_plan:
                print(f"Meal Plan: {result.meal_plan}")
            if hasattr(result, 'ingredients') and result.ingredients:
                print(f"Ingredients: {result.ingredients}")
            if hasattr(result, 'patient_details') and result.patient_details:
                print(f"Patient Details: {result.patient_details}")
        
        # Print the raw message content from AI
        if 'messages' in response:
            for msg in response['messages']:
                from langchain_core.messages import AIMessage
                if isinstance(msg, AIMessage):
                    print(f"AI: {msg.content}")
    
    # Follow-up message to test memory
    follow_up = "What treatments are available for it?"
    print(f"\nUser: {follow_up}")
    
    response = chat_service.process_chat(follow_up, thread_id)
    print("\nAI Response (with memory context):")
    
    # Handle response the same way
    if "error" in response:
        print(f"Error: {response['error']}")
    else:
        # Print the structured response if available
        if 'structured_response' in response:
            result = response['structured_response']
            print(f"Structured Response:")
            if hasattr(result, 'meal_plan') and result.meal_plan:
                print(f"Meal Plan: {result.meal_plan}")
            if hasattr(result, 'ingredients') and result.ingredients:
                print(f"Ingredients: {result.ingredients}")
            if hasattr(result, 'patient_details') and result.patient_details:
                print(f"Patient Details: {result.patient_details}")
        
        # Print the raw message content from AI
        if 'messages' in response:
            for msg in response['messages']:
                from langchain_core.messages import AIMessage
                if isinstance(msg, AIMessage):
                    print(f"AI: {msg.content}")
                    
if __name__ == "__main__":
    main()
