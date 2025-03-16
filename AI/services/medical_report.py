from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from AI.models.medical_report import MedicalReport
from AI.config.logging_info import setup_logger

# Set up logger
logger = setup_logger("medical_report_service")

class MedicalReportService:
    """Service for generating structured medical reports using LangGraph"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        """
        Initialize the medical report service
        
        Args:
            api_key: OpenAI API key
            model: Model to use for generation (default: gpt-4o)
        """
        # Initialize the language model
        logger.info(f"Initializing LLM with model: {model}")
        self.llm = ChatOpenAI(api_key=api_key, model=model, temperature=0)
        
        @tool
        def check_diabetes_symptoms(symptoms: List[str]) -> str:
            """Check if symptoms match common diabetes indicators."""
            diabetes_symptoms = [
                "frequent urination", "increased thirst", "extreme hunger",
                "unexplained weight loss", "fatigue", "blurred vision"
            ]
            matches = [s for s in symptoms if any(ds in s.lower() for ds in diabetes_symptoms)]
            
            result = ""
            if len(matches) >= 3:
                result = "Multiple symptoms consistent with diabetes detected."
            elif len(matches) > 0:
                result = "Some symptoms may be related to diabetes."
            else:
                result = "No clear diabetes symptoms detected."
                
            logger.debug(f"Diabetes symptom check: {result} (matched {len(matches)}/{len(symptoms)} symptoms)")
            return result
        
        @tool
        def analyze_dietary_needs(condition: str, allergies: List[str]) -> str:
            """Analyze dietary needs based on condition and allergies."""
            dietary_advice = "General dietary recommendations: "
            
            if "diabetes" in condition.lower():
                dietary_advice += "Low-carb diet recommended. Monitor sugar intake. "
            
            if allergies:
                dietary_advice += f"Avoid foods containing: {', '.join(allergies)}. "
            
            logger.debug(f"Dietary analysis for {condition} with allergies {allergies}: {dietary_advice}")
            return dietary_advice
        
        @tool
        def generate_three_day_meal_plan(condition: str, dietary_preferences: List[str], allergies: List[str]) -> str:
            """Generate a 3-day meal plan based on medical condition, dietary preferences and allergies."""
            logger.info(f"Generating 3-day meal plan for condition: {condition}")
            
            # Start with a reminder about the 3-day limit
            meal_plan_guidance = "Generate a 3-day meal plan (exactly 3 days, not more) "
            meal_plan_guidance += f"for a patient with {condition}. "
            
            if dietary_preferences:
                meal_plan_guidance += f"Consider these dietary preferences: {', '.join(dietary_preferences)}. "
                
            if allergies:
                meal_plan_guidance += f"Avoid these allergens: {', '.join(allergies)}. "
                
            meal_plan_guidance += "The meal plan should include breakfast, lunch, dinner, and snacks for each day."
            
            logger.debug(f"Meal plan guidance created: {meal_plan_guidance}")
            return meal_plan_guidance
        
        self.tools = [check_diabetes_symptoms, analyze_dietary_needs, generate_three_day_meal_plan]
        logger.info(f"Initialized {len(self.tools)} medical tools")
        
        # Custom system prompt for accurate medical report generation
        self.system_prompt = """
        You are a medical assistant creating structured patient reports.
        Generate accurate, detailed medical information based on the patient details provided.
        Use the available tools to enhance the report with calculated values and checks.
        The output should be a complete medical report with all required fields populated.
        
        IMPORTANT: When generating meal plans, you MUST limit them to exactly 3 days.
        Do not create meal plans for more than 3 days under any circumstances.
        Structure the meal plan with days 1-3 only, providing breakfast, lunch, dinner, and snacks for each day.
        """
        
        # Create the React agent with structured output
        logger.info("Creating ReAct agent with structured output")
        self.agent = create_react_agent(
            self.llm,
            tools=self.tools,
            response_format=(self.system_prompt, MedicalReport),
        )
        logger.info("MedicalReportService initialization complete")
    
    def generate_report(self, patient_info: Dict[str, Any]) -> MedicalReport:
        """
        Generate a structured medical report based on patient information
        
        Args:
            patient_info: Dictionary containing patient information
            
        Returns:
            MedicalReport: Structured medical report
        """
        patient_name = patient_info.get("name", "Unknown Patient")
        logger.info(f"Generating report for patient: {patient_name}")
        
        # Format the patient information as a message to the agent
        patient_description = self._format_patient_info(patient_info)
        logger.debug("Patient description formatted for LLM")
        
        # Invoke the agent with the formatted message
        logger.info("Invoking LangGraph agent")
        inputs = {"messages": [("user", patient_description)]}
        response = self.agent.invoke(inputs)
        
        logger.info(f"Report generation successful for patient: {patient_name}")
        # Return the structured response
        return response["structured_response"]
    
    def _format_patient_info(self, patient_info: Dict[str, Any]) -> str:
        """
        Format patient information into a prompt for the agent
        
        Args:
            patient_info: Dictionary containing patient information
            
        Returns:
            str: Formatted prompt
        """
        prompt = "Generate a comprehensive medical report for the following patient:\n\n"
        
        for key, value in patient_info.items():
            if isinstance(value, list):
                prompt += f"{key.replace('_', ' ').title()}: {', '.join(value)}\n"
            else:
                prompt += f"{key.replace('_', ' ').title()}: {value}\n"
        
        prompt += "\nCreate a complete medical report with all required fields."
        prompt += "\nIf a meal plan is needed, ALWAYS limit it to EXACTLY 3 days, not 7 days or any other number."
        return prompt
