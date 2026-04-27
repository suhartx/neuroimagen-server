# 05 - Integración del procesador Python

## Objetivo

Definir un borde de integración estable con el código Python clínico existente, preservando su autonomía y evitando reescrituras o modificaciones innecesarias.

## Alcance

Incluye `PROCESSOR_COMMAND`, wrapper `processor/run_processor.py`, placeholders, variables de entorno y tratamiento del modo stub. No cubre refactor clínico interno.

## Decisiones técnicas

- El procesador real SHALL integrarse por comando configurable.
- El wrapper SHALL ser el punto estable que la plataforma invoca siempre.
- El wrapper MAY ejecutar modo stub cuando no haya comando real configurado.
- Los parámetros de entrada y salida SHALL exponerse como placeholders y variables de entorno.

## Componentes afectados

- `processor/run_processor.py`
- `app/services/processor_runner.py`
- `.env.example`
- `docs/manual-operacion.md`

## Contratos de entrada/salida

### Entrada

- `job_id`
- `study_id`
- `input_path`
- `output_dir`
- `reports_dir`
- `log_file`
- `state_file`

### Salida

- código de retorno del proceso;
- artefactos en `output_dir`;
- opcionalmente PDF en `reports_dir`.

## Supuestos

- El procesador actual puede ejecutarse por CLI o envolverse mínimamente.
- El equipo clínico mantiene el algoritmo y esta plataforma solo lo orquesta.

## Riesgos

- scripts reales con firma inestable;
- uso de rutas absolutas rígidas;
- ausencia de PDF a pesar de completarse el análisis.

## Criterios de aceptación

- Debe ser posible operar con `PROCESSOR_COMMAND` vacío en modo stub.
- Debe ser posible reemplazar el stub por el procesador real sin tocar la API.
- La plataforma MUST recoger un PDF real si aparece en `reports_dir`.

## Pasos de validación

1. Ejecutar job con `PROCESSOR_COMMAND` vacío.
2. Confirmar salida stub y PDF local.
3. Configurar un comando real de prueba.
4. Verificar que el wrapper pase correctamente placeholders y variables.
