import uvicorn
from fastapi import Depends, Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.graphql import GraphQLApp
from graphene import Schema
import sys

sys.path.append("..")
from conf import ProjectSettings
from db import Query, Mutations
from routes import api_router
from util import deps, schemas

# REST API Settings
app = FastAPI(title=ProjectSettings.PROJECT_NAME,
              description=ProjectSettings.PROJECT_DESCRIPTION,
              version="1.0.0",
              # docs_url=None,
              # redoc_url=None,
              openapi_url=f"{ProjectSettings.API_VERSION_PATH}/openapi.json",
              docs_url=f"{ProjectSettings.API_VERSION_PATH}/docs",
              redoc_url=f"{ProjectSettings.API_VERSION_PATH}/redoc")
# Middleware Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=ProjectSettings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Routes
# app.include_router(api_router)


# app.add_route(f"{ProjectSettings.API_VERSION_PATH}/graphql", GraphQLApp(
#     schema=graphene.Schema(query=Query, mutation=Mutations)))

graphql_app = GraphQLApp(schema=Schema(query=Query, mutation=Mutations))


@app.api_route(f"{ProjectSettings.API_VERSION_PATH}/graphql",
               methods=["GET", "POST"])
async def graphql(request: Request, current_user: schemas.UserVerify = Depends(
    deps.get_current_user)):
    """
    FastAPI-GraphQL with JWT Authentication
    """
    return await graphql_app.handle_graphql(request=request)


app.include_router(api_router, prefix=ProjectSettings.API_VERSION_PATH)


# Root API
@app.get(ProjectSettings.API_VERSION_PATH, include_in_schema=False)
def root() -> JSONResponse:
    return JSONResponse(status_code=200,
                        content={
                            "message": "Welcome to Sample Server"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8088, log_level='debug')
