from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from fastapi.responses import JSONResponse
from datetime import timedelta
from jwt import exceptions
from jwt.utils import get_int_from_datetime
from datetime import datetime
import uuid
from fastapi.security import OAuth2PasswordRequestForm
import sys

sys.path.append("..")
from crud import crud_login, get_user, get_active_user, crud_users
from util import deps, schemas, response_schemas, get_json
from auth import access_token
from conf import ProjectSettings
from util import send_reset_password_email

router = APIRouter()


# replace response_model=Token with custom responses
@router.post("/getToken",
             responses=response_schemas.get_token_response,
             include_in_schema=False)
def authenticate_user(
        form_data: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:
    """ Return Access Token"""
    db_user = get_active_user(email=form_data.username)
    if db_user is None:
        return JSONResponse(status_code=400,
                            content={"message": "Invalid Credentials"})
    else:
        is_password_correct = crud_login.check_username_password(
            email=form_data.username,
            password=form_data.password)
        if is_password_correct is False:
            return JSONResponse(status_code=400,
                                content={"message": "Invalid Credentials"})
        else:
            access_token_expires = timedelta(
                minutes=ProjectSettings.ACCESS_TOKEN_EXPIRE_MINUTES)
            token = access_token.create_access_token(
                data={"sub": form_data.username},
                expires_delta=access_token_expires)
            return JSONResponse(status_code=200,
                                content={"access_token": token,
                                         "token_type": "Bearer"})


@router.get("/refresh_token",
            responses=response_schemas.get_token_response,
            include_in_schema=False)
def new_token(old_token: str = None, session_id: str = None) -> JSONResponse:
    """ Return Access Token"""
    if old_token and session_id:
        payload = access_token.decode_access_token(token=old_token)
        email = payload.get("sub")

        db_session = crud_login.check_active_session(session_id=session_id)
        session_time = datetime.strptime(str(db_session.created_timestamp),
                                         "%Y-%m-%d %H:%M:%S.%f")

        diff = datetime.utcnow() - session_time

        limit = ProjectSettings.SESSION_TOKEN_EXPIRE_SECONDS  # 12 hours

        if email == db_session.email and (
                db_session.status == "logged_in" or db_session.status == "active") \
                and diff.seconds < limit:
            crud_login.active_user(session_id=session_id)
            access_token_expires = timedelta(
                minutes=ProjectSettings.ACCESS_TOKEN_EXPIRE_MINUTES)
            token = access_token.create_access_token(
                data={"sub": email},
                expires_delta=access_token_expires)
            return JSONResponse(status_code=200,
                                content={"access_token": token,
                                         "token_type": "Bearer"})
        else:
            return JSONResponse(status_code=400,
                                content={"message": "session ended"})
    else:
        return JSONResponse(status_code=400,
                            content={"message": "invalid token"})


# replace response_model=Token with custom responses
@router.post("/login",
             responses=response_schemas.login_response,
             include_in_schema=False)
def login_user(user: schemas.UserLogIn) -> JSONResponse:
    """ Login user and Return Access Token"""
    db_user = get_active_user(email=user.email)
    print(db_user)
    if db_user is None:
        return JSONResponse(status_code=400,
                            content={"message": "Invalid Credentials"})
    else:
        is_password_correct = crud_login.check_username_password(
            email=user.email,
            password=user.password)
        if is_password_correct is False:
            return JSONResponse(status_code=400,
                                content={"message": "Invalid Credentials"})
        else:
            uid = str(uuid.uuid4().hex)
            crud_login.login_user(user=user, session_id=uid)
            access_token_expires = timedelta(
                minutes=ProjectSettings.ACCESS_TOKEN_EXPIRE_MINUTES)
            token = access_token.create_access_token(
                data={"sub": user.email},
                expires_delta=access_token_expires)
            return JSONResponse(status_code=200,
                                content={"access_token": token,
                                         "token_type": "Bearer",
                                         "session_id": uid,
                                         "user": get_json(get_user(
                                             email=user.email))})


# replace response_model=Token with custom responses
@router.put("/logoff/{session_id}",
            responses=response_schemas.general_responses,
            include_in_schema=False)
def logoff_user(session_id: str) -> JSONResponse:
    """ Login user and Return Access Token"""
    db_session = crud_login.logoff_user(session_id=session_id)
    if db_session is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})


@router.post("/password_recovery",
             responses=response_schemas.general_responses,
             include_in_schema=False)
def recover_password(user: schemas.UserBase) -> JSONResponse:
    """
    Password Recovery
    """
    db_user = get_active_user(email=user.email)

    if db_user is None:
        return JSONResponse(status_code=404, content={
            "message": "The user with this email "
                       "does not exist in the system."})

    password_reset_token = access_token.generate_password_reset_token(
        email=user.email)
    send_reset_password_email(emails=[user.email],
                              password_reset_token=password_reset_token)
    return JSONResponse(status_code=200,
                        content={"message": "success"})


@router.post("/reset_password",
             responses=response_schemas.general_responses,
             include_in_schema=False)
def reset_password(reset_data: schemas.UserPasswordReset) -> JSONResponse:
    """
    Reset password
    """
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
    try:
        payload = access_token.verify_password_reset_token(
            token=reset_data.token)
        token_validity = payload.get("exp")
        if get_int_from_datetime(datetime.utcnow()) >= token_validity:
            raise expire_exception
        token_email: str = payload.get("sub")
        if token_email is None:
            raise credentials_exception
    except exceptions.JWTException as e:
        print(e)
        raise credentials_exception
    db_user = crud_users.verify_user(email=token_email)
    if db_user is None:
        raise credentials_exception

    data = crud_users.update_user_password(email=token_email,
                                           password=reset_data.password)
    if data is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})
