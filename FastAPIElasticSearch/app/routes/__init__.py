from fastapi import APIRouter
from . import test

api_router = APIRouter()

api_router.include_router(test.router, tags=["Test"])
