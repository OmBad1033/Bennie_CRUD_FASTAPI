from fastapi import APIRouter
from .endpoints import task


api_router = APIRouter()
print("Starting")
api_router.include_router(
    task.product
)