# Manual de operación

## 1. Objetivo

Este manual describe cómo instalar, arrancar, operar y mantener `neuroimagen-server` en un entorno local controlado, pensado para equipos técnicos hospitalarios o de investigación clínica que necesiten procesar estudios de resonancia magnética sin exponer los datos a servicios externos.

## 2. Arquitectura operativa

- **FastAPI** expone la API de control.
- **Redis** actúa como broker de cola.
- **RQ Worker** consume tareas asíncronas.
- **Wrapper** `processor/run_processor.py` invoca el procesador real o ejecuta un stub.
- **Disco local** conserva entradas, salidas, reportes, logs y estado.

## 3. Carpetas relevantes

- `app/`: API, servicios y worker lógico.
- `worker/`: punto de entrada operacional del worker.
- `processor/`: ubicación esperada para montar o adaptar el código clínico existente.
- `data/inputs/`: estudios subidos.
- `data/outputs/`: artefactos producidos por el procesador.
- `data/reports/`: PDFs finales.
- `data/logs/`: logs sanitizados por job.
- `data/state/`: JSON autoritativos de estudios y jobs.

## 4. Instalación

### 4.1 Preparación

Ubicarse en:

```bash
cd /home/compneuro/Desktop/neuroimagen-server
```

Crear entorno:

```bash
cp .env.example .env
```

### 4.2 Configuración mínima

Editar `.env` y revisar:

- `QUEUE_MODE=rq`
- `REDIS_URL=redis://redis:6379/0`
- `PROCESSOR_COMMAND=`
- `ALLOWED_EXTENSIONS=.nii,.nii.gz,.zip`
- `MAX_UPLOAD_SIZE_MB=1024`
- `GENERATE_STUB_PDF=true`

## 5. Arranque y parada

### Arranque

```bash
cd /home/compneuro/Desktop/neuroimagen-server
bash scripts/start.sh
```

### Parada

```bash
cd /home/compneuro/Desktop/neuroimagen-server
bash scripts/stop.sh
```

## 6. Verificación de servicio

```bash
curl http://localhost:8000/health
```

Respuesta esperada:

```json
{"status":"ok","service":"neuroimagen-server","queue_mode":"rq"}
```

## 7. Carga de estudios

### Carga sin procesar todavía

```bash
curl -X POST "http://localhost:8000/studies/upload" \
  -F "file=@/ruta/estudio.nii.gz" \
  -F "enqueue_processing=false"
```

### Carga y encolado inmediato

```bash
curl -X POST "http://localhost:8000/studies/upload" \
  -F "file=@/ruta/estudio.nii.gz" \
  -F "enqueue_processing=true"
```

## 8. Gestión de jobs

### Crear job manualmente

```bash
curl -X POST "http://localhost:8000/jobs" \
  -H "Content-Type: application/json" \
  -d '{"study_id":"STUDY_ID","parameters":{"pipeline":"hospital-local"}}'
```

### Consultar estado

```bash
curl "http://localhost:8000/jobs/JOB_ID"
```

Estados previstos:

- `queued`
- `running`
- `completed`
- `failed`

### Consultar resultado

```bash
curl "http://localhost:8000/jobs/JOB_ID/result"
```

### Descargar PDF

```bash
curl -L "http://localhost:8000/jobs/JOB_ID/report" -o reporte.pdf
```

## 9. Integración del script Python real

### 9.1 Principio

El código clínico existente NO se reescribe. Se integra por borde estable.

### 9.2 Opción recomendada

Configurar en `.env`:

```env
PROCESSOR_COMMAND=python /app/processor/procesador_real.py --input {input_path} --output {output_dir} --reports {reports_dir}
```

### 9.3 Variables disponibles

- `JOB_ID`
- `STUDY_ID`
- `INPUT_PATH`
- `OUTPUT_DIR`
- `REPORTS_DIR`
- `LOG_FILE`
- `STATE_FILE`

### 9.4 Recomendación práctica

Si el procesador real requiere una firma más compleja, adaptalo dentro de `processor/` con un script fino que traduzca argumentos, pero NO toques la lógica clínica principal.

## 10. Errores frecuentes

### Archivo rechazado

Causas típicas:

- extensión no permitida;
- tamaño mayor al límite;
- archivo dañado o incompleto.

### Job en `failed`

Revisar:

- `data/logs/<job_id>/processor.log`
- valor de `PROCESSOR_COMMAND`
- permisos de `data/`

### Sin PDF final

- confirmar si el procesador real generó PDF en `data/reports/<job_id>/`;
- si no genera PDF y estás en pruebas, dejar `GENERATE_STUB_PDF=true`.

## 11. Logs

Los logs son deliberadamente sobrios:

- identificadores técnicos;
- códigos de salida;
- duración;
- tamaño de stdout/stderr.

No se debe registrar contenido clínico, nombres de pacientes, ni nombres originales de archivos.

## 12. Pruebas

Ejecutar desde la raíz del proyecto:

```bash
bash scripts/test.sh
```

Cobertura actual básica:

- `GET /health`
- validación de extensión
- creación de job y estado completo en modo inline, sin Redis real

## 13. Mantenimiento

- revisar crecimiento de `data/`;
- purgar estudios y reportes según política institucional;
- validar permisos del volumen compartido;
- monitorear jobs fallidos recurrentes;
- revisar compatibilidad del wrapper cuando cambie el procesador clínico.

## 14. Troubleshooting

### Redis no responde

- verificar contenedor `redis`;
- comprobar `REDIS_URL`;
- revisar si el worker inició correctamente.

### Worker no consume

- confirmar que `QUEUE_MODE=rq`;
- verificar contenedor `worker`;
- inspeccionar si el job quedó marcado `queued` en `data/state/jobs/`.

### Estado inconsistente

La fuente autoritativa es el JSON en disco, no Redis. Si Redis se reinicia, el historial de jobs permanece en `data/state/jobs/`.

## 15. Guía rápida para técnico hospitalario

1. Entrar a `/home/compneuro/Desktop/neuroimagen-server`.
2. Confirmar que `.env` esté correcto.
3. Ejecutar `bash scripts/start.sh`.
4. Probar `curl http://localhost:8000/health`.
5. Subir estudio con `curl` o con cliente HTTP institucional.
6. Anotar `study_id` y luego crear el job.
7. Consultar `GET /jobs/{job_id}` hasta ver `completed`.
8. Descargar el PDF final.
9. Si falla, revisar `data/logs/<job_id>/processor.log`.

## 16. Referencias internas

- `docs/sdd/`: documentación técnica de diseño.
- `openspec/changes/local-mri-processing-deployment/`: artefactos formales del cambio.
