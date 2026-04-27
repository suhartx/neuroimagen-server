from app.core.config import get_settings
from app.services.pdf import generate_minimal_pdf
from app.services.processor_runner import ProcessorRunner
from app.services.state import StateService, now_iso
from app.services.storage import StorageService


def process_job(job_id: str) -> None:
    settings = get_settings()
    state = StateService(settings)
    storage = StorageService(settings)
    runner = ProcessorRunner(settings)

    job = state.get_job(job_id)
    if not job:
        raise FileNotFoundError(f"job inexistente: {job_id}")

    study = state.get_study(job["study_id"])
    if not study:
        state.update_job(job_id, status="failed", error="study asociado no encontrado")
        return

    state.update_job(job_id, status="running", error=None, started_at=now_iso())

    input_path = storage.resolve_study_input(study)
    output_dir = storage.job_output_dir(job_id)
    reports_dir = storage.job_reports_dir(job_id)
    log_file = storage.job_logs_dir(job_id) / "processor.log"
    state_file = settings.state_path / "jobs" / f"{job_id}.json"

    try:
        execution = runner.run(
            job_id=job_id,
            study_id=study["study_id"],
            input_path=input_path,
            output_dir=output_dir,
            reports_dir=reports_dir,
            log_file=log_file,
            state_file=state_file,
        )
        if execution["return_code"] != 0:
            state.update_job(
                job_id,
                status="failed",
                error=f"processor terminó con código {execution['return_code']}",
                finished_at=now_iso(),
            )
            return

        report_path = storage.first_report_pdf(job_id)
        if report_path is None and settings.generate_stub_pdf:
            report_path = storage.default_report_path(job_id)
            generate_minimal_pdf(
                report_path,
                title="Reporte local de prueba",
                lines=[
                    f"Job: {job_id}",
                    f"Study: {study['study_id']}",
                    "Este PDF fue generado por el modo stub local.",
                    "Reemplace PROCESSOR_COMMAND para usar el procesador clínico real.",
                ],
            )

        result = {
            "output_dir": storage.relative_to_storage(output_dir),
            "report_path": storage.relative_to_storage(report_path) if report_path else None,
            "log_path": storage.relative_to_storage(log_file),
            "completed_at": now_iso(),
            "processor_mode": "external" if settings.processor_command else "stub",
        }
        state.update_job(job_id, status="completed", result=result, finished_at=now_iso(), error=None)
    except Exception as exc:
        state.update_job(job_id, status="failed", error=str(exc), finished_at=now_iso())
