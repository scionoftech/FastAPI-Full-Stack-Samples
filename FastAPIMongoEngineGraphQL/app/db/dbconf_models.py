import mongoengine_goodjson as gj
from datetime import datetime
from mongoengine import connect, StringField, DateTimeField,\
    BooleanField, IntField, ListField
import sys

sys.path.append("..")
from conf import DBSettings

session = connect(
    host=DBSettings.MONGODB_DATABASE_URL)


class User(gj.Document):
    # id = mongodb.StringField(max_length=120, unique=True, required=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    full_name = StringField(required=True)
    gender = StringField(required=True)

    email = StringField(required=True, unique=True)
    password = StringField(required=True)

    photo = StringField(required=False)
    city = StringField(required=False)
    region = StringField(required=False)
    zip = IntField(required=False)
    country = StringField(required=False)

    is_active = BooleanField(required=True)
    is_superuser = BooleanField(required=True)
    is_admin = BooleanField(required=True)

    created_by_userid = IntField(required=True)
    created_timestamp = DateTimeField(default=datetime.utcnow)
    modified_by_userid = IntField(required=True)
    modified_timestamp = DateTimeField(default=datetime.utcnow)

    meta = {'allow_inheritance': False,
            'collection': 'User',
            'auto_create_index': False,
            'indexes': [
                {
                    'fields': ['email']
                }]
            }

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


class UsersLoginAttempt(gj.Document):
    __tablename__ = "user_login_attempt"

    # id = StringField(required=True, index=True)
    email = StringField(required=True)
    session_id = StringField(required=True)
    ip_address = StringField(required=True)
    browser = StringField(required=True)
    status = StringField(required=True)
    created_timestamp = DateTimeField(default=datetime.utcnow)

    meta = {'allow_inheritance': False,
            'collection': 'UsersLoginAttempt',
            'auto_create_index': False,
            'indexes': [
                {
                    'fields': ['email']
                }]
            }

    def __repr__(self):
        return f"UsersLoginAttempt('{self.id}','{self.email}','{self.session_id}" \
               f",'{self.ip_address},'{self.browser},'{self.status}," \
               f"'{self.created_timestamp}')"


class Article(gj.Document):
    # article_id = StringField(primary_key=True, index=True)
    user_id = StringField(required=True)
    article_title = StringField(required=True)
    article_text = StringField(required=True)
    tags = ListField(required=False)
    created_timestamp = DateTimeField(default=datetime.utcnow)
    modified_timestamp = DateTimeField(default=datetime.utcnow)
    meta = {'allow_inheritance': False,
            'collection': 'Article',
            'auto_create_index': False,
            'indexes': [
                {
                    'fields': ['user_id']
                }]
            }

    def __repr__(self):
        return f"Article('{self.user_id}','{self.article_title}" \
               f",'{self.article_text},'{self.tags},'{self.created_timestamp}," \
               f"'{self.modified_timestamp}')"


# Log Model
class APILog(gj.Document):
    # id = Column(Integer, primary_key=True, index=True)
    name = StringField(required=True)
    log_level = IntField(required=True)
    log_level_name = StringField(required=True)
    method = StringField(required=True)
    args = StringField(required=True)
    module = StringField(required=True)
    func_name = StringField(required=True)
    line_no = StringField(required=True)
    exception_log = StringField(required=True)
    process = IntField(required=True)
    thread = StringField(required=True)
    thread_name = StringField(required=True)
    created_timestamp = DateTimeField(required=True)

    meta = {'allow_inheritance': False,
            'collection': 'APILog',
            'auto_create_index': False,
            'indexes': [
                {
                    'fields': ['func_name']
                }]
            }

    def __repr__(self):
        return f"ProcessLog('{self.name}','{self.log_level}'," \
               f"'{self.log_level_name}'),'{self.method}'," \
               f"'{self.args}','{self.module}','{self.func_name}'," \
               f"'{self.line_no}','{self.exception_log}','{self.process}'," \
               f"'{self.thread}','{self.thread_name}'," \
               f"'{self.created_timestamp}')"
