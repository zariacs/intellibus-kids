from fastapi import APIRouter, HTTPException, Body, Depends
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, validator
from services.report_generation import ChatService
from models.report import MealDay, Ingredients

# Initialize router
router = APIRouter(prefix="/api/v1", tags=["Medical Reports"])

# Initialize ChatService (could be moved to dependency injection)
chat_service = ChatService()

# Request Model
class PatientDataRequest(BaseModel):
    name: str = Field(..., description="Patient's full name")
    condition: str = Field(..., description="Medical condition")
    age: Optional[int] = Field(None, description="Patient's age")
    gender: Optional[str] = Field(None, description="Patient's gender")
    weight: Optional[float] = Field(None, description="Patient's weight in kg")
    height: Optional[float] = Field(None, description="Patient's height in cm")
    allergies: Optional[List[str]] = Field(None, description="List of patient's allergies")
    medications: Optional[List[str]] = Field(None, description="List of current medications")
    symptoms: Optional[List[str]] = Field(None, description="List of current symptoms")
    dietary_preferences: Optional[List[str]] = Field(None, description="List of dietary preferences")
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('name cannot be empty')
        return v
    
    @validator('condition')
    def condition_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('condition cannot be empty')
        return v

# Response Models
class MedicalReportResponse(BaseModel):
    markdown_report: str = Field(..., description="The medical report in markdown format")

# New structured JSON response model
class StructuredMealDay(BaseModel):
    day: str = Field(..., description="Day of the week")
    breakfast: str = Field(..., description="Breakfast meal with calorie count")
    lunch: str = Field(..., description="Lunch meal with calorie count")
    dinner: str = Field(..., description="Dinner meal with calorie count")

class StructuredIngredients(BaseModel):
    produce: List[str] = Field(..., description="List of fresh produce ingredients")
    groceries: List[str] = Field(..., description="List of grocery items")
    dry_goods: List[str] = Field(..., description="List of dry goods and grains")

class StructuredMedicalReportResponse(BaseModel):
    # Patient information section
    patient_name: str = Field(..., description="Patient's full name")
    patient_age: str = Field(..., description="Patient's age")
    patient_gender: str = Field(..., description="Patient's gender")
    patient_weight: str = Field(..., description="Patient's weight")
    patient_height: str = Field(..., description="Patient's height")
    patient_condition: str = Field(..., description="Patient's medical condition")
    patient_allergies: str = Field(..., description="Patient's allergies")
    
    # Report sections
    report_title: str = Field(..., description="Title of the medical report")
    condition_definition: str = Field(..., description="A clear definition of the patient's medical condition")
    challenges: List[str] = Field(..., description="Challenges faced by the patient due to their condition")
    
    # Meal plan (high priority with multi-day breakdown)
    meal_plan: List[StructuredMealDay] = Field(..., description="A 7-day meal plan with breakfast, lunch, and dinner")
    
    # Ingredients with category breakdown
    ingredients: StructuredIngredients = Field(..., description="Categorized list of ingredients needed for the meal plan")

@router.post("/generate_report", response_model=MedicalReportResponse)
async def generate_medical_report(patient_data: PatientDataRequest):
    """
    Generate a comprehensive medical report based on patient data in markdown format
    
    The report includes:
    - Patient details
    - Definition of the condition
    - Challenges faced by the patient
    - A 7-day meal plan with breakfast, lunch, and dinner
    - List of ingredients categorized by type
    
    All meal plans are specifically tailored to the patient's condition and respect any allergies
    or dietary preferences.
    """
    try:
        # Convert Pydantic model to dict
        patient_dict = patient_data.dict()
        
        # Process the patient data
        response = chat_service.process_patient_data(patient_dict)
        
        # Check for errors in response
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
        
        # Extract the markdown report from the response
        markdown_report = response.get("markdown_report", "")
        if not markdown_report:
            raise HTTPException(status_code=500, detail="Failed to generate report content")
        
        # Return the report
        return {"markdown_report": markdown_report}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/generate_structured_report", response_model=StructuredMedicalReportResponse)
async def generate_structured_medical_report(patient_data: PatientDataRequest):
    """
    Generate a comprehensive medical report based on patient data in structured JSON format
    
    The report includes:
    - Patient details (name, age, gender, weight, height, condition, allergies)
    - Definition of the condition
    - Challenges faced by the patient
    - A 7-day meal plan with breakfast, lunch, and dinner for each day
    - List of ingredients categorized by type (produce, groceries, dry goods)
    
    All meal plans are specifically tailored to the patient's condition and respect any allergies
    or dietary preferences.
    """
    try:
        # Convert Pydantic model to dict
        patient_dict = patient_data.dict()
        
        # Process the patient data
        response = chat_service.process_patient_data(patient_dict)
        
        # Check for errors in response
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
        
        # Check if we have a structured response
        if not all(key in response for key in ["patient_name", "meal_plan", "ingredients"]):
            raise HTTPException(status_code=500, detail="Failed to generate structured report content")
        
        # Return the structured report directly
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Utility function to convert markdown to HTML (for future use)
def convert_markdown_to_html(markdown_text: str) -> str:
    """
    Convert markdown text to HTML (placeholder for future implementation)
    
    Note: Implement this function using a library like markdown2 or mistune when needed.
    """
    # This is a placeholder - will be implemented when HTML output is needed
    return f"<div>{markdown_text}</div>"  # Simple placeholder 