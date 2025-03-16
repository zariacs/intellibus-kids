# LOCAL IMPORTS
from config.logging_info import setup_logger
from config.llm_setup import GeminiChat 
from models.report import LLMResponse, MealDay, Ingredients
from config.settings import config

# Third Party
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import time
import re
from typing import Dict, Any, Optional, List

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
                response_format=LLMResponse,  # Use our updated Pydantic model
                checkpointer=memory,
                tools=tools
            )
            
        except Exception as e:
            logger.error(f"Error initializing chat service: {str(e)}")
            raise  # Re-raise to properly handle the error
            
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
            dict: Response containing structured JSON report
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
            
            # Add instructions to return structured JSON using the Pydantic model format
            structured_output_instructions = SystemMessage(content="""After creating the markdown report, you must also 
            convert your output to a structured JSON format that follows this schema:
            {
                "patient_name": "Patient's name",
                "patient_age": "Patient's age",
                "patient_gender": "Patient's gender",
                "patient_weight": "Patient's weight",
                "patient_height": "Patient's height",
                "patient_condition": "Patient's condition",
                "patient_allergies": "Patient's allergies",
                "report_title": "Title of the medical report",
                "condition_definition": "Definition of the condition",
                "challenges": ["Challenge 1", "Challenge 2", "Challenge 3"],
                "meal_plan": [
                    {
                        "day": "Monday",
                        "breakfast": "Breakfast description with calories",
                        "lunch": "Lunch description with calories",
                        "dinner": "Dinner description with calories"
                    },
                    # Additional days...
                ],
                "ingredients": {
                    "produce": ["Item 1", "Item 2", ...],
                    "groceries": ["Item 1", "Item 2", ...],
                    "dry_goods": ["Item 1", "Item 2", ...]
                }
            }
            """)
            
            # Log the process
            logger.info(f"Processing patient data for {patient_data.get('name')}")
            logger.info(f"Using thread_id: {thread_id}")
            
            # Create inputs with all messages
            inputs = {"messages": [system_message, structured_output_instructions, user_message]}
            
            # Process through graph
            response = self.llm_graph.invoke(inputs, config=config_params)
            
            # Check if the response directly contains a structured output
            if isinstance(response, dict) and "output" in response:
                # If the agent returned a structured output object already
                structured_response = response["output"]
                logger.info("Successfully generated structured JSON report")
                return structured_response.model_dump()  # Convert Pydantic model to dict
            
            # If we need to parse the markdown content ourselves
            markdown_report = ""
            if 'messages' in response:
                for msg in response['messages']:
                    if isinstance(msg, AIMessage):
                        markdown_report = msg.content
                        break
            
            # Parse the markdown report into our structured format
            structured_report = self._parse_markdown_to_json(
                markdown_report, 
                patient_data.get('name'),
                age,
                gender,
                weight,
                height,
                patient_data.get('condition'),
                allergies_text
            )
            
            # Log completion
            logger.info(f"Successfully generated structured report for {patient_data.get('name')}")
            
            return structured_report
        except Exception as e:
            error_msg = f"Error processing patient data: {str(e)}"
            logger.error(error_msg)
            logger.exception(e)  # Log the full stack trace
            return {"error": error_msg}
    
    def _parse_markdown_to_json(self, markdown: str, name: str, age: str, gender: str, 
                               weight: str, height: str, condition: str, allergies: str) -> Dict[str, Any]:
        """Parse markdown report into structured JSON format
        
        Args:
            markdown: The markdown report text
            patient_info: Dictionary with patient information
            
        Returns:
            Dict[str, Any]: Structured JSON report
        """
        # Initialize response structure
        result = {
            "patient_name": name,
            "patient_age": age,
            "patient_gender": gender,
            "patient_weight": weight,
            "patient_height": height,
            "patient_condition": condition,
            "patient_allergies": allergies,
            "report_title": f"Medical Report for {name}",
            "condition_definition": "",
            "challenges": [],
            "meal_plan": [],
            "ingredients": {
                "produce": [],
                "groceries": [],
                "dry_goods": []
            }
        }
        
        # Extract definition of condition
        definition_pattern = r"## Definition of.*?\n(.*?)(?=##|$)"
        definition_match = re.search(definition_pattern, markdown, re.DOTALL)
        if definition_match:
            result["condition_definition"] = definition_match.group(1).strip()
        
        # Extract challenges
        challenges_pattern = r"## Challenges Faced By Patient.*?\n(.*?)(?=##|$)"
        challenges_match = re.search(challenges_pattern, markdown, re.DOTALL)
        if challenges_match:
            challenges_text = challenges_match.group(1).strip()
            # Extract individual challenges (assuming they're in a bullet point list)
            challenges = re.findall(r"- (.*?)(?=$|\n)", challenges_text)
            result["challenges"] = [challenge.strip() for challenge in challenges]
        
        # Extract meal plan
        meal_plan_pattern = r"\| (Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday) \| (.*?) \| (.*?) \| (.*?) \|"
        meal_plan_matches = re.findall(meal_plan_pattern, markdown)
        
        for match in meal_plan_matches:
            day = match[0]
            breakfast = match[1]
            lunch = match[2]
            dinner = match[3]
            
            result["meal_plan"].append({
                "day": day,
                "breakfast": breakfast,
                "lunch": lunch,
                "dinner": dinner
            })
        
        # Extract ingredients
        produce_pattern = r"### Produce\s*\n((?:- .*?\n)*)"
        produce_match = re.search(produce_pattern, markdown, re.DOTALL)
        if produce_match:
            produce_text = produce_match.group(1).strip()
            produce_items = re.findall(r"- (.*?)(?=$|\n)", produce_text)
            result["ingredients"]["produce"] = [item.strip() for item in produce_items]
        
        groceries_pattern = r"### Groceries\s*\n((?:- .*?\n)*)"
        groceries_match = re.search(groceries_pattern, markdown, re.DOTALL)
        if groceries_match:
            groceries_text = groceries_match.group(1).strip()
            groceries_items = re.findall(r"- (.*?)(?=$|\n)", groceries_text)
            result["ingredients"]["groceries"] = [item.strip() for item in groceries_items]
        
        dry_goods_pattern = r"### Dry Goods\s*\n((?:- .*?\n)*)"
        dry_goods_match = re.search(dry_goods_pattern, markdown, re.DOTALL)
        if dry_goods_match:
            dry_goods_text = dry_goods_match.group(1).strip()
            dry_goods_items = re.findall(r"- (.*?)(?=$|\n)", dry_goods_text)
            result["ingredients"]["dry_goods"] = [item.strip() for item in dry_goods_items]
        
        return result

# For testing the agent functionality
#def main():
#    """Test function to verify the LangGraph agent's functionality"""
#    print("Initializing ChatService...")
#    chat_service = ChatService()
#    
#    # First message
#    thread_id = "test_thread_123"
#    first_message = "What are the symptoms of diabetes?"
#    print(f"\nUser: {first_message}")
#    
#    response = chat_service.process_chat(first_message, thread_id)
#    print("\nAI Response:")
#    
#    # Handle response format correctly
#    if "error" in response:
#        print(f"Error: {response['error']}")
#    else:
#        # Print the structured response if available
#        if 'structured_response' in response:
#            result = response['structured_response']
#            print(f"Structured Response:")
#            if hasattr(result, 'meal_plan') and result.meal_plan:
#                print(f"Meal Plan: {result.meal_plan}")
#            if hasattr(result, 'ingredients') and result.ingredients:
#                print(f"Ingredients: {result.ingredients}")
#            if hasattr(result, 'patient_details') and result.patient_details:
#                print(f"Patient Details: {result.patient_details}")
#        
#        # Print the raw message content from AI
#        if 'messages' in response:
#            for msg in response['messages']:
#                from langchain_core.messages import AIMessage
#                if isinstance(msg, AIMessage):
#                    print(f"AI: {msg.content}")
#    
#    # Follow-up message to test memory
#    follow_up = "What treatments are available for it?"
#    print(f"\nUser: {follow_up}")
#    
#    response = chat_service.process_chat(follow_up, thread_id)
#    print("\nAI Response (with memory context):")
#    
#    # Handle response the same way
#    if "error" in response:
#        print(f"Error: {response['error']}")
#    else:
#        # Print the structured response if available
#        if 'structured_response' in response:
#            result = response['structured_response']
#            print(f"Structured Response:")
#            if hasattr(result, 'meal_plan') and result.meal_plan:
#                print(f"Meal Plan: {result.meal_plan}")
#            if hasattr(result, 'ingredients') and result.ingredients:
#                print(f"Ingredients: {result.ingredients}")
#            if hasattr(result, 'patient_details') and result.patient_details:
#                print(f"Patient Details: {result.patient_details}")
#        
#        # Print the raw message content from AI
#        if 'messages' in response:
#            for msg in response['messages']:
#                from langchain_core.messages import AIMessage
#                if isinstance(msg, AIMessage):
#                    print(f"AI: {msg.content}")