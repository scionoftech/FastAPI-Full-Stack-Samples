import strawberry
import uuid
from datetime import timedelta
from strawberry.types import Info
from typing import Union
from app.resolvers.crud_users import get_active_user
from app.resolvers.crud_login import check_username_password, \
    login_user
from app.resolvers.crud_users import get_user_id
from app.resolvers.crud_articles import get_article_s
from app.util.fragments import GetArticles
from app.util import schemas, scalars
from app.conf.config import ProjectSettings
from app.auth import access_token
from app.util.deps import jwt_and_error_handler


@strawberry.type
class Query:

    @strawberry.field
    async def login(self, info: Info, user_name: str = None,
                    userpw: str = None) -> Union[
        scalars.UserLogin, None]:
        db_user = await get_active_user(email=user_name)
        if db_user is None:
            raise ValueError("User not found")
        else:
            is_password_correct = await check_username_password(
                email=user_name,
                password=userpw)
            if is_password_correct is False:
                raise ValueError("Invalid Credentials")
            else:
                uid = str(uuid.uuid4().hex)
                user = schemas.UserLogIn(email=user_name)
                await login_user(user=user, session_id=uid)
                access_token_expires = timedelta(
                    minutes=int(ProjectSettings.ACCESS_TOKEN_EXPIRE_MINUTES))
                token = access_token.create_access_token(
                    data={"sub": user.email},
                    expires_delta=access_token_expires)
                user_data = await get_user_id(user_id=user_name)
                print(user_data)
                return scalars.UserLogin(access_token=token,
                                         token_type="Bearer",
                                         session_id=uid,
                                         user=user_data)

    @strawberry.field
    @jwt_and_error_handler
    async def get_articles(self, info: Info, tag: str = None,
                           article_id: str = None,
                           page_num: int = 1) -> GetArticles:

        return await get_article_s(tag=tag, article_id=article_id,
                                   page_num=page_num)
