import graphene
from graphql import GraphQLError
from datetime import timedelta
import uuid
import sys

sys.path.append("..")
from auth import access_token
from conf import ProjectSettings
from crud import crud_users, crud_articles, crud_base, crud_login
from db import SessionLocal as db
from util import schemas


class CreateUser(graphene.Mutation):
    """
    Create User Record
    """

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        full_name = graphene.String(required=True)
        gender = graphene.String(required=True)
        is_active = graphene.Boolean(required=True)
        is_superuser = graphene.Boolean(required=True)
        is_admin = graphene.Boolean(required=True)
        created_by_userid = graphene.Int(required=True)

    message = graphene.String()

    # user = graphene.Field(lambda: schemas.UserCreate)

    @staticmethod
    def mutate(root, info, email, password, first_name, last_name, full_name,
               gender, is_active, is_superuser, is_admin, created_by_userid):

        user = schemas.UserCreate(email=email, password=password,
                                  first_name=first_name,
                                  last_name=last_name, full_name=full_name,
                                  gender=gender, is_active=is_active,
                                  is_superuser=is_superuser, is_admin=is_admin,
                                  created_by_userid=created_by_userid)
        message = "success"
        db_user = crud_base.get_user(email=email, db=db)
        if db_user:
            raise GraphQLError("Email already registered")
        db_create = crud_users.create_user(user=user, db=db)
        if db_create is None:
            raise GraphQLError("Internal Server Error")
        return CreateUser(message=message)


class UpdateUser(graphene.Mutation):
    """
    Update User Record
    """

    class Arguments:
        user_id = graphene.Int(required=True)
        email = graphene.String(required=False)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)
        full_name = graphene.String(required=False)
        gender = graphene.String(required=False)
        is_active = graphene.Boolean(required=False)
        is_superuser = graphene.Boolean(required=False)
        is_admin = graphene.Boolean(required=False)
        created_by_userid = graphene.Int(required=False)

    message = graphene.String()

    # user = graphene.Field(lambda: schemas.UserCreate)

    @staticmethod
    def mutate(root, info, user_id, email, first_name, last_name, full_name,
               gender, is_active, is_superuser, is_admin, created_by_userid):

        update_user = schemas.UserUpdate(email=email,
                                         first_name=first_name,
                                         last_name=last_name,
                                         full_name=full_name,
                                         gender=gender, is_active=is_active,
                                         is_superuser=is_superuser,
                                         is_admin=is_admin,
                                         created_by_userid=created_by_userid)
        message = "success"
        db_user = crud_base.get_user(email=email, db=db)
        if db_user:
            raise GraphQLError("No User Found")
        db_update = crud_users.update_user(user_id=user_id, user=update_user,
                                           db=db)
        if db_update is None:
            raise GraphQLError("Internal Server Error")
        return CreateUser(message=message)


class UpdatePassword(graphene.Mutation):
    """
    Update User Password
    """

    class Arguments:
        user_id = graphene.Int(required=True)
        password = graphene.Int(required=True)
        new_password = graphene.String(required=False)

    message = graphene.String()

    # user = graphene.Field(lambda: schemas.UserCreate)

    @staticmethod
    def mutate(root, info, user_id, password, new_password):

        update_user = schemas.UserPasswordChange(password=password,
                                                 new_password=new_password)
        message = "success"
        is_password_correct = crud_users.check_password(user_id=user_id,
                                                        password=update_user.password,
                                                        db=db)
        if is_password_correct is False:
            raise GraphQLError("Invalid Old password")

        db_update = crud_users.change_user_password(user_id=user_id,
                                                    password=update_user.new_password,
                                                    db=db)
        if db_update is None:
            raise GraphQLError("Internal Server Error")
        return CreateUser(message=message)


class DeleteUser(graphene.Mutation):
    """
    Delete User Record
    """

    class Arguments:
        user_id = graphene.Int(required=True)

    message = graphene.String()

    @staticmethod
    def mutate(root, info, user_id):
        delete_user = schemas.UserDelete(user_id=user_id)
        message = "success"
        db_update = crud_users.delete_user(user_id=delete_user.user_id, db=db)
        if db_update is None:
            raise GraphQLError("Internal Server Error")
        return CreateUser(message=message)


class AuthUser(graphene.Mutation):
    """
    Authenticate user
    """

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        ip_address = graphene.String(required=True)
        browser = graphene.String(required=True)

    token = graphene.String()
    token_type = graphene.String()
    session_id = graphene.String()

    @staticmethod
    def mutate(root, info, email, password, ip_address, browser):
        db_user = crud_base.get_active_user(email=email, db=db)
        auth_user = schemas.UserLogIn(email=email,
                                      ip_address=ip_address,
                                      browser=browser)
        if db_user is None:
            raise GraphQLError("Email not existed")
        else:
            is_password_correct = crud_login.check_username_password(
                email=email,
                password=password,
                db=db)
            if is_password_correct is False:
                raise GraphQLError("Password is not correct")
            else:
                uid = str(uuid.uuid4().hex)
                crud_login.login_user(user=auth_user, session_id=uid, db=db)
                access_token_expires = timedelta(
                    minutes=ProjectSettings.ACCESS_TOKEN_EXPIRE_MINUTES)
                token = access_token.create_access_token(
                    data={"sub": auth_user.email},
                    expires_delta=access_token_expires)
                return AuthUser(token=token, token_type="Bearer",
                                session_id=uid)
