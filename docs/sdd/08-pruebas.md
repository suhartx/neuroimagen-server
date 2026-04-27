# 08 - Pruebas

## Objetivo

Definir la estrategia mínima de pruebas para garantizar que la plataforma base funciona y que los contratos críticos no se rompen al integrar el procesador clínico.

## Alcance

Incluye pruebas básicas de API y validación sin Redis real, apoyadas en modo `inline`. No incluye pruebas de performance, fuzzing ni validación clínica del algoritmo MRI.

## Decisiones técnicas

- Pytest SHALL ser el runner de pruebas.
- La suite básica SHOULD evitar dependencia de Redis usando `QUEUE_MODE=inline`.
- Los casos mínimos MUST cubrir salud, validación de extensión y ciclo simple de job.

## Componentes afectados

- `tests/conftest.py`
- `tests/test_health.py`
- `tests/test_upload_validation.py`
- `tests/test_jobs.py`

## Contratos de entrada/salida

### Entrada

- cliente de pruebas FastAPI;
- archivos dummy de MRI;
- configuración temporal de almacenamiento.

### Salida

- confirmación de respuestas HTTP esperadas;
- confirmación de job completado;
- confirmación de PDF stub descargable.

## Supuestos

- El entorno de pruebas tiene Python y dependencias instaladas.
- El wrapper puede ejecutarse en modo stub.

## Riesgos

- poca cobertura sobre Redis real;
- poca cobertura sobre procesador clínico real;
- falsos positivos si el stub oculta problemas de integración externa.

## Criterios de aceptación

- `GET /health` MUST devolver 200.
- Subida con extensión inválida MUST devolver 400.
- Un job inline MUST completar y exponer resultado y PDF.

## Pasos de validación

1. Ejecutar `bash scripts/test.sh`.
2. Confirmar verde en los tres módulos de prueba.
3. Agregar más casos cuando se conecte el procesador real.
