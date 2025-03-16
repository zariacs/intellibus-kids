from fastapi import APIRouter, Request, HTTPException, Depends
import json
from ..services.clerk import ClerkIntegrationService

router = APIRouter()

# Initialize the service
clerk_service = ClerkIntegrationService()

async def verify_clerk_webhook(request: Request) -> bool:
    """Verify that the webhook request is coming from Clerk."""
    try:

        svix_id = request.headers.get("svix-id")
        svix_timestamp = request.headers.get("svix-timestamp")
        svix_signature = request.headers.get("svix-signature")


        if not all([svix_id, svix_timestamp, svix_signature]):
            raise HTTPException(status_code=401, detail="Missing required Clerk webhook headers")
        
        return True
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid webhook request: {str(e)}")

@router.post("/clerk")
async def handle_clerk_webhook(request: Request, verified: bool = Depends(verify_clerk_webhook)):
    """Handle webhook events from Clerk."""
    try:
        body = await request.body()
        payload = json.loads(body)
        
        event_type = payload.get("type")
        
        if event_type == "user.created":
            result = await clerk_service.process_user_creation(payload)
            return result
        else:
            return {
                "status": "acknowledged", 
                "event": event_type,
                "message": f"Event {event_type} received but not processed"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing webhook: {str(e)}")