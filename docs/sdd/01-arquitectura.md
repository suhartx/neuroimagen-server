# 01 - Arquitectura

## Objetivo

Describir la arquitectura objetivo para una plataforma local de procesamiento MRI con separación clara entre plano de control, ejecución asíncrona, integración clínica y persistencia operacional.

## Alcance

Aplica a la solución base local con FastAPI, Redis, RQ, wrapper de procesador y almacenamiento en disco. No cubre clúster distribuido ni balanceo multi-sitio.

## Decisiones técnicas

- La API SHALL ser FastAPI por simplicidad y velocidad de implementación.
- El backend asíncrono SHALL ser RQ por menor complejidad inicial que Celery.
- Redis SHALL actuar como broker, no como sistema de registro.
- La persistencia autoritativa SHALL estar en archivos JSON de estado y carpetas montadas en disco.
- El procesador real SHALL quedar aislado detrás de `processor/run_processor.py` y/o `PROCESSOR_COMMAND`.

## Componentes afectados

- `app/main.py`
- `app/api/routes/*`
- `app/services/*`
- `app/workers/*`
- `processor/run_processor.py`
- `worker/rq_worker.py`

## Vista lógica

1. Cliente sube estudio.
2. API valida y persiste el archivo.
3. API registra estudio y job en JSON.
4. API encola job en Redis/RQ.
5. Worker consume el job.
6. Worker ejecuta el wrapper del procesador.
7. Worker recolecta salidas y PDF.
8. Worker actualiza estado final en disco.
9. API expone estado y artefactos al operador.

## Contratos de entrada/salida

### Entrada

- archivo MRI válido;
- `study_id` existente para crear job;
- variables de entorno de operación.

### Salida

- JSON de estado por estudio y por job;
- directorios de salida y logs;
- PDF final descargable.

## Supuestos

- Un nodo local basta para la carga inicial.
- La concurrencia inicial es baja o moderada.
- El procesador puede ejecutarse por CLI.
- El volumen `data/` es persistente entre reinicios.

## Riesgos

- acople accidental con el procesador real;
- tareas demasiado pesadas para un único worker;
- registros no sanitizados;
- inconsistencia si el procesador escribe parcialmente.

## Criterios de aceptación

- La arquitectura MUST separar API, cola, worker y wrapper.
- Debe existir un borde estable para el procesador real.
- Debe ser posible reiniciar Redis sin perder historia clínica-operativa del job.

## Pasos de validación

1. Revisar que la API no invoque directamente lógica clínica compleja.
2. Confirmar que el worker use `ProcessorRunner`.
3. Confirmar que el job state viva en `data/state/jobs/*.json`.
4. Confirmar que los PDFs salgan de `data/reports/<job_id>/`.
