from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from app.core.config import get_settings
from app.domain.models import JobCreateRequest, JobCreateResponse, JobStateResponse, JobResultResponse
from app.services.queue import enqueue_process_job
from app.services.state import StateService
from app.services.storage import StorageService

router = APIRouter(tags=["jobs"])


@router.post("/jobs", response_model=JobCreateResponse, status_code=status.HTTP_202_ACCEPTED)
def create_job(request: JobCreateRequest) -> JobCreateResponse:
    settings = get_settings()
    state = StateService(settings)

    if not state.study_exists(request.study_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="study_id inexistente")

    job = state.create_job(
        study_id=request.study_id,
        source="api",
        parameters=request.parameters,
    )
    queue_info = enqueue_process_job(job["job_id"])
    state.attach_queue_metadata(job["job_id"], queue_info)
    current = state.get_job(job["job_id"])

    return JobCreateResponse(
        job_id=job["job_id"],
        study_id=request.study_id,
        status=current["status"],
    )


@router.get("/jobs/{job_id}", response_model=JobStateResponse)
def get_job(job_id: str) -> JobStateResponse:
    state = StateService(get_settings())
    job = state.get_job(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="job_id inexistente")
    return JobStateResponse(**job)


@router.get("/jobs/{job_id}/result", response_model=JobResultResponse)
def get_job_result(job_id: str) -> JobResultResponse:
    state = StateService(get_settings())
    job = state.get_job(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="job_id inexistente")
    if job["status"] != "completed":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="resultado aún no disponible")
    return JobResultResponse(job_id=job_id, study_id=job["study_id"], result=job.get("result", {}))


@router.get("/jobs/{job_id}/report")
def download_report(job_id: str):
    settings = get_settings()
    state = StateService(settings)
    storage = StorageService(settings)

    job = state.get_job(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="job_id inexistente")
    if job["status"] != "completed":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="reporte aún no disponible")

    report_path = storage.resolve_report_for_job(job)
    if not report_path or not report_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PDF final no encontrado")

    return FileResponse(path=report_path, media_type="application/pdf", filename=f"{job_id}.pdf")
