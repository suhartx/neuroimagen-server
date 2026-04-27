# Tasks: local-mri-processing-deployment

## Phase 1: Infraestructura y configuración

- [x] 1.1 Crear `requirements.txt`, `Dockerfile`, `docker-compose.yml` y `.env.example`.
- [x] 1.2 Crear scripts operativos `scripts/start.sh`, `scripts/stop.sh` y `scripts/test.sh`.
- [x] 1.3 Crear layout persistente `data/inputs`, `data/outputs`, `data/reports`, `data/logs`, `data/state`.

## Phase 2: API y almacenamiento

- [x] 2.1 Implementar bootstrap FastAPI en `app/main.py`.
- [x] 2.2 Implementar `GET /health`.
- [x] 2.3 Implementar `POST /studies/upload` con validación de extensión y tamaño.
- [x] 2.4 Implementar persistencia de estudios y jobs en JSON sobre disco.

## Phase 3: Ejecución asíncrona

- [x] 3.1 Implementar cola con Redis + RQ y modo `inline` para pruebas.
- [x] 3.2 Implementar worker y tarea `process_job`.
- [x] 3.3 Implementar transiciones de estado `queued/running/completed/failed`.

## Phase 4: Integración del procesador

- [x] 4.1 Implementar `processor/run_processor.py` como wrapper estable.
- [x] 4.2 Soportar `PROCESSOR_COMMAND` con placeholders y variables de entorno.
- [x] 4.3 Implementar generación de PDF stub cuando el procesador real no lo produzca.

## Phase 5: API de resultados y documentación

- [x] 5.1 Implementar `GET /jobs/{job_id}` y `GET /jobs/{job_id}/result`.
- [x] 5.2 Implementar `GET /jobs/{job_id}/report`.
- [x] 5.3 Escribir `README.md` y `docs/manual-operacion.md` en castellano.
- [x] 5.4 Escribir los documentos SDD de `docs/sdd/`.

## Phase 6: Pruebas

- [x] 6.1 Agregar pruebas básicas de health.
- [x] 6.2 Agregar pruebas de validación de extensión.
- [x] 6.3 Agregar pruebas de creación de job y ciclo completo sin Redis real.
