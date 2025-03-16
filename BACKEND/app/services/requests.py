from datetime import datetime
from fastapi import HTTPException
from ..models.requests import NutritionRequest, NutritionRequestCreate
from ..db import supabase
import httpx
from typing import List, Dict, Any
from ..config import settings

class NutritionRequestService:
    def __init__(self):
        self.valid_statuses = ["pending", "in_review", "approved", "rejected"]
        self.table = "nutrition_requests"
        self.nevin_api_url = settings.NEVIN  

    async def get_nevin_suggestions(self, request_data: Dict[Any, Any]) -> str:
        """
        Makes an API call to Nevin's suggestion service.
        This is a placeholder until you have the actual endpoint.
        """
        try:
            # Prepare the data for Nevin's API
            nevin_request = {
                "conditions": request_data.get("conditions"),
                "symptoms": request_data.get("symptoms"),
                "diet_restriction": request_data.get("diet_restriction"),
                "triggers": request_data.get("triggers"),
                "concerns": request_data.get("concerns")
            }

        
            async with httpx.AsyncClient() as client:
                 response = await client.post(
                     self.nevin_api_url,
                     json=nevin_request,
                     timeout=30.0
                 )
                 if response.status_code == 200:
                     return response.json()["suggestions"]
            
            # For now, return a placeholder message
            return "Placeholder for Nevin's suggestions. API endpoint not yet implemented."
            
        except Exception as e:
            print(f"Error getting Nevin suggestions: {str(e)}")
            return "Failed to get automated suggestions. Please review manually."

    async def create_request(self, request: NutritionRequestCreate) -> NutritionRequest:
        try:
            # Prepare the initial data
            data = {
                "patient_id": request.patient_id,
                "nutri_code": request.nutri_code,
                "conditions": request.conditions,
                "symptoms": request.symptoms,
                "diet_restriction": request.diet_restriction,
                "triggers": request.triggers,
                "concerns": request.concerns,
                "status": "pending",
                "created_at": datetime.utcnow().isoformat(),
            }
            
            # Get suggestions from Nevin's API
            nevin_suggestions = await self.get_nevin_suggestions(data)
            data["nevin_suggest"] = nevin_suggestions
            
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
