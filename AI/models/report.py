from typing import List, Optional
from pydantic import BaseModel, Field   

class LLMResponse(BaseModel):
    """Pydantic model for a LLM's response to a medical report question."""
    
    patient_details: List[str] = Field(
        description="Contains the personal details of the patient (name, age, condition, allergies)",
        default_factory=list
    )
    condition_definition: str = Field(
        description="A clear definition of the patient's medical condition",
        default=""
    )
    challenges: List[str] = Field(
        description="Challenges faced by the patient due to their condition",
        default_factory=list
    )
    meal_plan: str = Field(
        description="A 7-day meal plan with breakfast, lunch, and dinner that addresses the patient's condition",
        default=""
    )
    ingredients: str = Field(
        description="A categorized list of ingredients needed for the meal plan (produce, groceries, dry goods)",
        default=""
    )
    
    class Config:
        """Configuration for the Pydantic model"""
        validate_assignment = True
        arbitrary_types_allowed = True
        from_attribute = True