from fastapi import HTTPException
from ..db.supabase import get_db
import uuid
from datetime import datetime
from passlib.context import CryptContext
from typing import Dict
from ..db import supabase

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self):
        self.supabase = get_db()
        self.table = "cust_users"
        self.supabase.postgrest.schema(schema="public")
        
    def create_user(self, user_data):
        # Check if user exists
        existing_user = self.supabase.schema("public").from_("cust_users") \
            .select("*") \
            .eq("email", user_data.email) \
            .execute()
            
        if existing_user.data:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash the password
        hashed_password = pwd_context.hash(user_data.password)
        
        # Prepare user data
        new_user = {
            "name": user_data.name,
            "email": user_data.email,
            "password": hashed_password,
            "role": user_data.role,
            "nutri_code":user_data.nutri_code
        }
        
        # Insert into Supabase
        result = self.supabase.from_(self.table) \
        .insert(new_user) \
        .execute()
            
        return result.data[0]

    async def get_user_role(self, user_id: str) -> str:
        """Get user's role from database"""
        try:
            result = supabase.table("cust_users")\
                .select("role")\
                .eq("user_id", user_id)\
                .execute()
                
            if not result.data:
                raise HTTPException(
                    status_code=404,
                    detail=f"User with ID {user_id} not found"
                )
                
            return result.data[0]["role"]
            
        except Exception as e:
            print(f"Error getting user role: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get user role: {str(e)}"
            )

    async def verify_doctor_role(self, user_id: str) -> bool:
        """Verify if user has doctor role"""
        try:
            role = await self.get_user_role(user_id)
            if role != "doctor":
                raise HTTPException(
                    status_code=403,
                    detail="Only doctors can perform this action"
                )
            return True
            
        except HTTPException as e:
            raise e
        except Exception as e:
            print(f"Error verifying doctor role: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to verify doctor role: {str(e)}"
            )