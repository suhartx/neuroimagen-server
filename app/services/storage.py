from pathlib import Path

from app.core.config import Settings


class StorageService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def ensure_base_directories(self) -> None:
        for directory in [
            self.settings.inputs_path,
            self.settings.outputs_path,
            self.settings.reports_path,
            self.settings.logs_path,
            self.settings.state_path,
        ]:
            directory.mkdir(parents=True, exist_ok=True)

    def persist_study_upload(self, study_id: str, extension: str, content: bytes) -> Path:
        destination = self.settings.inputs_path / study_id / f"study{extension}"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
        return destination

    def resolve_study_input(self, study_record: dict) -> Path:
        return self.settings.storage_root_path / study_record["storage_path"]

    def job_output_dir(self, job_id: str) -> Path:
        path = self.settings.outputs_path / job_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    def job_reports_dir(self, job_id: str) -> Path:
        path = self.settings.reports_path / job_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    def job_logs_dir(self, job_id: str) -> Path:
        path = self.settings.logs_path / job_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    def default_report_path(self, job_id: str) -> Path:
        return self.job_reports_dir(job_id) / "report.pdf"

    def first_report_pdf(self, job_id: str) -> Path | None:
        reports_dir = self.job_reports_dir(job_id)
        pdfs = sorted(reports_dir.glob("*.pdf"))
        return pdfs[0] if pdfs else None

    def relative_to_storage(self, path: Path) -> str:
        return str(path.relative_to(self.settings.storage_root_path))

    def resolve_report_for_job(self, job_record: dict) -> Path | None:
        report_path = job_record.get("result", {}).get("report_path")
        if not report_path:
            return None
        return self.settings.storage_root_path / report_path
