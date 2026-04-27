from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.core.config import get_settings
from app.domain.models import StudyUploadResponse
from app.services.queue import enqueue_process_job
from app.services.state import StateService
from app.services.storage import StorageService
from app.services.validation import ValidationError, validate_extension, validate_upload_size

router = APIRouter(tags=["studies"])


@router.post("/studies/upload", response_model=StudyUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_study(
    file: UploadFile = File(...),
    enqueue_processing: bool = Form(False),
) -> StudyUploadResponse:
    settings = get_settings()
    storage = StorageService(settings)
    state = StateService(settings)

    try:
        extension = validate_extension(file.filename or "", settings.allowed_extensions)
        content = await file.read()
        validate_upload_size(len(content), settings.max_upload_size_bytes)
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    study = state.create_study(
        extension=extension,
        content_type=file.content_type,
        size_bytes=len(content),
    )
    storage.persist_study_upload(study["study_id"], extension, content)

    response_job_id = None
    if enqueue_processing:
        job = state.create_job(study_id=study["study_id"], source="upload")
        queue_info = enqueue_process_job(job["job_id"])
        state.attach_queue_metadata(job["job_id"], queue_info)
        response_job_id = job["job_id"]

    return StudyUploadResponse(
        study_id=study["study_id"],
        status="uploaded",
        enqueue_processing=enqueue_processing,
        job_id=response_job_id,
    )
