# LOCAL IMPORTS
from config.logging_info import setup_logger
from config.llm_setup import GeminiChat 
from models.report import LLMResponse
from config.settings import config

# Third Party
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
import json
import time
from typing import Dict, Any, List, Optional

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
            config_params = {"configurable": {"thread_id": thread_id}}
            
            # Create proper HumanMessage object instead of tuple
            user_message = HumanMessage(content=message)
            
            # System message using default from settings
            system_message = SystemMessage(content=config.default_system_prompt)
            
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
            response = self.llm_graph.invoke(inputs, config=config_params)
            
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
        
    def process_patient_data(self, patient_data: Dict[str, Any], thread_id: Optional[str] = None) -> Dict[str, Any]:
        """Process patient data to generate a comprehensive medical report
        
        Args:
            patient_data (dict): Dictionary containing patient information including:
                - name: Patient's name (required)
                - age: Patient's age (optional)
                - gender: Patient's gender (optional)
                - weight: Patient's weight in kg (optional)
                - height: Patient's height in cm (optional)
                - condition: Medical condition (required)
                - allergies: List of allergies (optional)
                - medications: Current medications (optional)
                - symptoms: Current symptoms (optional)
                - dietary_preferences: Any dietary preferences (optional)
            thread_id (str, optional): Unique identifier for the conversation
                
        Returns:
            dict: Response containing structured medical report
        """
        # Validate essential fields
        if not patient_data.get('name'):
            logger.error("Missing required field: 'name'")
            return {"error": "Missing required field: 'name'"}
        
        if not patient_data.get('condition'):
            logger.error("Missing required field: 'condition'")
            return {"error": "Missing required field: 'condition'"}
        
        # Generate thread_id if not provided
        if thread_id is None:
            thread_id = f"patient_{patient_data.get('name', 'unknown').lower().replace(' ', '_')}_{int(time.time())}"
        
        try:
            # Create config with thread_id for memory persistence
            config_params = {"configurable": {"thread_id": thread_id}}
            
            # Format allergies list or use default
            allergies = patient_data.get('allergies', [])
            if not allergies:
                allergies_text = "None reported"
            elif isinstance(allergies, list):
                allergies_text = ", ".join(allergies)
            else:
                allergies_text = str(allergies)
            
            # Additional patient information formatting
            age = f"{patient_data.get('age', 'Not provided')} years" if patient_data.get('age') else 'Not provided'
            gender = patient_data.get('gender', 'Not provided')
            weight = f"{patient_data.get('weight', 'Not provided')} kg" if patient_data.get('weight') else 'Not provided'
            height = f"{patient_data.get('height', 'Not provided')} cm" if patient_data.get('height') else 'Not provided'
            medications = patient_data.get('medications', 'None reported')
            if isinstance(medications, list):
                medications = ", ".join(medications)
                
            symptoms = patient_data.get('symptoms', 'None reported')
            if isinstance(symptoms, list):
                symptoms = ", ".join(symptoms)
                
            dietary_prefs = patient_data.get('dietary_preferences', 'None reported')
            if isinstance(dietary_prefs, list):
                dietary_prefs = ", ".join(dietary_prefs)
            
            # Construct a prompt that will generate the desired report format
            prompt = f"""
            Generate a comprehensive medical report for this patient:
            
            Patient information:
            - Name: {patient_data.get('name')}
            - Age: {age}
            - Gender: {gender}
            - Weight: {weight}
            - Height: {height}
            - Condition: {patient_data.get('condition')}
            - Allergies: {allergies_text}
            - Current Medications: {medications}
            - Symptoms: {symptoms}
            - Dietary Preferences: {dietary_prefs}
            
            Please format the report in markdown exactly as follows:
            
            # Medical Report for {patient_data.get('name')}
            
            ## Patient Details
            - Name: {patient_data.get('name')}
            - Age: {age}
            - Gender: {gender}
            - Weight: {weight}
            - Height: {height}
            - Condition: {patient_data.get('condition')}
            - Allergies: {allergies_text}
            
            ## Definition of {patient_data.get('condition')}
            [Provide a clear, accurate definition of the patient's condition]
            
            ## Challenges Faced By Patient
            [List 3-5 specific challenges this patient might face based on their condition]
            
            ## Recommended Meal Plan
            [Create a 7-day meal plan that specifically addresses their medical condition]
            
            The meal plan must be in this exact markdown table format with breakfast, lunch, and dinner for all 7 days:
            
            | Day | Breakfast (kcal) | Lunch (kcal) | Dinner (kcal) |
            |-----|------------------|--------------|---------------|
            | Monday | [meal] (kcal) | [meal] (kcal) | [meal] (kcal) |
            | Tuesday | [meal] (kcal) | [meal] (kcal) | [meal] (kcal) |
            ...and so on for all 7 days
            
            ## Ingredients
            Organize all needed ingredients into three categories:
            
            ### Produce
            - [list all fresh produce]
            
            ### Groceries
            - [list all grocery items]
            
            ### Dry Goods
            - [list all dry goods, grains, etc.]
            
            Make sure all meals adhere strictly to any allergies and dietary preferences listed, and are specifically designed to help with the patient's condition of {patient_data.get('condition')}.
            """
            
            # Create proper HumanMessage object
            user_message = HumanMessage(content=prompt)
            
            # Create system message for clear direction
            system_message = SystemMessage(content="""You are a specialized medical AI assistant that creates 
            comprehensive medical reports. You must focus on providing evidence-based information and practical 
            meal plans specifically tailored to the patient's medical condition. All recommendations must be 
            medically appropriate for their condition. Include calorie counts for all meals. Format your response 
            as a well-structured markdown document exactly following the template specified.""")
            
            # Log the process
            logger.info(f"Processing patient data for {patient_data.get('name')}")
            logger.info(f"Using thread_id: {thread_id}")
            
            # Create inputs with both messages
            inputs = {"messages": [system_message, user_message]}
            
            # Process through graph
            response = self.llm_graph.invoke(inputs, config=config_params)
            
            # Extract the markdown content from the AI message
            markdown_report = ""
            if 'messages' in response:
                for msg in response['messages']:
                    if isinstance(msg, AIMessage):
                        markdown_report = msg.content
                        break
            
            # Add the markdown report to the response
            response['markdown_report'] = markdown_report
            
            # Log completion
            logger.info(f"Successfully generated medical report for {patient_data.get('name')}")
            
            return response
        except Exception as e:
            error_msg = f"Error processing patient data: {str(e)}"
            logger.error(error_msg)
            logger.exception(e)  # Log the full stack trace
            return {"error": error_msg}

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
    
def test_patient_report():
    """Test function to verify the patient report generation functionality"""
    print("Initializing ChatService...")
    chat_service = ChatService()
    
    # Sample patient data
    patient_data = {
        "name": "John Doe",
        "age": 45,
        "gender": "Male",
        "weight": 82,
        "height": 178,
        "condition": "Type 2 Diabetes",
        "allergies": ["shellfish", "peanuts"],
        "medications": ["Metformin 500mg", "Lisinopril 10mg"],
        "symptoms": ["fatigue", "increased thirst", "blurred vision"],
        "dietary_preferences": ["low carb"]
    }
    
    print(f"\nGenerating report for patient: {patient_data['name']}")
    print(f"Condition: {patient_data['condition']}")
    
    # Process the patient data
    response = chat_service.process_patient_data(patient_data)
    
    # Print the response
    if "error" in response:
        print(f"Error: {response['error']}")
    else:
        print("\nGenerated Medical Report:")
        print("-" * 50)
        print(response.get("markdown_report", "No report generated"))
        print("-" * 50)
        
# Uncomment to run the test
# if __name__ == "__main__":
#     test_patient_report()
