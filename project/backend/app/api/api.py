from fastapi import APIRouter
from app.api.endpoints import pinnacle

api_router = APIRouter()
api_router.include_router(pinnacle.router, prefix="/api/v1")
