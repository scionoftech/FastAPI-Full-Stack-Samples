import strawberry
from typing import List, Optional
from strawberry.scalars import JSON


@strawberry.input
class UserInput:
    id: Optional[str] = strawberry.field(description="ID",
                                         default=None)
    first_name: Optional[str] = strawberry.field(
        description="First Name", default=None)
    last_name: Optional[str] = strawberry.field(
        description="Last name", default=None)
    full_name: Optional[str] = strawberry.field(
        description="full name", default=None)
    gender: Optional[str] = strawberry.field(description="gender",
                                             default=None)
    email: Optional[str] = strawberry.field(description="email",
                                            default=None)
    password: Optional[str] = strawberry.field(description="password",
                                               default=None)
    photo: Optional[str] = strawberry.field(description="photo",
                                            default=None)
    city: Optional[str] = strawberry.field(description="city",
                                           default=None)
    region: Optional[str] = strawberry.field(description="region",
                                             default=None)
    zip: Optional[int] = strawberry.field(description="zip",
                                          default=None)
    country: Optional[str] = strawberry.field(description="country",
                                              default=None)
    is_active: Optional[bool] = strawberry.field(
        description="is_active", default=None)
    is_superuser: Optional[bool] = strawberry.field(
        description="is_super", default=None)
    is_admin: Optional[bool] = strawberry.field(
        description="is_admin", default=None)
    created_by_userid: Optional[str] = strawberry.field(
        description="id", default=None)
    modified_by_userid: Optional[str] = strawberry.field(
        description="id", default=None)


@strawberry.type
class User:
    id: Optional[str] = strawberry.field(description="ID",
                                         default=None)
    first_name: Optional[str] = strawberry.field(
        description="First Name", default=None)
    last_name: Optional[str] = strawberry.field(
        description="Last name", default=None)
    full_name: Optional[str] = strawberry.field(
        description="full name", default=None)
    gender: Optional[str] = strawberry.field(description="gender",
                                             default=None)
    email: Optional[str] = strawberry.field(description="email",
                                            default=None)
    password: Optional[str] = strawberry.field(description="password",
                                               default=None)
    photo: Optional[str] = strawberry.field(description="photo",
                                            default=None)
    city: Optional[str] = strawberry.field(description="city",
                                           default=None)
    region: Optional[str] = strawberry.field(description="region",
                                             default=None)
    zip: Optional[int] = strawberry.field(description="zip",
                                          default=None)
    country: Optional[str] = strawberry.field(description="country",
                                              default=None)
    is_active: Optional[bool] = strawberry.field(
        description="is_active", default=None)
    is_superuser: Optional[bool] = strawberry.field(
        description="is_super", default=None)
    is_admin: Optional[bool] = strawberry.field(
        description="is_admin", default=None)
    created_by_userid: Optional[str] = strawberry.field(
        description="id", default=None)
    modified_by_userid: Optional[str] = strawberry.field(
        description="id", default=None)
    created_timestamp: Optional[str] = strawberry.field(
        description="datetime", default=None)
    modified_timestamp: Optional[str] = strawberry.field(
        description="datetime", default=None)
    deleted_timestamp: Optional[str] = strawberry.field(
        description="datetime", default=None)


@strawberry.type
class UsersLoginAttempt:
    id: Optional[str] = strawberry.field(description="ID",
                                         default=None)
    email: Optional[str] = strawberry.field(description="email",
                                            default=None)
    session_id: Optional[str] = strawberry.field(
        description="session_id", default=None)
    ip_address: Optional[str] = strawberry.field(
        description="ip_address", default=None)
    browser: Optional[str] = strawberry.field(description="browser",
                                              default=None)
    status: Optional[str] = strawberry.field(description="status",
                                             default=None)
    created_timestamp: Optional[str] = strawberry.field(
        description="created_timestamp", default=None)
    modified_timestamp: Optional[str] = strawberry.field(
        description="datetime", default=None)
    deleted_timestamp: Optional[str] = strawberry.field(
        description="datetime", default=None)


@strawberry.input
class ArticleInput:
    article_id: Optional[str] = strawberry.field(description="ID",
                                                 default=None)
    user_id: Optional[str] = strawberry.field(description="user_id",
                                              default=None)
    article_title: Optional[str] = strawberry.field(
        description="article_title",
        default=None)
    article_text: Optional[str] = strawberry.field(
        description="article_text",
        default=None)
    tags: Optional[JSON] = strawberry.field(
        description="article_text",
        default=None)


@strawberry.type
class Article:
    article_id: Optional[str] = strawberry.field(description="ID",
                                                 default=None)
    user_id: Optional[str] = strawberry.field(description="user_id",
                                              default=None)
    article_title: Optional[str] = strawberry.field(
        description="article_title",
        default=None)
    article_text: Optional[str] = strawberry.field(
        description="article_text",
        default=None)
    tags: Optional[JSON] = strawberry.field(
        description="article_text",
        default=None)
    created_timestamp: Optional[str] = strawberry.field(
        description="created_timestamp",
        default=None)
    modified_timestamp: Optional[str] = strawberry.field(
        description="modified_timestamp", default=None)
    deleted_timestamp: Optional[str] = strawberry.field(
        description="datetime", default=None)


@strawberry.type()
class ArticlePageData:
    """

    """
    page_num: int = strawberry.field(description="page num",
                                     default=None)
    record_count: int = strawberry.field(description="record count",
                                         default=None)
    record: List[Article] = strawberry.field(description="records",
                                             default=None)


@strawberry.type
class GetArticles:
    """

    """
    total_pages: int = strawberry.field(description="total pages",
                                        default=None)
    total_records: int = strawberry.field(description="total records",
                                          default=None)
    previous_page: int = strawberry.field(description="previous_page",
                                          default=None)
    next_page: int = strawberry.field(description="next page",
                                      default=None)
    has_previous: int = strawberry.field(description="has previous",
                                         default=None)
    has_next: int = strawberry.field(description="has next",
                                     default=None)
    page_data: int = strawberry.field(description="page data",
                                      default=None)


@strawberry.type
class UserLogin:
    access_token: Optional[str] = strawberry.field(
        description="access_token",
        default=None)
    token_type: Optional[str] = strawberry.field(
        description="token_type",
        default=None)
    session_id: Optional[str] = strawberry.field(
        description="session_id", default=None)
    user: Optional[User] = strawberry.field(description="user",
                                            default=None)
