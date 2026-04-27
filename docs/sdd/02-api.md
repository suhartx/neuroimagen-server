# 02 - API

## Objetivo

Definir la superficie REST mínima necesaria para ingesta de estudios, encolado de procesamiento, consulta de estado y descarga del reporte final.

## Alcance

Incluye endpoints HTTP locales y sus contratos de entrada/salida. No incluye autenticación fuerte ni versionado avanzado.

## Decisiones técnicas

- La API SHALL ser JSON para control y `multipart/form-data` para subida de archivos.
- Los IDs SHALL ser UUIDs.
- Los endpoints de resultado y PDF SHOULD devolver conflicto si el job aún no terminó.
- La API MUST evitar filtrar nombres originales de archivos y contenido clínico.

## Componentes afectados

- `app/api/routes/health.py`
- `app/api/routes/studies.py`
- `app/api/routes/jobs.py`
- `app/domain/models.py`

## Contratos de entrada/salida

### GET /health

- Entrada: ninguna.
- Salida: `{status, service, queue_mode}`.

### POST /studies/upload

- Entrada: `multipart/form-data` con `file` y `enqueue_processing` opcional.
- Salida: `{study_id, status, enqueue_processing, job_id?}`.

### POST /jobs

- Entrada: `{"study_id":"...","parameters":{...}}`.
- Salida: `{job_id, study_id, status}`.

### GET /jobs/{job_id}

- Entrada: `job_id`.
- Salida: estado completo del job con timestamps, cola, resultado y error.

### GET /jobs/{job_id}/result

- Entrada: `job_id`.
- Salida: metadatos del resultado si el job finalizó correctamente.

### GET /jobs/{job_id}/report

- Entrada: `job_id`.
- Salida: binario PDF.

## Supuestos

- Los clientes internos aceptan contratos simples.
- No hace falta streaming de subida en esta primera iteración.
- El archivo cabe dentro del límite definido por configuración.

## Riesgos

- archivos demasiado grandes cargados completamente en memoria;
- usos concurrentes intensivos sin tuning;
- intentos repetidos con `study_id` inexistente.

## Criterios de aceptación

- Todos los endpoints mínimos MUST existir.
- La subida MUST validar extensión y tamaño.
- `POST /jobs` MUST rechazar `study_id` inexistente.
- `GET /jobs/{job_id}/report` MUST entregar `application/pdf`.

## Pasos de validación

1. Ejecutar pruebas básicas.
2. Subir archivo válido y uno inválido.
3. Crear job con `study_id` correcto e incorrecto.
4. Descargar reporte de un job completado.
