## Exploration: local-mri-processing-deployment

### Current State
The repository is effectively empty: only `openspec/config.yaml` and generated skill-registry metadata exist. There is no application code, no container setup, no API layer, no queue worker, no storage layout, and no existing integration for the MRI processor. The processor itself is assumed to already exist externally and MUST be invoked through a configurable command such as `PROCESSOR_COMMAND` or a stable wrapper like `processor/run_processor.py`.

### Affected Areas
- `openspec/config.yaml` — confirms this is a new/empty project with no detected stack, tests, or conventions.
- `openspec/changes/local-mri-processing-deployment/exploration.md` — exploration artifact for this change.
- `app/api/` — recommended FastAPI HTTP entrypoints for upload, job creation, status, and result download.
- `app/workers/` — recommended async job execution layer using Celery or RQ.
- `app/services/` — orchestration around storage, validation, job state, and processor invocation.
- `app/domain/` — request/result models and clinical-processing job rules.
- `storage/` — persistent local disk layout for uploads, job workdirs, outputs, and PDFs.
- `docker-compose.yml` — local deployment topology for API, Redis, worker, and mounted volumes.
- `Dockerfile` / `docker/` — reproducible container image and entrypoint scripts.
- `.env.example` — operator-configured settings including `PROCESSOR_COMMAND`, storage paths, and limits.

### Approaches
1. **Celery-based worker architecture** — FastAPI enqueues MRI processing jobs into Redis and Celery workers run the external processor command.
   - Pros: Mature retries/time limits, better job lifecycle primitives, easier future scaling to multiple workers, strong operational ecosystem.
   - Cons: More moving pieces and configuration than the project may need on day one.
   - Effort: Medium

2. **RQ-based worker architecture** — FastAPI enqueues jobs into Redis Queue and lightweight workers execute the external processor command.
   - Pros: Simpler setup, easier to understand in an empty project, good fit for local single-site deployment.
   - Cons: Weaker workflow/retry primitives than Celery, less ergonomic for richer scheduling and task policies.
   - Effort: Low

### Recommendation
Start with **RQ + FastAPI + Redis + mounted local disk**. This is the best build-now path because the project is empty and the real processor command is still unknown. The integration boundary should be a thin `ProcessorRunner` abstraction that accepts a configurable command template, a per-job working directory, and structured input/output paths; that keeps the clinical Python logic untouched while letting the platform be implemented immediately. Design the queue interface so Celery can replace RQ later without breaking the API contract if operational demands grow.

Recommended target architecture:
- **FastAPI**: synchronous control plane only — create job, inspect status, fetch artifacts, download PDF.
- **Redis**: broker plus lightweight transient job coordination.
- **RQ worker**: executes one job at a time per worker process, spawning the external processor command inside an isolated job workspace.
- **Persistent disk**: mounted volume such as `/data/neuroimagen/{job_id}/` with subfolders `input/`, `work/`, `output/`, `reports/`, `logs/`.
- **Metadata/state**: initial implementation can persist canonical job state on disk as JSON sidecars to avoid introducing a database before requirements exist; Redis remains non-source-of-truth.

Expected project structure under `/home/compneuro/Desktop/neuroimagen-server`:
- `app/main.py` — FastAPI app bootstrap.
- `app/api/routes/jobs.py` — create/status/result endpoints.
- `app/api/routes/health.py` — liveness/readiness endpoints.
- `app/core/config.py` — env-driven settings.
- `app/domain/jobs.py` — job/status/result models.
- `app/services/storage.py` — local filesystem layout and atomic writes.
- `app/services/validation.py` — upload/file validation and PDF safety checks.
- `app/services/processor_runner.py` — configurable external command launcher.
- `app/services/job_state.py` — disk-backed job metadata and idempotency handling.
- `app/workers/rq_worker.py` — queue bootstrap.
- `app/workers/tasks.py` — async processing task entrypoints.
- `processor/run_processor.py` — optional stable wrapper if the real processor command needs adaptation.
- `storage/.gitkeep` — mounted persistent root in local dev only.
- `docker-compose.yml` — api, redis, worker, shared volume.
- `Dockerfile` — single image reused by api and worker.
- `.env.example` — command, paths, queue, limits, logging knobs.
- `tests/` — API, service, and worker integration tests once implementation starts.

### Risks
- **Clinical data handling**: MRI files and derived PDFs may contain PHI/PII; local disk paths, backups, and logs MUST avoid leaking patient identifiers.
- **File validation**: accepting arbitrary uploads is dangerous; validate extension, MIME hints, size limits, and expected archive structure before invoking the processor.
- **Logging hygiene**: never log raw filenames, patient names, full paths, or command arguments if they embed identifiers; use job IDs and structured logs.
- **PDF result handling**: PDFs may be missing, malformed, duplicated, or too large; result publication MUST be explicit and only after successful completion checks.
- **Idempotency**: repeated uploads/retries can trigger duplicate processing; the API needs an idempotency key or deterministic content hash strategy plus collision policy.
- **Operational recovery**: Redis is not durable job history; source-of-truth state must survive container restarts on disk.
- **Process isolation**: external processor commands can hang, overuse RAM, or partially write outputs; enforce timeouts, exit-code handling, and atomic result promotion.
- **Permissions and retention**: local shared volumes can drift in ownership and fill up; retention and cleanup policies are mandatory for operations.

### Ready for Proposal
Yes — enough is known to write proposal/spec/design artifacts now. The proposal should lock the integration boundary around a configurable external processor command, choose RQ as the initial async backend with an explicit future migration path to Celery, and define disk-backed job state plus clinical-data safeguards as core scope.
