from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class Demographics(BaseModel):
    age: Optional[int] = None
    gender: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None

class NutritionRequest(BaseModel):
    id: int
    created_at: datetime
    patient_id: str
    nutri_code: Optional[str] = None
    conditions: Optional[List[str]] = None
    symptoms: Optional[List[str]] = None
    diet_restriction: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    medications: Optional[List[str]] = None
    dietary_preferences: Optional[List[str]] = None
    triggers: Optional[List[str]] = None
    concerns: Optional[List[str]] = None
    demographics: Optional[Demographics] = None  # Added demographics
    nevin_suggest: Optional[str] = None
    approved_reccomendation: Optional[str] = None
    status: Optional[str] = 'Pending'
    updated_at: Optional[datetime] = None

class NutritionRequestCreate(BaseModel):
    patient_id: str
    nutri_code: str 
    conditions: Optional[List[str]] = None
    symptoms: Optional[List[str]] = None
    diet_restriction: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    medications: Optional[List[str]] = None
    dietary_preferences: Optional[List[str]] = None
    triggers: Optional[List[str]] = None
    concerns: Optional[List[str]] = None
    approved_reccomendation: Optional[str] = None
    demographics: Optional[Demographics] = None 
    nevin_suggest: Optional[str] = None

class RequestAction(BaseModel):
    request_id: int
    user_id: str

class RequestActionResponse(BaseModel):
    success: bool
    message: str
    request: NutritionRequest