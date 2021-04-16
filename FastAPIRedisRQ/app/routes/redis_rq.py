from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette import status
from rq.job import Job

import sys

sys.path.append("..")
from conf import RedisSettings
from util import response_schemas, schema, get_process_id
from util import redis_queue, redis_conn
from controller import some_long_function

router = APIRouter()


@router.post("/create_job", responses=response_schemas.general_responses)
def queue_test(redis_rq: schema.RedisRq) -> JSONResponse:
    """ Create a Job using redis rq """

    job = redis_queue.enqueue(some_long_function, jsonable_encoder(redis_rq),
                              job_id=get_process_id(),
                              job_timeout=RedisSettings.REDIS_JOB_TIMEOUT)

    if job is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success", "job_id": job.id})


@router.get("/check_status",
            responses=response_schemas.check_status_response)
def check_status(job_id: str) -> JSONResponse:
    """ Check Job Status"""

    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except Exception as exception:
        require_exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not found"
        )
        raise require_exception
    response = {"job_id": job.id, "job_status": job.get_status()}
    return JSONResponse(status_code=200, content=response)


@router.get("/results",
            responses=response_schemas.get_results_response)
def get_results(job_id: str) -> JSONResponse:
    """ Get Job Results"""

    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except Exception as exception:
        require_exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not found"
        )
        raise require_exception
    if not job.result:
        require_exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No result found for job_id {job.id}. Try checking the job's status."
        )
        raise require_exception

    return JSONResponse(status_code=200, content=job.result)
