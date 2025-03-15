from fastapi import APIRouter
from . import users

api_router = APIRouter()

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)