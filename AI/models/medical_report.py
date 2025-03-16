from typing import List, Optional, Dict
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
    # Adding meal plan fields with 3-day limit
    meal_plan_days: int = Field(
        description="Number of days for meal plan generation",
        default=3,  # Set default to 3 days
    )
    meal_plan: Optional[Dict[str, List[Dict[str, str]]]] = Field(
        description="Meal plan for the specified number of days based on condition and preferences",
        default=None,
    ) 