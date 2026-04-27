from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.jobs import router as jobs_router
from app.api.routes.studies import router as studies_router
from app.core.config import get_settings
from app.services.state import StateService
from app.services.storage import StorageService


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings = get_settings()
    storage = StorageService(settings)
    storage.ensure_base_directories()
    StateService(settings).ensure_structure()
    yield


settings = get_settings()
app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(health_router)
app.include_router(studies_router)
app.include_router(jobs_router)
