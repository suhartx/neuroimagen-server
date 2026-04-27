from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "neuroimagen-server"
    host: str = "0.0.0.0"
    port: int = 8000
    redis_url: str = "redis://redis:6379/0"
    rq_queue_name: str = "mri-processing"
    queue_mode: str = "rq"
    processor_command: str = ""
    processor_wrapper_path: str = "processor/run_processor.py"
    processor_timeout_seconds: int = 1800
    max_upload_size_mb: int = 1024
    allowed_extensions_csv: str = Field(
        default=".nii,.nii.gz,.zip",
        validation_alias=AliasChoices("ALLOWED_EXTENSIONS", "ALLOWED_EXTENSIONS_CSV"),
    )
    storage_root: str = "data"
    generate_stub_pdf: bool = True
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        populate_by_name=True,
    )

    @property
    def project_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    def resolve_path(self, raw_path: str) -> Path:
        path = Path(raw_path)
        if path.is_absolute():
            return path
        return self.project_root / path

    @property
    def storage_root_path(self) -> Path:
        return self.resolve_path(self.storage_root)

    @property
    def inputs_path(self) -> Path:
        return self.storage_root_path / "inputs"

    @property
    def outputs_path(self) -> Path:
        return self.storage_root_path / "outputs"

    @property
    def reports_path(self) -> Path:
        return self.storage_root_path / "reports"

    @property
    def logs_path(self) -> Path:
        return self.storage_root_path / "logs"

    @property
    def state_path(self) -> Path:
        return self.storage_root_path / "state"

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024

    @property
    def allowed_extensions(self) -> set[str]:
        return {
            item.strip().lower()
            for item in self.allowed_extensions_csv.split(",")
            if item.strip()
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()
