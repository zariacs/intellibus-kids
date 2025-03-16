from typing import List
from pydantic import BaseModel, Field

class MedicalReport(BaseModel):
    """Pydantic model for structured medical report response"""
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