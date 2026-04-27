# Historial conversacional y técnico del proyecto

Este documento resume el historial disponible de trabajo sobre `neuroimagen-server`.

No es una transcripción literal completa del chat. Es un registro técnico reconstruido a partir de la conversación actual, resúmenes persistidos y decisiones guardadas durante el desarrollo.

## Estado inicial

El proyecto comenzó como una carpeta vacía orientada a crear una plataforma local Dockerizada para procesamiento de imágenes de resonancia magnética en contexto de neurorrehabilitación.

Desde el inicio se pidió:

- trabajar en castellano,
- documentar claramente el sistema,
- no reescribir ni modificar el procesador clínico Python existente,
- integrarlo mediante una capa envoltorio o comando configurable,
- preparar una base local ejecutable con Docker,
- dejar trazabilidad técnica mediante documentación SDD.

## Metodología usada

Se usó una metodología de desarrollo guiada por especificaciones, SDD —Spec-Driven Development—.

La idea fue no empezar directamente por código, sino dejar primero una estructura razonada:

- exploración del problema,
- propuesta técnica,
- especificaciones,
- diseño,
- tareas,
- implementación,
- documentación de operación.

Los artefactos principales quedaron en:

```txt
openspec/
docs/sdd/
```

## Decisiones principales

### Integración del procesador clínico

Se decidió integrar el procesador Python existente sin modificarlo.

Para eso se preparó una capa intermedia configurable mediante `PROCESSOR_COMMAND` y el wrapper:

```txt
processor/run_processor.py
```

Esto permite conectar el procesamiento real sin acoplar el servidor web directamente al código clínico.

### Servidor web/API

Se implementó una API con FastAPI.

Endpoints principales:

```txt
POST /studies/upload
GET  /jobs/{job_id}
GET  /jobs/{job_id}/result
GET  /jobs/{job_id}/report
```

La API permite subir un fichero, crear un estudio, encolar procesamiento y descargar el PDF generado cuando el trabajo termina.

### Procesamiento asíncrono

Se preparó una cola de trabajos con Redis y RQ.

Esto separa la subida del fichero del procesamiento pesado, evitando bloquear la API mientras se ejecuta el análisis.

### Persistencia actual

El estado actual se guarda en ficheros JSON sobre disco, bajo:

```txt
data/state/studies/
data/state/jobs/
```

También se prepararon carpetas para entradas, salidas, reportes y logs:

```txt
data/inputs/
data/outputs/
data/reports/
data/logs/
```

Esta persistencia es suficiente para una primera base local, pero no sustituye una base de datos real para uso multiusuario.

## Qué quedó implementado

Se creó una estructura completa de proyecto con:

- API FastAPI,
- cola Redis/RQ,
- worker de procesamiento,
- wrapper del procesador,
- almacenamiento en disco,
- generación o localización de PDF de reporte,
- Dockerfile,
- docker-compose.yml,
- scripts de arranque/parada/pruebas,
- tests base,
- documentación SDD,
- manual de operación,
- README en castellano.

## Qué no está implementado todavía

Todavía no existe:

- autenticación de usuarios,
- login,
- JWT o sesiones,
- separación de datos por usuario,
- panel web visual para usuarios finales,
- base de datos PostgreSQL/SQLite,
- modelo relacional de usuarios, estudios, trabajos y PDFs,
- auditoría clínica completa.

El sistema actual es una base backend/API para procesamiento local. Para convertirlo en una plataforma multiusuario real, esos puntos deben añadirse después.

## Estado de GitHub

El repositorio local se inicializó en Git y se subió a GitHub.

Commit inicial:

```txt
45b454d feat: scaffold neuroimagen server
```

Repositorio remoto:

```txt
https://github.com/suhartx/neuroimagen-server.git
```

Rama principal:

```txt
main
```

## Últimas aclaraciones conversadas

Se aclaró que:

- el sistema actual sí tiene una API para subir ficheros y descargar PDFs,
- no tiene todavía una interfaz web visual completa,
- no tiene autenticación de usuarios,
- no tiene base de datos relacional,
- el estado actual se guarda como JSON en disco,
- conviene documentar los siguientes pasos antes de seguir añadiendo funcionalidades.

Como resultado se creó también:

```txt
docs/tareas-pendientes.md
```

El primer punto de ese documento es probar lo que ya está hecho antes de implementar nuevas funcionalidades.

## Siguientes pasos recomendados

El orden recomendado es:

1. Probar manualmente la base actual.
2. Confirmar que Docker, subida, procesamiento y PDF funcionan.
3. Corregir errores detectados en pruebas.
4. Añadir base de datos real.
5. Añadir usuarios y autenticación.
6. Asociar estudios, jobs y PDFs a usuarios.
7. Crear interfaz web visual.
8. Reforzar auditoría, seguridad y pruebas.
