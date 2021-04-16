from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, JSON, \
    Boolean, PrimaryKeyConstraint, UniqueConstraint, FLOAT
from datetime import datetime
import sys

sys.path.append("..")
from db.dbconf import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
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
    created_timestamp = Column(TIMESTAMP, nullable=False,
                               default=datetime.utcnow)
    modified_by_userid = Column(Integer, nullable=False)
    modified_timestamp = Column(TIMESTAMP, nullable=False,
                                default=datetime.utcnow)

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


class UsersLoginAttempt(Base):
    __tablename__ = "user_login_attempt"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    session_id = Column(String, nullable=False)
    ip_address = Column(String, nullable=True)
    browser = Column(String, nullable=True)
    status = Column(String, nullable=False)
    created_timestamp = Column(TIMESTAMP, nullable=False,
                               default=datetime.utcnow)

    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_login_attempt_pkey'),
        {"schema": "articles", 'extend_existing': True}
    )

    def __repr__(self):
        return f"UsersLoginAttempt('{self.id}','{self.user_id}','{self.session_id}" \
               f",'{self.ip_address},'{self.browser},'{self.status}," \
               f"'{self.created_timestamp}')"


class Article(Base):
    __tablename__ = "user_articles"

    article_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    article_title = Column(String, nullable=False)
    article_text = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)
    created_timestamp = Column(TIMESTAMP, nullable=False,
                               default=datetime.utcnow)
    modified_timestamp = Column(TIMESTAMP, nullable=False,
                                default=datetime.utcnow)
    __table_args__ = (
        PrimaryKeyConstraint('article_id', name='article_pkey'),
        {"schema": "articles", 'extend_existing': True}
    )

    def __repr__(self):
        return f"Article('{self.article_id}','{self.user_id}','{self.article_title}" \
               f",'{self.article_text},'{self.tags},'{self.created_timestamp}," \
               f"'{self.modified_timestamp}')"
