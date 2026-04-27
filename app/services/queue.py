from redis import Redis
from rq import Queue

from app.core.config import get_settings
from app.workers.tasks import process_job


def enqueue_process_job(job_id: str) -> dict:
    settings = get_settings()
    if settings.queue_mode == "inline":
        process_job(job_id)
        return {"mode": "inline", "queue_job_id": job_id}

    connection = Redis.from_url(settings.redis_url)
    queue = Queue(
        settings.rq_queue_name,
        connection=connection,
        default_timeout=settings.processor_timeout_seconds + 60,
    )
    job = queue.enqueue("app.workers.tasks.process_job", job_id, job_id=job_id, result_ttl=86400)
    return {"mode": "rq", "queue_job_id": job.id}
