from fastapi.security import OAuth2PasswordBearer
from jwt import exceptions
from jwt.utils import get_int_from_datetime
from datetime import datetime
from fastapi import Depends, HTTPException
from functools import wraps
from typing import Callable
from starlette import status
from fastapi import Request
from app.auth import access_token
from app.resolvers import crud_users
from app.util.schemas import TokenData, UserVerify
import logging
from app.conf import ProjectSettings

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{ProjectSettings.API_VERSION_PATH}/getToken")


def get_current_user(
        token: str = Depends(oauth2_scheme)) -> UserVerify:
    """ Verify User Authentication"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    expire_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="access expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    require_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="access denied",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token:
        try:
            payload = access_token.decode_access_token(token=token)
            token_validity = payload.get("exp")
            if get_int_from_datetime(
                    datetime.utcnow()) >= token_validity:
                raise expire_exception
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except exceptions.JWTException as e:
            logging.info("get_current_user")
            raise credentials_exception
        user = crud_users.verify_user(email=token_data.email)
        if user is None:
            raise credentials_exception
        return user
    else:
        raise require_exception


def jwt_and_error_handler(resolver) -> Callable:
    @wraps(resolver)
    async def wrapper(parent, info, *args, **kwargs) -> Callable:
        try:
            request: Request = info.context["request"]
            if "authorization" in request.headers.keys():
                bearer_token = request.headers.get("authorization",
                                                   "")
                if "Bearer" in bearer_token:
                    token = bearer_token.split(" ")[1]
                    result = await get_current_user(token=token)
                    if result is not None:
                        info.context["current_user"] = result
                        return await resolver(parent, info, *args,
                                              **kwargs)
                else:
                    raise ValueError("User is not authenticated")
            else:
                raise ValueError("User is not authenticated")

        except Exception as e:
            response = info.context["response"]
            error_message = str(e)
            if error_message in ["User not authenticated",
                                 "Invalid Credentials",
                                 " Could not validate credentials",
                                 "access expired", "access denied"]:
                status_code = 401
            else:
                status_code = 500
            response.status_code = status_code
            raise ValueError(error_message)
    return wrapper
