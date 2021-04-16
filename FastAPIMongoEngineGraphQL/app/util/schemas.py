from pydantic import BaseModel
from typing import List

# ---------------- login schemas -------------------- #
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    expire: str = None
    issue_time: str = None


# ---------------- login schemas -------------------- #
class UserBase(BaseModel):
    email: str


class UserVerify(UserBase):
    id: int


class UserCreate(UserBase):
    password: str
    first_name: str
    last_name: str
    full_name: str
    gender: str
    is_active: bool = True
    is_superuser: bool = False
    is_admin: bool = False
    created_by_userid: int


class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    full_name: str
    city: str
    country: str
    is_active: bool = True
    is_superuser: bool = False
    is_admin: bool = False
    modified_by_userid: int


class UserPasswordChange(BaseModel):
    password: str
    new_password: str


class UserAuthenticate(UserBase):
    password: str


class UserLogIn(UserBase):
    password: str
    account_id: str
    ip_address: str
    browser: str


class UserPasswordReset(BaseModel):
    token: str
    password: str


# return in response
class User(UserBase):
    id: int

    class Config:
        orm_mode = True


# Request body classes
class RedisRq(BaseModel):
    range_value: int


class ArticleCreate(BaseModel):
    user_id: str
    article_title: str
    article_text: str
    tags: List


class ArticleUpdate(BaseModel):
    user_id: str
    article_title: str
    article_text: str
    tags: List
