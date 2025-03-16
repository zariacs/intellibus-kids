from typing import List, Optional
from pydantic import BaseModel, Field

class PatientReportRequest(BaseModel):
    """Request model for patient report generation"""
    name: str = Field(description="Patient's full name")
    condition: str = Field(description="Patient's primary medical condition")
    age: int = Field(description="Patient's age in years")
    gender: str = Field(description="Patient's gender")
    weight: float = Field(description="Patient's weight in kg")
    height: float = Field(description="Patient's height in cm")
    allergies: List[str] = Field(
        description="List of patient's allergies", 
        default_factory=list
    )
    medications: List[str] = Field(
        description="List of patient's current medications with dosage",
        default_factory=list
    )
    symptoms: List[str] = Field(
        description="List of patient's reported symptoms",
        default_factory=list
    )
    dietary_preferences: List[str] = Field(
        description="List of patient's dietary preferences or restrictions",
        default_factory=list
    )
    
class PatientReportResponse(BaseModel):
    """Response model for patient report generation"""
    success: bool = Field(description="Whether the report generation was successful")
    message: str = Field(description="Information message about the report generation")
    report: Optional[dict] = Field(description="The generated medical report", default=None)
    error: Optional[str] = Field(description="Error message if any", default=None) 