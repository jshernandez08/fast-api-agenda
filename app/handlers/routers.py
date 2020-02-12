from .contact import router as contactRouter
from fastapi import APIRouter

routers = APIRouter()
routers.include_router(contactRouter)