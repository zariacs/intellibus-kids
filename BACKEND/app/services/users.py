from fastapi import HTTPException
from ..db.supabase import get_db
import uuid
from datetime import datetime
from passlib.context import CryptContext

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