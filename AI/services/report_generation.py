# LOCAL IMPORTS
from config.logging_info import setup_logger
from config.llm_setup import OpenAIChat
from models.report import LLMResponse, MealDay, Ingredients
from config.settings import config

# Third Party
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import time
import re
import json
from typing import Dict, Any, Optional, List
from pydantic import BaseModel

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
            # Initialize OpenAI using default config settings
            logger.info("Initializing LLM service...")
            self.llm = OpenAIChat()
            
            # Define the tools list with our standalone function
            tools = [get_context_from_vectorstore]
            
            # Initialize the vectorstore db
            logger.info("Initializing vectorstore...")
            
            # Create the agent after tools are defined
            logger.info("Initializing AGENT (with memory)...")
            memory = MemorySaver()
            
            # Create the ReAct agent with tools
            self.llm_graph = create_react_agent(
                model=self.llm.llm,
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
            
            # Initialize the report structure
            report = {
                "patient_name": patient_data.get('name'),
                "patient_age": age,
                "patient_gender": gender,
                "patient_weight": weight,
                "patient_height": height,
                "patient_condition": patient_data.get('condition'),
                "patient_allergies": allergies_text,
                "report_title": f"Medical Report for {patient_data.get('name')}",
                "condition_definition": "",
                "challenges": [],
                "meal_plan": [],
                "ingredients": {
                    "produce": [],
                    "groceries": [],
                    "dry_goods": []
                }
            }
            
            # Log the process
            logger.info(f"Processing patient data for {patient_data.get('name')}")
            logger.info(f"Using thread_id: {thread_id}")
            
            # Step 1: Generate condition definition and challenges
            logger.info("Step 1: Generating condition definition and challenges")
            definition_prompt = f"""
            As a medical expert, provide the following information about {patient_data.get('condition')}:
            
            1. A clear, concise definition of the condition (2-3 sentences)
            2. List 3-5 specific challenges that {patient_data.get('name')} might face with this condition
            
            Format your response as a JSON object with two fields:
            - "definition": the definition of the condition
            - "challenges": an array of challenges
            
            Example:
            {{
                "definition": "Type 2 Diabetes is a chronic condition that affects the way the body processes blood sugar (glucose).",
                "challenges": [
                    "Managing blood sugar levels throughout the day",
                    "Maintaining a consistent exercise routine",
                    "Following dietary restrictions"
                ]
            }}
            
            Return ONLY the JSON object, no other text.
            """
            
            definition_response = self.llm.invoke([
                SystemMessage(content="You are a medical expert specializing in chronic conditions. Provide accurate, evidence-based information in JSON format only."),
                HumanMessage(content=definition_prompt)
            ])
            
            # Extract definition and challenges
            try:
                # Try to parse JSON directly from the response
                definition_content = definition_response.content
                # Remove any markdown code block formatting if present
                definition_content = re.sub(r'```json\s*|\s*```', '', definition_content)
                definition_data = json.loads(definition_content)
                
                report["condition_definition"] = definition_data.get("definition", "")
                report["challenges"] = definition_data.get("challenges", [])
                
                logger.info(f"Successfully generated definition and {len(report['challenges'])} challenges")
            except Exception as e:
                logger.error(f"Error parsing definition response: {str(e)}")
                # Fallback to basic extraction
                definition_content = definition_response.content
                # Try to extract definition using regex
                definition_match = re.search(r'"definition":\s*"([^"]+)"', definition_content)
                if definition_match:
                    report["condition_definition"] = definition_match.group(1)
                
                # Try to extract challenges using regex
                challenges = re.findall(r'"([^"]+)"', re.search(r'"challenges":\s*\[(.*?)\]', definition_content, re.DOTALL).group(1) if re.search(r'"challenges":\s*\[(.*?)\]', definition_content, re.DOTALL) else "")
                report["challenges"] = challenges
            
            # Step 2: Generate meal plan day by day
            logger.info("Step 2: Generating meal plan")
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            
            # Create a comprehensive prompt for the entire meal plan
            meal_plan_prompt = f"""
            Create a 7-day meal plan for {patient_data.get('name')}, who has {patient_data.get('condition')}.
            
            Patient details:
            - Allergies: {allergies_text}
            - Dietary preferences: {dietary_prefs}
            
            For each day (Monday through Sunday), provide:
            - Breakfast with calorie count
            - Lunch with calorie count
            - Dinner with calorie count
            
            Format your response as a JSON array of objects, where each object represents one day:
            [
                {{
                    "day": "Monday",
                    "breakfast": "Oatmeal with berries and nuts (350 kcal)",
                    "lunch": "Grilled chicken salad with olive oil dressing (450 kcal)",
                    "dinner": "Baked salmon with roasted vegetables (550 kcal)"
                }},
                ... and so on for all 7 days
            ]
            
            Ensure all meals:
            1. Are appropriate for someone with {patient_data.get('condition')}
            2. Avoid any allergens: {allergies_text}
            3. Respect dietary preferences: {dietary_prefs}
            4. Include calorie counts for each meal
            
            Return ONLY the JSON array, no other text.
            """
            
            meal_plan_response = self.llm.invoke([
                SystemMessage(content="You are a nutritionist specializing in medical diets. Create appropriate meal plans in JSON format only."),
                HumanMessage(content=meal_plan_prompt)
            ])
            
            # Parse and add to meal plan
            try:
                # Try to parse JSON directly from the response
                meal_plan_content = meal_plan_response.content
                # Remove any markdown code block formatting if present
                meal_plan_content = re.sub(r'```json\s*|\s*```', '', meal_plan_content)
                meal_plan_data = json.loads(meal_plan_content)
                
                # Convert to our meal plan format
                for day_data in meal_plan_data:
                    meal_day = {
                        "day": day_data.get("day", ""),
                        "breakfast": day_data.get("breakfast", ""),
                        "lunch": day_data.get("lunch", ""),
                        "dinner": day_data.get("dinner", "")
                    }
                    report["meal_plan"].append(meal_day)
                
                logger.info(f"Successfully generated meal plan with {len(report['meal_plan'])} days")
            except Exception as e:
                logger.error(f"Error parsing meal plan response: {str(e)}")
                # If JSON parsing fails, try to extract using regex
                meal_plan_content = meal_plan_response.content
                
                # Try to extract each day's meals using regex
                for day in days:
                    day_pattern = rf'{{"day":\s*"{day}",\s*"breakfast":\s*"([^"]+)",\s*"lunch":\s*"([^"]+)",\s*"dinner":\s*"([^"]+)"'
                    day_match = re.search(day_pattern, meal_plan_content)
                    
                    if day_match:
                        meal_day = {
                            "day": day,
                            "breakfast": day_match.group(1),
                            "lunch": day_match.group(2),
                            "dinner": day_match.group(3)
                        }
                        report["meal_plan"].append(meal_day)
            
            # Step 3: Generate ingredients list
            logger.info("Step 3: Generating ingredients list")
            
            # Create a prompt for the ingredients based on the meal plan
            meal_plan_text = ""
            for day in report["meal_plan"]:
                meal_plan_text += f"{day['day']}:\n"
                meal_plan_text += f"- Breakfast: {day['breakfast']}\n"
                meal_plan_text += f"- Lunch: {day['lunch']}\n"
                meal_plan_text += f"- Dinner: {day['dinner']}\n\n"
            
            ingredients_prompt = f"""
            Based on the following 7-day meal plan for a patient with {patient_data.get('condition')}, 
            create a comprehensive shopping list of all ingredients needed, categorized into:
            - Produce (fresh fruits and vegetables)
            - Groceries (packaged foods, dairy, meat, etc.)
            - Dry Goods (grains, pasta, rice, beans, etc.)
            
            Meal Plan:
            {meal_plan_text}
            
            Format your response as a JSON object with three arrays:
            {{
                "produce": ["Item 1", "Item 2", ...],
                "groceries": ["Item 1", "Item 2", ...],
                "dry_goods": ["Item 1", "Item 2", ...]
            }}
            
            Combine similar ingredients and provide quantities where appropriate.
            Return ONLY the JSON object, no other text.
            """
            
            ingredients_response = self.llm.invoke([
                SystemMessage(content="You are a nutritionist creating shopping lists. Organize ingredients by category in JSON format only."),
                HumanMessage(content=ingredients_prompt)
            ])
            
            # Parse and add ingredients
            try:
                # Try to parse JSON directly from the response
                ingredients_content = ingredients_response.content
                # Remove any markdown code block formatting if present
                ingredients_content = re.sub(r'```json\s*|\s*```', '', ingredients_content)
                ingredients_data = json.loads(ingredients_content)
                
                report["ingredients"]["produce"] = ingredients_data.get("produce", [])
                report["ingredients"]["groceries"] = ingredients_data.get("groceries", [])
                report["ingredients"]["dry_goods"] = ingredients_data.get("dry_goods", [])
                
                logger.info(f"Successfully generated ingredients list with {len(report['ingredients']['produce'])} produce items, "
                           f"{len(report['ingredients']['groceries'])} grocery items, and {len(report['ingredients']['dry_goods'])} dry goods")
            except Exception as e:
                logger.error(f"Error parsing ingredients response: {str(e)}")
                # If JSON parsing fails, try to extract using regex
                ingredients_content = ingredients_response.content
                
                # Try to extract each category using regex
                produce_match = re.search(r'"produce":\s*\[(.*?)\]', ingredients_content, re.DOTALL)
                if produce_match:
                    produce_items = re.findall(r'"([^"]+)"', produce_match.group(1))
                    report["ingredients"]["produce"] = produce_items
                
                groceries_match = re.search(r'"groceries":\s*\[(.*?)\]', ingredients_content, re.DOTALL)
                if groceries_match:
                    groceries_items = re.findall(r'"([^"]+)"', groceries_match.group(1))
                    report["ingredients"]["groceries"] = groceries_items
                
                dry_goods_match = re.search(r'"dry_goods":\s*\[(.*?)\]', ingredients_content, re.DOTALL)
                if dry_goods_match:
                    dry_goods_items = re.findall(r'"([^"]+)"', dry_goods_match.group(1))
                    report["ingredients"]["dry_goods"] = dry_goods_items
            
            # Log completion
            logger.info(f"Successfully generated structured report for {patient_data.get('name')}")
            
            return report
        except Exception as e:
            error_msg = f"Error processing patient data: {str(e)}"
            logger.error(error_msg)
            logger.exception(e)  # Log the full stack trace
            return {"error": error_msg}
