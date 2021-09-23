import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# import sys
#
# sys.path.append("..")
from app.conf import ProjectSettings
from app.routes import api_router

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


app.include_router(api_router, prefix=ProjectSettings.API_VERSION_PATH)


# Server startup event
# @app.on_event("startup")
# def startup_event():
#     pass


# Root API
@app.get(ProjectSettings.API_VERSION_PATH, include_in_schema=False)
def root() -> JSONResponse:
    return JSONResponse(status_code=200,
                        content={
                            "message": "Welcome to Sample Server"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8088, log_level='debug')
