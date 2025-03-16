from fastapi import APIRouter, HTTPException, Body, Depends
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, validator
from services.report_generation import ChatService

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

# Response Model
class MedicalReportResponse(BaseModel):
    markdown_report: str = Field(..., description="The medical report in markdown format")

@router.post("/generate_report", response_model=MedicalReportResponse)
async def generate_medical_report(patient_data: PatientDataRequest):
    """
    Generate a comprehensive medical report based on patient data
    
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

# Utility function to convert markdown to HTML (for future use)
def convert_markdown_to_html(markdown_text: str) -> str:
    """
    Convert markdown text to HTML (placeholder for future implementation)
    
    Note: Implement this function using a library like markdown2 or mistune when needed.
    """
    # This is a placeholder - will be implemented when HTML output is needed
    return f"<div>{markdown_text}</div>"  # Simple placeholder 