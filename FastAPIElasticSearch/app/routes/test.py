from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from app.db.dbconf import elastic_search
from app.util.helper import verify_api_key
from starlette import status
router = APIRouter()


@router.get("/test_elk")
def test_elk(request: Request):
    ai_api_key = request.headers.get('ai_api_key')
    if not verify_api_key(api_key=ai_api_key):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Credentials")
    res = elastic_search.test_connection()
    return JSONResponse(status_code=200, content={"ouput":str(res)})
