from fastapi import APIRouter, HTTPException
from ..models.requests import NutritionRequest, NutritionRequestCreate
from ..services.requests import NutritionRequestService
from ..config import settings
from typing import List, Dict
import httpx

router = APIRouter()
request_service = NutritionRequestService()

@router.post("/create", response_model=NutritionRequest)
async def create_request(request: NutritionRequestCreate):
    try:
        # First get user data
        user_data = await request_service.get_user_data(request.patient_id)
        
        # Format data for Nevin
        nevin_request = await request_service.format_nevin_request(user_data, request)
        
        # Use the Nevin router endpoint instead of direct API call
        nevin_response = await get_nevin_suggestion(nevin_request)
        print(f"Nevin said {nevin_response}")
        nevin_suggest = nevin_response.get("suggestion", "No suggestion provided")
        
        # Create request with the Nevin suggestion
        data = request.model_dump()
        data["nevin_suggest"] = nevin_suggest
        
        # Call create_request with the updated data
        result = await request_service.create_request_with_suggestion(data)
        return result
            
    except Exception as e:
        print(f"Error in create_request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create request: {str(e)}"
        )

@router.patch("/{request_id}/status", response_model=NutritionRequest)
async def update_request_status(
    request_id: int, 
    status: str,
    nevin_suggest: str | None = None,
    approved_reco: str | None = None
):
    return request_service.update_request_status(
        request_id=request_id,
        status=status,
        nevin_suggest=nevin_suggest,
        approved_reco=approved_reco
    )

@router.post("/nevin/suggest", response_model=Dict)
async def get_nevin_suggestion(request_data: dict):
    """
    Direct endpoint to test Nevin's API suggestions.
    """
    try:
        if not settings.NEVIN:
            raise HTTPException(
                status_code=500,
                detail="Nevin API endpoint not configured"
            )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.NEVIN,
                json=request_data,
                timeout=150
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Nevin API error: {response.text}"
                )
                
            return response.json()
            
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Nevin API request timed out"
        )
    except Exception as e:
        print(f"Error calling Nevin API: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get Nevin suggestions: {str(e)}"
        )
