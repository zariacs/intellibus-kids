from fastapi import APIRouter, HTTPException
from ..models.requests import (
    NutritionRequest, 
    NutritionRequestCreate, 
    RequestAction,
    RequestActionResponse
)
from ..services.requests import NutritionRequestService
from ..services.users import UserService
from ..config import settings
from typing import List, Dict
import httpx

router = APIRouter()
request_service = NutritionRequestService()
user_service = UserService()

@router.post("/create", response_model=NutritionRequest)
async def create_request(request: NutritionRequestCreate):
    try:
        # First get user data
        user_data = await request_service.get_user_data(request.patient_id)
        
        # Format data for Nevin
        nevin_request = await request_service.format_nevin_request(user_data, request)
        
        # Get Nevin suggestion
        try:
            nevin_response = await get_nevin_suggestion(nevin_request)
            nevin_suggest = nevin_response.get("markdown_report", "") if nevin_response else ""
            print(f"Nevin suggestion received: {nevin_suggest}")
        except Exception as nevin_error:
            print(f"Error getting Nevin suggestion: {nevin_error}")
            nevin_suggest = "Failed to get automated suggestions. Please review manually."
        
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

@router.post("/approve", response_model=NutritionRequest)
async def approve_request(request: RequestAction):
    """Approve a request and move nevin_suggest to approved_recommendation"""
    try:
        # Verify doctor role
        await user_service.verify_doctor_role(request.user_id)
        
        # Get current request to access nevin_suggest
        current_request = await request_service.get_request_by_id(request.request_id)
       
        # Store the current nevin_suggest value
        suggestion_to_approve = current_request.nevin_suggest
        
        if not suggestion_to_approve:
            raise HTTPException(
                status_code=400,
                detail="Cannot approve request: No suggestion available"
            )
        
        # Approve request and move nevin_suggest to approved_reccomendation
        # Note the spelling of approved_reccomendation to match the model
        result = await request_service.update_request_status(
            request_id=request.request_id,
            status="approved",
            approved_recommendation=suggestion_to_approve
        )
        
        return result
            
    except Exception as e:
        print(f"Error approving request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to approve request: {str(e)}"
        )

@router.post("/deny", response_model=NutritionRequest)
async def deny_request(request: RequestAction):
    """Deny a request"""
    try:
        # Verify doctor role
        await user_service.verify_doctor_role(request.user_id)
        
        # Get current request
        current_request = await request_service.get_request_by_id(request.request_id)
        
        # Deny request
        result = await request_service.update_request_status(
            request_id=request.request_id,
            status="rejected"
        )
        
        return result
            
    except Exception as e:
        print(f"Error denying request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to deny request: {str(e)}"
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

@router.post("/patient/requests", response_model=List[NutritionRequest])
async def get_patient_requests(user_id: str):
    """Get all requests for a specific patient"""
    try:
        # Verify the user exists
        await request_service.get_user_data(user_id)
        
        # Get all requests for this patient
        requests = await request_service.get_requests_by_patient(user_id)
        return requests
            
    except Exception as e:
        print(f"Error fetching patient requests: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch patient requests: {str(e)}"
        )
