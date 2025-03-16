from fastapi import APIRouter, HTTPException, Depends
from ..models.users import User, CreateUser
from ..db import supabase
from ..services import UserService
from typing import List

router = APIRouter()

user_service =UserService()

@router.post("/register", response_model=User)
async def create_user(user: CreateUser):
    try:
        new_user = user_service.create_user(user)
        return new_user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")


