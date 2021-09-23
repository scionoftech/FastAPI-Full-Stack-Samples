from fastapi import APIRouter
from . import users
from . import login
from . import articles

api_router = APIRouter()

api_router.include_router(login.router, tags=["Login"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(articles.router, prefix="/articles",
                          tags=["Articles"])
