from datetime import datetime
from fastapi import HTTPException
from ..models.requests import NutritionRequest, NutritionRequestCreate
from ..db import supabase
from typing import Dict, Any, List
from tenacity import retry, stop_after_attempt, wait_exponential

class NutritionRequestService:
    def __init__(self):
        self.valid_statuses = ["pending", "in_review", "approved", "rejected"]
        self.table = "nutrition_requests"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def get_user_data(self, user_id: int) -> Dict:
        """Fetch user data from the users table with retry logic"""
        try:
            print(f"Attempting to fetch user data for ID: {user_id}")
            
            result = supabase.table("cust_users")\
                .select("*")\
                .eq("id", user_id)\
                .execute()
            
            if not result.data:
                raise HTTPException(
                    status_code=404,
                    detail=f"User with ID {user_id} not found"
                )
            
            return result.data[0]
            
        except Exception as e:
            print(f"Error in get_user_data: {type(e).__name__}, {str(e)}")
            if "Connection reset by peer" in str(e):
                raise ConnectionError(f"Database connection error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch user data: {str(e)}"
            )

    async def format_nevin_request(self, user_data: Dict, request: NutritionRequestCreate) -> Dict:
        """Format the request data for Nevin's API"""
        try:
            return {
                "name": user_data.get("name", ""),
                "condition": request.conditions[0] if request.conditions else "",
                "age": request.demographics.age if request.demographics else None,
                "gender": request.demographics.gender if request.demographics else None,
                "weight": request.demographics.weight if request.demographics else None,
                "height": request.demographics.height if request.demographics else None,
                "allergies": request.allergies or [],
                "medications": request.medications or [],
                "symptoms": request.symptoms or [],
                "dietary_preferences": request.dietary_preferences or []
            }
        except Exception as e:
            print(f"Error formatting Nevin request: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to format request data: {str(e)}"
            )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def create_request_with_suggestion(self, request_data: dict) -> NutritionRequest:
        """Create a request with a pre-fetched Nevin suggestion"""
        try:
            print(f"Creating request with data: {request_data}")
            
            data = {
                "patient_id": request_data["patient_id"],
                "nutri_code": request_data["nutri_code"],
                "conditions": request_data["conditions"],
                "symptoms": request_data["symptoms"],
                "diet_restriction": request_data.get("diet_restriction"),
                "allergies": request_data.get("allergies"),
                "medications": request_data.get("medications"),
                "dietary_preferences": request_data.get("dietary_preferences"),
                "triggers": request_data.get("triggers"),
                "concerns": request_data.get("concerns"),
                "demographics": request_data.get("demographics"),
                "nevin_suggest": request_data.get("nevin_suggest"),
                "status": "pending",
                "created_at": datetime.utcnow().isoformat(),
            }
            
            result = supabase.table(self.table).insert(data).execute()
            
            if not result.data:
                raise HTTPException(status_code=400, detail="Failed to create request")
            
            return NutritionRequest(**result.data[0])
            
        except Exception as e:
            print(f"Error in create_request_with_suggestion: {type(e).__name__}, {str(e)}")
            if "Connection reset by peer" in str(e):
                raise ConnectionError(f"Database connection error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while creating request: {str(e)}"
            )

    async def create_request(self, request: NutritionRequestCreate) -> NutritionRequest:
        try:
            # Get suggestions from Nevin's API
            nevin_suggest = await self.get_nevin_suggest(request)
            
            # Prepare the data for database
            data = {
                "patient_id": request.patient_id,
                "nutri_code": request.nutri_code,
                "conditions": request.conditions,
                "symptoms": request.symptoms,
                "diet_restriction": request.diet_restriction,
                "allergies": request.allergies,
                "medications": request.medications,
                "dietary_preferences": request.dietary_preferences,
                "triggers": request.triggers,
                "concerns": request.concerns,
                "demographics": request.demographics.dict() if request.demographics else None,
                "nevin_suggest": nevin_suggest,
                "status": "pending",
                "created_at": datetime.utcnow().isoformat(),
            }
            
            # Create the request in Supabase
            result = supabase.table(self.table).insert(data).execute()
            
            if not result.data:
                raise HTTPException(status_code=400, detail="Failed to create request")
                
            return NutritionRequest(**result.data[0])
            
        except Exception as e:
            print(f'Error creating request: {str(e)}')
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while creating request: {str(e)}"
            )

    def update_request_status(
        self, 
        request_id: int, 
        status: str,
        nevin_suggest: str | None = None,
        approved_reco: str | None = None
    ) -> NutritionRequest:
        try:
            # Validate status
            if status not in self.valid_statuses:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid status. Must be one of: {', '.join(self.valid_statuses)}"
                )
            
            # Prepare update data
            update_data = {
                "status": status,
                "updated_at": datetime.utcnow().isoformat()
            }
            
            # Add optional fields if provided
            if nevin_suggest is not None:
                update_data["nevin_suggest"] = nevin_suggest
            if approved_reco is not None:
                update_data["approved_reco"] = approved_reco
                
            result = supabase.table(self.table)\
                .update(update_data)\
                .eq("id", request_id)\
                .execute()
                
            if not result.data:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Request with ID {request_id} not found"
                )
                
            return NutritionRequest(**result.data[0])
            
        except HTTPException as e:
            raise e
        except Exception as e:
            print(f'Error updating request status: {str(e)}')
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while updating request: {str(e)}"
            )

    def get_requests_by_nutricode(self, nutri_code: str) -> List[NutritionRequest]:
        try:
            result = supabase.table(self.table)\
                .select("*")\
                .eq("nutri_code", nutri_code)\
                .order("created_at", desc=True)\
                .execute()
                
            if not result.data:
                return []  # Return empty list if no requests found
                
            return [NutritionRequest(**request) for request in result.data]
            
        except Exception as e:
            print(f'Error fetching requests by nutricode: {str(e)}')
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while fetching requests: {str(e)}"
            )
