from fastapi import APIRouter
from . import redis_rq
api_router = APIRouter()

# api_router.include_router(login.router, tags=["Login"])
api_router.include_router(redis_rq.router, prefix="/redis_rq", tags=["Redis rq"])
