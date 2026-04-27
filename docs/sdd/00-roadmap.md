# 00 - Roadmap

## Objetivo

Definir una hoja de ruta realista para construir y evolucionar una plataforma local de procesamiento de resonancia magnética, priorizando seguridad operacional, integración no invasiva con el procesador Python existente y trazabilidad clínica mínima.

## Alcance

Incluye fases de infraestructura, API, asincronía, integración del procesador, persistencia, seguridad básica, pruebas y operación. No incluye validación clínica del algoritmo ni rediseño del código científico ya existente.

## Decisiones técnicas

- Fase 1: base mínima con FastAPI + Redis + RQ + disco local.
- Fase 2: integración del procesador por `PROCESSOR_COMMAND` y wrapper estable.
- Fase 3: robustez operacional con retención, observabilidad y endurecimiento.
- La fuente autoritativa del estado SHALL residir en JSON en disco.
- Redis SHOULD usarse solo como coordinación transitoria.

## Componentes afectados

- `app/`
- `worker/`
- `processor/`
- `data/`
- `docs/`
- `docker-compose.yml`

## Contratos de entrada/salida

### Entrada

- requerimientos funcionales del sitio local;
- script Python clínico existente;
- políticas operativas del hospital o laboratorio.

### Salida

- plataforma desplegable localmente;
- documentación de operación;
- contratos API y de integración;
- base de pruebas automatizadas.

## Milestones

### Milestone 1 — Fundación de plataforma

- estructura del repositorio;
- contenedores base;
- FastAPI con `GET /health`;
- layout persistente en `data/`;
- configuración por `.env`.

### Milestone 2 — Ingesta y validación

- `POST /studies/upload`;
- validación de extensión y tamaño;
- persistencia de estudio y metadatos mínimos;
- sanitización de logs.

### Milestone 3 — Ejecución asíncrona

- `POST /jobs`;
- Redis + RQ;
- worker dedicado;
- estados `queued`, `running`, `completed`, `failed`.

### Milestone 4 — Integración del procesador clínico

- wrapper `processor/run_processor.py`;
- soporte para `PROCESSOR_COMMAND`;
- variables de entorno y placeholders;
- manejo de timeout y códigos de salida.

### Milestone 5 — Resultados y reportes

- `GET /jobs/{job_id}`;
- `GET /jobs/{job_id}/result`;
- `GET /jobs/{job_id}/report`;
- recolección de PDF real o generación stub local.

### Milestone 6 — Operación segura

- manual técnico;
- troubleshooting;
- estrategia de limpieza/retención;
- endurecimiento de permisos y monitoreo básico.

## Supuestos

- El despliegue es local o en red interna controlada.
- El procesador real existe fuera de esta plataforma.
- El usuario operador puede preparar `.env` y montar volúmenes.
- Los formatos principales serán `.nii`, `.nii.gz` y `.zip`.

## Riesgos

- crecimiento descontrolado de almacenamiento;
- salida irregular del procesador real;
- PDFs ausentes o mal generados;
- reinicios de Redis confundidos con pérdida de estado;
- exposición accidental de PHI en logs o nombres de archivos.

## Criterios de aceptación

- La plataforma MUST arrancar localmente con Docker Compose.
- La API MUST permitir subir estudios, crear jobs y descargar PDF.
- El estado MUST quedar trazado en disco aunque Redis se reinicie.
- El procesador clínico MUST integrarse sin reescritura.
- La documentación MUST ser suficiente para un técnico hospitalario.

## Pasos de validación

1. Arrancar servicios locales.
2. Ejecutar `GET /health`.
3. Subir un estudio válido.
4. Crear un job.
5. Confirmar transición de estados.
6. Descargar PDF final.
7. Verificar existencia de JSON en `data/state/jobs/`.
