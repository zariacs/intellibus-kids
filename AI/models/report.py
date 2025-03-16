from pydantic import BaseModel, Field   

class LLMResponse(BaseModel):
    """Pydantic model for a LLM's response to a question."""
    #answer: str = Field(description="A 200 word essay from the details using the article document data.", default="")
    #title: List[str] = Field(description="The titles of the articles", default_factory=list)
    #links: List[str] = Field(description="The URLs of the articles", default_factory=list)
    #name_source: List[str] = Field(description="The sources of the articles", default_factory=list)
    #date: List[str] = Field(description="The dates of the articles", default_factory=list)
    #metadata: Optional[dict] = Field(description="Relevant non-empty article metadata", default_factory=dict)
    
    patient_details: list[str] = Field(description="Contains the personal details of the patient")
    meal_plan: str = Field(description="A 7-day meal plan for a patient")
    ingredients: str = Field(description="The ingredients which will be used to create the meal plan")
    
    
    class Config:
        """Configuration for the Pydantic model"""
        validate_assignment = True
        arbitrary_types_allowed = True
        from_attribute = True