import json
from datetime import UTC, datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any
from uuid import uuid4

from app.core.config import Settings


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


class StateService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.jobs_dir = settings.state_path / "jobs"
        self.studies_dir = settings.state_path / "studies"

    def ensure_structure(self) -> None:
        self.jobs_dir.mkdir(parents=True, exist_ok=True)
        self.studies_dir.mkdir(parents=True, exist_ok=True)

    def _atomic_write_json(self, path: Path, payload: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile("w", delete=False, dir=path.parent, encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            temp_path = Path(handle.name)
        temp_path.replace(path)

    def _read_json(self, path: Path) -> dict[str, Any] | None:
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def create_study(self, *, extension: str, content_type: str | None, size_bytes: int) -> dict[str, Any]:
        self.ensure_structure()
        study_id = str(uuid4())
        payload = {
            "study_id": study_id,
            "extension": extension,
            "content_type": content_type,
            "size_bytes": size_bytes,
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "storage_path": f"inputs/{study_id}/study{extension}",
        }
        self._atomic_write_json(self.studies_dir / f"{study_id}.json", payload)
        return payload

    def study_exists(self, study_id: str) -> bool:
        return (self.studies_dir / f"{study_id}.json").exists()

    def get_study(self, study_id: str) -> dict[str, Any] | None:
        return self._read_json(self.studies_dir / f"{study_id}.json")

    def create_job(self, *, study_id: str, source: str, parameters: dict[str, Any] | None = None) -> dict[str, Any]:
        self.ensure_structure()
        job_id = str(uuid4())
        timestamp = now_iso()
        payload = {
            "job_id": job_id,
            "study_id": study_id,
            "status": "queued",
            "created_at": timestamp,
            "updated_at": timestamp,
            "source": source,
            "parameters": parameters or {},
            "queue": {},
            "result": {},
            "error": None,
        }
        self._atomic_write_json(self.jobs_dir / f"{job_id}.json", payload)
        return payload

    def attach_queue_metadata(self, job_id: str, queue_info: dict[str, Any]) -> dict[str, Any]:
        job = self.get_job(job_id)
        if not job:
            raise FileNotFoundError(f"job no encontrado: {job_id}")
        job["queue"] = queue_info
        job["updated_at"] = now_iso()
        self._atomic_write_json(self.jobs_dir / f"{job_id}.json", job)
        return job

    def update_job(self, job_id: str, **changes: Any) -> dict[str, Any]:
        job = self.get_job(job_id)
        if not job:
            raise FileNotFoundError(f"job no encontrado: {job_id}")
        job.update(changes)
        job["updated_at"] = now_iso()
        self._atomic_write_json(self.jobs_dir / f"{job_id}.json", job)
        return job

    def get_job(self, job_id: str) -> dict[str, Any] | None:
        return self._read_json(self.jobs_dir / f"{job_id}.json")
