# from app.db import schemas
#
# {
#     400: {"model": schemas.Message, "description": "Bad Request"}
# }

base_responses = {
    400: {"description": "Bad Request"},
    401: {"description": "Unauthorized"},
    404: {"description": "Not Found"},
    422: {"description": "Validation Error"},
    500: {"description": "Internal Server Error"}
}

general_responses = {
    **base_responses,
    200: {
        "content": {
            "application/json": {
                "example": {"message": "success"}
            }
        },
    }
}

all_users_responses = {
    **base_responses,
    200: {
        "content": {
            "application/json": {
                "example": {"total_pages": 0,
                            "total_items": 0,
                            "page_data": {"page_num": 0,
                                          "items_count": 0,
                                          "items":
                                              [{
                                                  "id": 0,
                                                  "first_name": "string",
                                                  "last_name": "string"
                                                  , "full_name": "string",
                                                  "gender": "string",
                                                  "email": "string"
                                                  , "photo": "string"
                                                  , "city": "string",
                                                  "region": "string"
                                                  , "zip": "string",
                                                  "country": "string"
                                                  , "is_active": "string",
                                                  "is_superuser": "string"
                                                  , "is_admin": "string"
                                                  ,
                                                  "created_by_userid": "string"
                                                  ,
                                                  "created_timestamp": "string"
                                                  ,
                                                  "modified_by_userid": "string"
                                                  ,
                                                  "modified_timestamp": "string"}]}}
            }
        },
    }
}

get_token_response = {
    **base_responses,
    200: {
        "content": {
            "application/json": {
                "example": {"access_token": "string",
                            "token_type": "string"}
            }
        },
    }
}

login_response = {
    **base_responses,
    200: {
        "content": {
            "application/json": {
                "example": {"access_token": "string",
                            "token_type": "string",
                            "session_id": "string",
                            "user": {
                                "id": 0, "first_name": "string",
                                "last_name": "string"
                                , "full_name": "string", "gender": "string"
                                , "email": "string"
                                , "photo": "string"
                                , "city": "string", "region": "string"
                                , "zip": "string", "country": "string"
                                , "is_active": "string"
                                , "is_superuser": "string"
                                , "is_admin": "string"
                                , "created_by_userid": "string"
                                , "created_timestamp": "string"
                                , "modified_by_userid": "string"
                                , "modified_timestamp": "string"}}
            }
        },
    }
}

single_users_responses = {
    **base_responses,
    200: {
        "content": {
            "application/json": {
                "example": {
                    "id": 0, "first_name": "string",
                    "last_name": "string"
                    , "full_name": "string", "gender": "string"
                    , "email": "string"
                    , "photo": "string"
                    , "city": "string", "region": "string"
                    , "zip": "string", "country": "string"
                    , "is_active": "string", "is_superuser": "string"
                    , "is_admin": "string"
                    , "created_by_userid": "string"
                    , "created_timestamp": "string"
                    , "modified_by_userid": "string"
                    , "modified_timestamp": "string"}
            }
        },
    }
}