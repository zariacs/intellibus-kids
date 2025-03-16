from fastapi import HTTPException
import json
from typing import Dict, Any, Optional
from supabase import create_client, Client
from ..config import settings

class ClerkIntegrationService:
    def __init__(self):
        """Initialize the Supabase client for Clerk integration."""
        self.supabase: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_API
        )
        self.users_table = "cust_users"
        self.schema = "public"
    
    async def process_user_creation(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process user creation from Clerk webhook data."""
        try:
            user_data = webhook_data.get("data", {})
            
            # Extract email from email_addresses array
            email_addresses = user_data.get("email_addresses", [])
            email = email_addresses[0].get("email_address") if email_addresses else None
            
            if not email:
                raise HTTPException(status_code=400, detail="Email address required")
            
            # Extract name information
            first_name = user_data.get("first_name", "")
            last_name = user_data.get("last_name", "")
            full_name = f"{first_name} {last_name}".strip()
            
            # Default to 'user' role if not specified
            role = "patient"
            
            # Create user record
            user = {
                "email": email,
                "name": full_name if full_name else None,
                "role": role,
                # Password will be handled by Clerk, so we don't store it in Supabase
                # nutr_code is optional and would be set later for nutritionist users
            }
            
            # Insert the user into the cust_users table
            result = self.supabase.table(self.users_table).insert(user).execute()
            
            if not result.data:
                raise HTTPException(status_code=500, detail="Failed to create user in Supabase")
                
            return {
                "status": "success",
                "message": "User successfully added to database",
                "data": result.data[0]
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")
    
    async def update_user_role(self, email: str, role: str, nutr_code: Optional[str] = None) -> Dict[str, Any]:
        """Update user role and nutritionist code if applicable."""
        try:
            update_data = {"role": role}
            
            # Only add nutr_code if it's provided and role is nutritionist
            if role == "doctor" and nutr_code:
                update_data["nutri_code"] = nutr_code
            
            # Update the user record
            result = self.supabase.table(self.users_table) \
                .update(update_data) \
                .eq("email", email) \
                .execute()
            
            if not result.data:
                raise HTTPException(status_code=404, detail="User not found")
                
            return {
                "status": "success",
                "message": "User role updated successfully",
                "data": result.data[0]
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating user role: {str(e)}")