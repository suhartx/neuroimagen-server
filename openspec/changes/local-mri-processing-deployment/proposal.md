# Proposal: local-mri-processing-deployment

## Contexto

El repositorio estaba prácticamente vacío y el usuario solicitó una plataforma local Dockerizada completa para recepción y procesamiento de estudios MRI orientados a Neurorrehabilitación. El código clínico Python existente no debe reescribirse ni modificarse; la integración debe resolverse mediante un comando configurable y/o un wrapper estable.

## Problema

Actualmente no existe API, cola asíncrona, worker, almacenamiento persistente, trazabilidad de jobs ni documentación operativa. Eso impide montar un entorno local controlado donde el algoritmo clínico pueda ejecutarse sin acoplarse a una infraestructura ad hoc.

## Propuesta

Construir una base mínima robusta con:

- FastAPI para el plano de control.
- Redis + RQ para ejecución asíncrona.
- Estado autoritativo en JSON sobre disco.
- Estructura persistente en `data/`.
- Wrapper `processor/run_processor.py` que invoque `PROCESSOR_COMMAND` o stub local.
- Manual completo y documentos SDD en castellano.

## Alcance

### Incluye

- endpoints de salud, upload, creación de job, estado, resultado y reporte PDF;
- contenedorización local;
- pruebas básicas;
- documentación de operación y arquitectura.

### Excluye

- rediseño del procesador clínico existente;
- autenticación hospitalaria avanzada;
- base de datos relacional;
- validación clínica del algoritmo.

## Módulos afectados

- `app/`
- `worker/`
- `processor/`
- `data/`
- `docs/`
- `openspec/changes/local-mri-processing-deployment/`

## Riesgos

- datos sensibles expuestos por logs o scripts externos;
- crecimiento del almacenamiento local;
- comportamiento variable del procesador real;
- dependencia operacional excesiva del modo stub si no se completa integración real.

## Rollback plan

Si la integración real del procesador falla, la plataforma puede mantenerse en modo stub para pruebas locales mientras se ajusta `PROCESSOR_COMMAND`, sin cambiar la API ni la estructura de almacenamiento.
