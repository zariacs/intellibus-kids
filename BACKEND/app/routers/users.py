from fastapi import APIRouter, HTTPException, Depends
from ..models.users import User, CreateUser
from ..db import supabase
from typing import List

router = APIRouter()


@router.post("/register", response_model=User)
async def create_user(user: CreateUser):
    # Register user with Supabase Auth and add to users table
    try:
        # Insert user data into nutri_lab.users table
        data = {
            "name": user.name,
            "role": user.role, 
            "email": user.email,
            "nutriCode": user.nutriCode
        }
        
        result = supabase.table("nutri_labs.users").insert(data).execute()
        
        if not result.data:
            raise HTTPException(status_code=400, detail="Failed to create user")
            
        created_user = result.data[0]
        return User(**created_user)
    except:
        print('Unable to create user')
