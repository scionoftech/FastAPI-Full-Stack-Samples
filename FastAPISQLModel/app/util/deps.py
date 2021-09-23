from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jwt import exceptions
from jwt.utils import get_int_from_datetime
from datetime import datetime
from fastapi import Depends, HTTPException
from starlette import status
# import sys
#
# sys.path.append("..")
from app.auth import access_token
from app.db import session_scope
from app.crud import crud_users
from app.util.schemas import TokenData, UserVerify
from app.logs import fastapi_logger
from app.conf import ProjectSettings


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{ProjectSettings.API_VERSION_PATH}/getToken")


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(session_scope)) -> UserVerify:
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
            if get_int_from_datetime(datetime.utcnow()) >= token_validity:
                raise expire_exception
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except exceptions.JWTException as e:
            fastapi_logger.exception("get_current_user")
            raise credentials_exception
        user = crud_users.verify_user(email=token_data.email)
        if user is None:
            raise credentials_exception
        return user
    else:
        raise require_exception
