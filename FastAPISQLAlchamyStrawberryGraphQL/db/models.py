from sqlalchemy import Column, Integer, String, Text, JSON, \
    Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db import Base, Timestampedtable


class User(Timestampedtable, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    gender = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    photo = Column(String, nullable=False)
    city = Column(String, nullable=False)
    region = Column(String, nullable=False)
    zip = Column(Integer, nullable=False)
    country = Column(String, nullable=False)

    is_active = Column(Boolean, nullable=False)
    is_superuser = Column(Boolean, nullable=False)
    is_admin = Column(Boolean, nullable=False)

    created_by_userid = Column(Integer, nullable=False)
    modified_by_userid = Column(Integer, nullable=False)

    user_articles = relationship("Article", back_populates="users")

    def __repr__(self):
        return f"User('{self.id}','{self.client_id}','{self.first_name}'" \
               f",'{self.first_name}'" \
               f",'{self.last_name}','{self.full_name}','{self.gender}'" \
               f",'{self.email}'" \
               f",'{self.photo}','{self.city}','{self.region}'" \
               f",'{self.zip}','{self.country}','{self.is_active}'" \
               f",'{self.is_superuser}','{self.is_admin}','" \
               f"{self.created_by_userid}'" \
               f",'{self.created_timestamp}','{self.modified_by_userid}'," \
               f"'{self.modified_timestamp}')"


class UsersLoginAttempt(Timestampedtable, Base):
    __tablename__ = "user_login_attempt"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    session_id = Column(String, nullable=False)
    ip_address = Column(String, nullable=True)
    browser = Column(String, nullable=True)
    status = Column(String, nullable=False)

    def __repr__(self):
        return f"UsersLoginAttempt('{self.id}','{self.user_id}','{self.session_id}" \
               f",'{self.ip_address},'{self.browser},'{self.status}," \
               f"'{self.created_timestamp}')"


class Article(Timestampedtable, Base):
    __tablename__ = "user_articles"

    article_id = Column(String,primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    article_title = Column(String, nullable=False)
    article_text = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)

    users = relationship("User", back_populates="user_articles")

    def __repr__(self):
        return f"Article('{self.article_id}','{self.user_id}','{self.article_title}" \
               f",'{self.article_text},'{self.tags},'{self.created_timestamp}," \
               f"'{self.modified_timestamp}')"
