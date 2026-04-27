# 07 - Operación y mantenimiento

## Objetivo

Establecer lineamientos de operación cotidiana, soporte técnico y mantenimiento preventivo para la plataforma local.

## Alcance

Incluye arranque/parada, verificación de salud, monitoreo básico, análisis de fallos, limpieza y evolución controlada del entorno. No incluye observabilidad enterprise.

## Decisiones técnicas

- Docker Compose SHALL ser el mecanismo base de operación local.
- Los scripts `start.sh`, `stop.sh` y `test.sh` SHALL centralizar comandos frecuentes.
- El troubleshooting SHALL apoyarse en el estado en disco y logs por job.

## Componentes afectados

- `docker-compose.yml`
- `scripts/`
- `docs/manual-operacion.md`
- `data/`

## Contratos de entrada/salida

### Entrada

- acciones operativas del técnico;
- revisiones de logs y estado;
- actualización de `.env`.

### Salida

- sistema levantado o detenido;
- diagnóstico básico ante incidentes;
- ambiente listo para pruebas o uso local.

## Supuestos

- Existe personal técnico capaz de editar `.env` y correr comandos de shell.
- El host dispone de espacio, Docker y permisos sobre el volumen.

## Riesgos

- rotación manual insuficiente de artefactos;
- dependencia de conocimiento tribal;
- cambios en el procesador real sin actualizar el wrapper.

## Criterios de aceptación

- Debe existir un manual operativo en castellano.
- Deben existir comandos claros de arranque, parada y pruebas.
- Debe quedar documentado cómo inspeccionar jobs fallidos.

## Pasos de validación

1. Ejecutar scripts de arranque y parada.
2. Consultar `/health`.
3. Simular un fallo del procesador y revisar el log del job.
