# neuroimagen-server

Plataforma local Dockerizada para recepción, encolado y procesamiento asíncrono de estudios de resonancia magnética orientados a Neurorrehabilitación, integrando un procesador Python clínico existente sin reescribirlo.

## Qué resuelve

- Expone una API REST con FastAPI.
- Encola procesamiento con Redis + RQ.
- Mantiene estado trazable en JSON sobre disco como fuente autoritativa.
- Guarda entradas, salidas, reportes, logs y estado en `data/`.
- Permite integrar el procesador real vía `PROCESSOR_COMMAND` o usando `processor/run_processor.py`.
- En modo local stub genera un PDF mínimo de prueba si el procesador real no produce uno.

## Arquitectura resumida

- **API**: FastAPI en `app/`.
- **Broker**: Redis.
- **Worker**: RQ ejecutando `app.workers.tasks.process_job`.
- **Integración clínica**: `processor/run_processor.py` como wrapper estable.
- **Persistencia**: disco local en `data/inputs`, `data/outputs`, `data/reports`, `data/logs`, `data/state`.

## Estructura principal

```text
/home/compneuro/Desktop/neuroimagen-server
├── app/
├── worker/
├── processor/
├── data/
├── docs/
├── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

## Requisitos

- Docker y Docker Compose.
- Python 3.11+ si querés correr pruebas locales fuera de contenedores.
- Un script/comando Python clínico existente si vas a reemplazar el modo stub.

## Configuración inicial

Desde `/home/compneuro/Desktop/neuroimagen-server`:

```bash
cp .env.example .env
```

Variables más importantes:

- `QUEUE_MODE=rq`: modo normal con Redis/RQ.
- `PROCESSOR_COMMAND=`: comando del procesador real. Si queda vacío, se usa stub.
- `ALLOWED_EXTENSIONS=.nii,.nii.gz,.zip`
- `MAX_UPLOAD_SIZE_MB=1024`
- `GENERATE_STUB_PDF=true`

## Comandos exactos

Ubicado en `/home/compneuro/Desktop/neuroimagen-server`:

### Arranque

```bash
bash scripts/start.sh
```

### Parada

```bash
bash scripts/stop.sh
```

### Pruebas básicas locales

```bash
bash scripts/test.sh
```

## Endpoints REST

- `GET /health`
- `POST /studies/upload`
- `POST /jobs`
- `GET /jobs/{job_id}`
- `GET /jobs/{job_id}/result`
- `GET /jobs/{job_id}/report`

## Flujo de uso

### 1. Subir estudio

```bash
curl -X POST "http://localhost:8000/studies/upload" \
  -F "file=@/ruta/al/estudio.nii.gz" \
  -F "enqueue_processing=false"
```

### 2. Crear job para un `study_id`

```bash
curl -X POST "http://localhost:8000/jobs" \
  -H "Content-Type: application/json" \
  -d '{"study_id":"REEMPLAZAR_STUDY_ID","parameters":{"pipeline":"local"}}'
```

### 3. Consultar estado

```bash
curl "http://localhost:8000/jobs/REEMPLAZAR_JOB_ID"
```

### 4. Consultar metadatos del resultado

```bash
curl "http://localhost:8000/jobs/REEMPLAZAR_JOB_ID/result"
```

### 5. Descargar PDF final

```bash
curl -L "http://localhost:8000/jobs/REEMPLAZAR_JOB_ID/report" -o reporte.pdf
```

## Integración del procesador Python real

El punto de integración NO toca el código clínico existente. Tenés dos caminos:

1. **Usar el wrapper estable** `processor/run_processor.py` y dejar que él invoque el procesador real.
2. **Configurar `PROCESSOR_COMMAND`** con placeholders.

Ejemplo:

```env
PROCESSOR_COMMAND=python /app/processor/mi_script_clinico.py --input {input_path} --output {output_dir} --reports {reports_dir}
```

Placeholders soportados:

- `{job_id}`
- `{study_id}`
- `{input_path}`
- `{output_dir}`
- `{reports_dir}`
- `{log_file}`
- `{state_file}`

Además, el wrapper exporta variables de entorno equivalentes (`JOB_ID`, `INPUT_PATH`, etc.) por si el script clínico ya espera ese formato.

## Logs y protección de datos

- Los logs guardan `job_id`, `study_id`, código de salida y tamaños de stdout/stderr.
- NO se persiste contenido de archivos subidos.
- NO se loguean nombres originales ni datos clínicos sensibles.

## Reportes PDF

- Si el procesador real deja un PDF en `data/reports/<job_id>/`, la API lo expone.
- Si no hay PDF y `GENERATE_STUB_PDF=true`, el worker genera uno mínimo de prueba.
- Ese PDF stub sirve solo para validación operativa local.

## Documentación

- Manual operativo: `docs/manual-operacion.md`
- SDD ampliado: `docs/sdd/`
- Artefactos OpenSpec del cambio: `openspec/changes/local-mri-processing-deployment/`

## Troubleshooting rápido

- Si `POST /jobs` queda sin procesar, verificá Redis y el contenedor `worker`.
- Si el job falla, revisá `data/logs/<job_id>/processor.log`.
- Si no aparece PDF, revisá `PROCESSOR_COMMAND` o dejá `GENERATE_STUB_PDF=true` para pruebas.
- Si el archivo se rechaza, confirmá extensión permitida y tamaño máximo.

## Estado del proyecto

Este repositorio ya incluye una base mínima robusta para desarrollo local hospitalario y para conectar el procesador clínico real sin rehacer su lógica.
