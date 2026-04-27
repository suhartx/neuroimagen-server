# 03 - Ejecución asíncrona

## Objetivo

Definir cómo se desacopla la recepción HTTP del procesamiento MRI, evitando que el tiempo de ejecución del algoritmo bloquee al cliente o degrade la API.

## Alcance

Incluye Redis, RQ, worker y transiciones de estado. No incluye scheduling avanzado ni reintentos inteligentes por política clínica.

## Decisiones técnicas

- Se adopta RQ por simplicidad operacional inicial.
- Redis SHALL almacenar mensajes de cola transitorios.
- El worker SHALL actualizar el estado en disco antes, durante y después del procesamiento.
- Para pruebas locales SHOULD existir un `QUEUE_MODE=inline` que evite depender de Redis real.

## Componentes afectados

- `app/services/queue.py`
- `app/workers/tasks.py`
- `app/workers/rq_worker.py`
- `worker/rq_worker.py`

## Contratos de entrada/salida

### Entrada

- `job_id` registrado previamente.

### Salida

- transición `queued -> running -> completed|failed`;
- metadatos de cola;
- resultado o error persistido.

## Supuestos

- El número de workers puede empezar en uno.
- El procesamiento es ejecutable por línea de comandos.
- La duración del job puede ser larga y variable.

## Riesgos

- cuelgues del procesador externo;
- reinicio del worker en mitad de tarea;
- divergencia entre Redis y estado en disco si se asumiera mal la autoridad.

## Criterios de aceptación

- Un job MUST poder crearse sin ejecutarse inline en producción.
- El estado MUST quedar reflejado en disco aunque Redis se reinicie.
- El modo inline MUST permitir pruebas básicas sin broker real.

## Pasos de validación

1. Crear job en modo `inline` y verificar finalización.
2. Crear job en modo `rq` con Redis activo.
3. Confirmar actualización de JSON antes y después de correr el wrapper.
