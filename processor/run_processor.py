import argparse
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile


def atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", delete=False, dir=path.parent, encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        temp_path = Path(handle.name)
    temp_path.replace(path)


def stub_result(args: argparse.Namespace) -> int:
    args.output_dir.mkdir(parents=True, exist_ok=True)
    metadata_path = args.output_dir / "result.json"
    atomic_write_json(
        metadata_path,
        {
            "job_id": args.job_id,
            "study_id": args.study_id,
            "mode": "stub",
            "message": "Procesamiento simulado para entorno local.",
        },
    )
    return 0


def external_result(args: argparse.Namespace, command_template: str) -> int:
    context = {
        "job_id": args.job_id,
        "study_id": args.study_id,
        "input_path": str(args.input_path),
        "output_dir": str(args.output_dir),
        "reports_dir": str(args.reports_dir),
        "log_file": str(args.log_file),
        "state_file": str(args.state_file),
    }
    formatted = command_template.format(**context)
    env = os.environ.copy()
    env.update(
        {
            "JOB_ID": args.job_id,
            "STUDY_ID": args.study_id,
            "INPUT_PATH": str(args.input_path),
            "OUTPUT_DIR": str(args.output_dir),
            "REPORTS_DIR": str(args.reports_dir),
            "LOG_FILE": str(args.log_file),
            "STATE_FILE": str(args.state_file),
        }
    )
    completed = subprocess.run(shlex.split(formatted), env=env, cwd=Path.cwd(), check=False)
    return completed.returncode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Wrapper estable para integración del procesador MRI existente")
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--study-id", required=True)
    parser.add_argument("--input-path", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--reports-dir", required=True, type=Path)
    parser.add_argument("--log-file", required=True, type=Path)
    parser.add_argument("--state-file", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.reports_dir.mkdir(parents=True, exist_ok=True)
    args.log_file.parent.mkdir(parents=True, exist_ok=True)

    command_template = os.getenv("PROCESSOR_COMMAND", "").strip()
    if not command_template:
        return stub_result(args)
    return external_result(args, command_template)


if __name__ == "__main__":
    sys.exit(main())
