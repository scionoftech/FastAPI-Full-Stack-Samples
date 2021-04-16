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

check_status_response = {
    **base_responses,
    200: {
        "content": {
            "application/json": {
                "example": {"job_id": "string",
                            "job_status": "string"
                            }
            }
        },
    }
}

get_results_response = {
    **base_responses,
    200: {
        "content": {
            "application/json": {
                "example": {"job_id": "string",
                            "job_enqueued_at": "string",
                            "job_started_at": "string"}
            }
        },
    }
}
