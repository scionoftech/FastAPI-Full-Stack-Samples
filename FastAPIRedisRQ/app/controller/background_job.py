import time
from typing import Dict
from rq import get_current_job


def some_long_function(redis_rq: Dict):
    """An example function for redis queue."""
    job = get_current_job()
    print("Job started")
    time.sleep(redis_rq["range_value"])
    print("Job Completed")
    return {
        "job_id": job.id,
        "job_enqueued_at": job.enqueued_at.isoformat(),
        "job_started_at": job.started_at.isoformat()
    }
