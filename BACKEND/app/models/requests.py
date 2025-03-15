from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class NutritionRequest(BaseModel):
    id: int
    created_at: datetime
    patient_id: int
    nutri_code: Optional[str] = None
    conditions: Optional[str] = None
    symptoms: Optional[str] = None
    diet_restriction: Optional[str] = None
    triggers: Optional[str] = None
    concerns: Optional[str] = None
    nevin_suggest: Optional[str] = None
    approved_reco: Optional[str] = None
    status: Optional[str] = None
    updated_at: Optional[datetime] = None

class NutritionRequestCreate(BaseModel):
    patient_id: int
    nutri_code: str 
    conditions: Optional[str] = None
    symptoms: Optional[str] = None
    diet_restriction: Optional[str] = None
    triggers: Optional[str] = None
    concerns: Optional[str] = None
