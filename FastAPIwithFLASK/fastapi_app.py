import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.responses import JSONResponse
from flask_app import flask_app

# REST API Settings
app = FastAPI(title="Sample",
              description="Sample API",
              version="1.0.0",
              # docs_url=None,
              # redoc_url=None,
              openapi_url="/api/v1/openapi.json",
              docs_url="/api/v1/docs",
              redoc_url="/api/v1/redoc")
# Middleware Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> JSONResponse:
    return JSONResponse(status_code=200,
                        content={
                            "message": "Hello World, This is FastAPI"})


# mount Flask API application with FastAPI Endpoint
# check at http://localhost:8088/flask_api/
app.mount(path="/flask_api", app=WSGIMiddleware(flask_app))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8088, log_level='debug')
