from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from enum import Enum
import sys

sys.path.append("..")
from util import deps, schemas, get_json
from crud import crud_users, crud_login, crud_base
from util import response_schemas

router = APIRouter()


class UserStatus(str, Enum):
    enable = "enable"
    disable = "disable"


@router.post("/", responses=response_schemas.general_responses)
def register_user(user: schemas.UserCreate) -> JSONResponse:
    """ Register A User"""
    data = crud_base.get_user(email=user.email)
    if data is not None:
        return JSONResponse(status_code=400,
                            content={"message": "email already registered"})
        # raise HTTPException(status_code=400,
        #                     detail="email already registered")
    data = crud_users.create_user(user=user)
    if data is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})


@router.put("/{user_id}", responses=response_schemas.general_responses)
def update_user(user_id: str, user: schemas.UserUpdate,
                current_user: schemas.UserVerify = Depends(
                    deps.get_current_user)) -> JSONResponse:
    """ Update A User"""

    data = crud_users.update_user(user_id=user_id, user=user)
    if data is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})


@router.put("/change_password/{user_id}",
            responses=response_schemas.general_responses,
            include_in_schema=False)
def update_password(user_id: str, user: schemas.UserPasswordChange,
                    current_user: schemas.UserVerify = Depends(
                        deps.get_current_user)) -> JSONResponse:
    """ Update User Password"""
    is_password_correct = crud_users.check_password(user_id=user_id,
                                                    password=user.password)
    if is_password_correct is False:
        return JSONResponse(status_code=400,
                            content={"message": "Invalid password"})

    data = crud_users.change_user_password(user_id=user_id,
                                           password=user.new_password)
    if data is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})

    return JSONResponse(status_code=200,
                        content={"message": "success"})


@router.put("/user_status/{user_id}",
            responses=response_schemas.general_responses)
def update_user_status(user_id: str, status: UserStatus = UserStatus.enable,
                       current_user: schemas.UserVerify = Depends(
                           deps.get_current_user)) -> JSONResponse:
    """ Update A User Status """

    data = crud_users.user_status_update(user_id=user_id, status=status)
    if data is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})


@router.delete("/{user_id}",
               responses=response_schemas.general_responses)
def delete_user(user_id: str, current_user: schemas.UserVerify = Depends(
    deps.get_current_user)) -> JSONResponse:
    """ Delete A User"""
    data = crud_users.delete_user(user_id=user_id)
    if data is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})


@router.get("/", responses=response_schemas.all_users_responses)
def get_users(user_id: str = None, page_num: int = 1,
              current_user: schemas.UserVerify = Depends(
                  deps.get_current_user)) -> JSONResponse:
    """ Return All Users"""
    if user_id is not None:
        db_user = crud_users.get_user_id(id=user_id)
        if db_user is None:
            return JSONResponse(status_code=500,
                                content={"message": "No User Found"})
        return JSONResponse(status_code=200,
                            content=db_user.to_json())
    else:
        db_user = crud_users.get_all_user(page_num=page_num)
        if db_user is None:
            return JSONResponse(status_code=500,
                                content={"message": "No Users Found"})
        return JSONResponse(status_code=200,
                            content={"total_pages": db_user.pages,
                                     "total_items": db_user.total_items,
                                     "page_data": {"page_num": page_num,
                                                   "item_count": db_user.page_size,
                                                   "items":
                                                       get_json(
                                                           db_user.items)}})
