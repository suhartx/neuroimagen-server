# 04 - Persistencia y almacenamiento

## Objetivo

Definir una estructura de almacenamiento local persistente que sea simple, auditable y suficientemente robusta para un sitio local sin base de datos relacional en esta primera etapa.

## Alcance

Incluye diseño de carpetas, estado JSON, artefactos de entrada/salida y criterios de escritura atómica. No incluye cifrado en reposo a nivel de volumen.

## Decisiones técnicas

- `data/` SHALL ser la raíz persistente.
- `data/state/jobs/` y `data/state/studies/` SHALL guardar JSON autoritativos.
- Las escrituras de estado SHALL ser atómicas mediante archivo temporal + replace.
- Los paths publicados por la API SHOULD ser relativos a `data/`.

## Componentes afectados

- `app/services/storage.py`
- `app/services/state.py`
- `data/`

## Contratos de entrada/salida

### Entrada

- bytes del estudio subido;
- cambios de estado de job;
- artefactos del procesador.

### Salida

- `data/inputs/<study_id>/study.ext`
- `data/outputs/<job_id>/...`
- `data/reports/<job_id>/report.pdf`
- `data/logs/<job_id>/processor.log`
- `data/state/studies/<study_id>.json`
- `data/state/jobs/<job_id>.json`

## Supuestos

- El volumen local es persistente y con espacio suficiente.
- La institución define luego política de retención.

## Riesgos

- saturación de disco;
- cambios manuales sobre `data/`;
- permisos inconsistentes entre host y contenedores.

## Criterios de aceptación

- Deben existir las carpetas persistentes mínimas requeridas.
- Cada estudio y job MUST tener un JSON recuperable.
- El job state MUST sobrevivir reinicios del stack.

## Pasos de validación

1. Subir un estudio y revisar `data/inputs/`.
2. Crear job y revisar `data/state/jobs/`.
3. Completar job y revisar `outputs`, `reports` y `logs`.
