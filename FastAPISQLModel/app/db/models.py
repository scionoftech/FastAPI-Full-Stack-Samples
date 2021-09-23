from typing import Optional, Dict
from sqlalchemy import Column, String, PrimaryKeyConstraint, UniqueConstraint, \
    TEXT, JSON
from sqlmodel import Field

from datetime import datetime
from sqlmodel import SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(primary_key=True, index=True)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    full_name: str = Field(nullable=False)
    gender: str = Field(nullable=False)

    email: str = Field(sa_column=Column(String, unique=True, nullable=False))
    password: str = Field(nullable=False)

    photo: str = Field(nullable=False)
    city: str = Field(nullable=False)
    region: str = Field(nullable=False)
    zip: Optional[int] = Field(nullable=False)
    country: str = Field(nullable=False)

    is_active: bool = Field(nullable=False)
    is_superuser: bool = Field(nullable=False)
    is_admin: bool = Field(nullable=False)

    created_by_userid: Optional[int] = Field(nullable=False)
    created_timestamp: datetime = Field(nullable=False,
                                        default=datetime.utcnow())
    modified_by_userid: Optional[int] = Field(nullable=False)
    modified_timestamp: datetime = Field(nullable=False,
                                         default=datetime.utcnow())

    __table_args__ = (PrimaryKeyConstraint('id', name='users_pkey'),
                      UniqueConstraint('email'),
                      {"schema": "articles", 'extend_existing': True}
                      )

    def __repr__(self):
        return f"User('{self.id}','{self.first_name}'" \
               f",'{self.first_name}'" \
               f",'{self.last_name}','{self.full_name}','{self.gender}'" \
               f",'{self.email}'" \
               f",'{self.photo}','{self.city}','{self.region}'" \
               f",'{self.zip}','{self.country}','{self.is_active}'" \
               f",'{self.is_superuser}','{self.is_admin}','" \
               f"{self.created_by_userid}'" \
               f",'{self.created_timestamp}','{self.modified_by_userid}'," \
               f"'{self.modified_timestamp}')"


class UsersLoginAttempt(SQLModel, table=True):
    __tablename__ = "user_login_attempt"

    id: Optional[int] = Field(primary_key=True, index=True)
    email: str = Field(nullable=False)
    session_id: str = Field(nullable=False)
    ip_address: str = Field(nullable=False)
    browser: str = Field(nullable=False)
    status: str = Field(nullable=False)
    created_timestamp: datetime = Field(nullable=False,
                                        default=datetime.utcnow())

    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_login_attempt_pkey'),
        {"schema": "articles", 'extend_existing': True}
    )

    def __repr__(self):
        return f"UsersLoginAttempt('{self.id}','{self.email}','{self.session_id}" \
               f",'{self.ip_address},'{self.browser},'{self.status}," \
               f"'{self.created_timestamp}')"


class Article(SQLModel, table=True):
    __tablename__ = "user_articles"

    article_id: str = Field(primary_key=True, index=True)
    user_id: str = Field(nullable=False)
    article_title: str = Field(nullable=False)
    article_text: str = Field(sa_column=Column(TEXT, nullable=False))
    tags: Dict = Field(sa_column=Column(JSON, nullable=False))
    created_timestamp: datetime = Field(nullable=False,
                                        default=datetime.utcnow())
    modified_timestamp: datetime = Field(nullable=False,
                                         default=datetime.utcnow())
    __table_args__ = (
        PrimaryKeyConstraint('article_id', name='article_pkey'),
        {"schema": "articles", 'extend_existing': True}
    )

    def __repr__(self):
        return f"Article('{self.article_id}','{self.user_id}','{self.article_title}" \
               f",'{self.article_text},'{self.tags},'{self.created_timestamp}," \
               f"'{self.modified_timestamp}')"
