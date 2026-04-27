# Spec: MRI local processing platform

## Requirement 1 — API básica de control

La plataforma MUST exponer endpoints para salud, carga de estudios, creación de jobs, consulta de estado, metadatos de resultado y descarga de PDF final.

### Scenario 1.1

**Given** un servicio recién iniciado  
**When** un operador consulta `GET /health`  
**Then** la API MUST responder `200` con estado `ok` y modo de cola configurado.

### Scenario 1.2

**Given** un estudio MRI válido  
**When** el operador ejecuta `POST /studies/upload`  
**Then** la plataforma MUST crear un `study_id` y persistir el archivo en almacenamiento local.

## Requirement 2 — Validación y protección básica

La plataforma MUST validar extensiones permitidas y tamaño máximo antes de aceptar archivos.

### Scenario 2.1

**Given** un archivo con extensión no permitida  
**When** el operador intenta subirlo  
**Then** la API MUST rechazarlo con error `400`.

## Requirement 3 — Ejecución asíncrona trazable

La plataforma MUST registrar cada job en disco y usar Redis/RQ solo como mecanismo transitorio de despacho.

### Scenario 3.1

**Given** un `study_id` existente  
**When** el operador crea un job  
**Then** la plataforma MUST generar `job_id`, marcarlo `queued` y conservar ese estado en JSON.

### Scenario 3.2

**Given** un worker operativo  
**When** el job es consumido  
**Then** el estado MUST transicionar a `running` y luego a `completed` o `failed`.

## Requirement 4 — Integración no invasiva del procesador

La plataforma SHALL integrar el código clínico existente mediante `PROCESSOR_COMMAND` y/o `processor/run_processor.py`, sin reescribir su lógica.

### Scenario 4.1

**Given** que `PROCESSOR_COMMAND` está vacío  
**When** se ejecuta un job local  
**Then** el wrapper MAY usar modo stub para producir salida mínima de prueba.

### Scenario 4.2

**Given** que `PROCESSOR_COMMAND` está configurado  
**When** el worker invoca el wrapper  
**Then** el comando MUST recibir rutas y metadatos operativos necesarios.

## Requirement 5 — Reporte PDF final

La plataforma MUST exponer un PDF final por job completado.

### Scenario 5.1

**Given** que el procesador real deja un PDF en `reports_dir`  
**When** el job termina  
**Then** la API MUST publicar ese PDF como reporte final.

### Scenario 5.2

**Given** que el procesador no dejó PDF y el modo stub está habilitado  
**When** el worker finaliza el job  
**Then** la plataforma MUST generar un PDF mínimo para validación local.
