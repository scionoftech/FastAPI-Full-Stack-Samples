import uvicorn
from fastapi.responses import JSONResponse
from app.event_handler import app


# Root API
@app.get("/root", include_in_schema=False)
def root() -> JSONResponse:
    return JSONResponse(status_code=200,
                        content={
                            "message": "Welcome to Sample Server"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8088, log_level='debug')
