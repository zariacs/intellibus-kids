from typing import List
from pydantic import BaseModel, Field   

class MealDay(BaseModel):
    """Model for a single day in the meal plan"""
    day: str = Field(description="Day of the week")
    breakfast: str = Field(description="Breakfast meal with calorie count")
    lunch: str = Field(description="Lunch meal with calorie count")
    dinner: str = Field(description="Dinner meal with calorie count")

class Ingredients(BaseModel):
    """Model for categorized ingredients"""
    produce: List[str] = Field(description="List of fresh produce ingredients", default_factory=list)
    groceries: List[str] = Field(description="List of grocery items", default_factory=list)
    dry_goods: List[str] = Field(description="List of dry goods and grains", default_factory=list)

class LLMResponse(BaseModel):
    """Pydantic model for structured JSON response to a medical report question."""
    
    # Patient information section
    patient_name: str = Field(description="Patient's full name")
    patient_age: str = Field(description="Patient's age")
    patient_gender: str = Field(description="Patient's gender")
    patient_weight: str = Field(description="Patient's weight")
    patient_height: str = Field(description="Patient's height")
    patient_condition: str = Field(description="Patient's medical condition")
    patient_allergies: str = Field(description="Patient's allergies")
    
    # Report sections
    report_title: str = Field(description="Title of the medical report")
    condition_definition: str = Field(description="A clear definition of the patient's medical condition")
    challenges: List[str] = Field(description="Challenges faced by the patient due to their condition", default_factory=list)
    
    # Meal plan (high priority with multi-day breakdown)
    meal_plan: List[MealDay] = Field(
        description="A 7-day meal plan with breakfast, lunch, and dinner that addresses the patient's condition",
        default_factory=list
    )
    
    # Ingredients with category breakdown
    ingredients: Ingredients = Field(
        description="Categorized list of ingredients needed for the meal plan",
        default_factory=Ingredients
    )
    
    class Config:
        """Configuration for the Pydantic model"""
        validate_assignment = True
        arbitrary_types_allowed = True
        from_attribute = True