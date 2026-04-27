import subprocess
import sys
import time
from pathlib import Path

from app.core.config import Settings


class ProcessorRunner:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def run(
        self,
        *,
        job_id: str,
        study_id: str,
        input_path: Path,
        output_dir: Path,
        reports_dir: Path,
        log_file: Path,
        state_file: Path,
    ) -> dict:
        wrapper_path = self.settings.resolve_path(self.settings.processor_wrapper_path)
        command = [
            sys.executable,
            str(wrapper_path),
            "--job-id",
            job_id,
            "--study-id",
            study_id,
            "--input-path",
            str(input_path),
            "--output-dir",
            str(output_dir),
            "--reports-dir",
            str(reports_dir),
            "--log-file",
            str(log_file),
            "--state-file",
            str(state_file),
        ]
        started = time.time()
        result = subprocess.run(
            command,
            cwd=self.settings.project_root,
            capture_output=True,
            text=True,
            timeout=self.settings.processor_timeout_seconds,
            check=False,
        )
        duration_seconds = round(time.time() - started, 3)

        log_file.parent.mkdir(parents=True, exist_ok=True)
        log_file.write_text(
            "\n".join(
                [
                    f"job_id={job_id}",
                    f"study_id={study_id}",
                    f"return_code={result.returncode}",
                    f"duration_seconds={duration_seconds}",
                    f"stdout_bytes={len(result.stdout.encode('utf-8', errors='ignore'))}",
                    f"stderr_bytes={len(result.stderr.encode('utf-8', errors='ignore'))}",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

        return {
            "return_code": result.returncode,
            "duration_seconds": duration_seconds,
        }
