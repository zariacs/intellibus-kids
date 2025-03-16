from fastapi import APIRouter
from . import users,requests


api_router = APIRouter()

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)

api_router.include_router(
    requests.router,
    prefix="/requests",
    tags=["requests"]
)