# 06 - Seguridad básica y protección de datos

## Objetivo

Reducir exposición accidental de datos sensibles en una plataforma local de neuroimagen, aunque todavía no se implemente un esquema completo de autenticación, autorización o cifrado institucional.

## Alcance

Incluye validación de extensiones, control de tamaño, sanitización de logs y minimización de metadatos. No incluye IAM, LDAP, SSO ni cifrado transparente del volumen.

## Decisiones técnicas

- Los nombres originales de archivo SHOULD NOT persistirse en estado ni logs.
- Los logs MUST omitir contenido clínico y stdout/stderr crudos.
- La API MUST validar extensión y tamaño antes de persistir.
- Los reportes y outputs MUST quedar dentro de `data/` y no en rutas arbitrarias.

## Componentes afectados

- `app/services/validation.py`
- `app/services/processor_runner.py`
- `app/services/state.py`
- `docs/manual-operacion.md`

## Contratos de entrada/salida

### Entrada

- archivo cargado por operador;
- configuración del comando del procesador.

### Salida

- rechazo temprano de archivos no permitidos;
- logs sanitizados;
- metadatos operativos mínimos.

## Supuestos

- El despliegue corre en red interna y host administrado.
- El acceso físico/lógico al servidor está controlado por la institución.

## Riesgos

- fuga de PHI por script externo mal instrumentado;
- retención excesiva de archivos;
- permisos débiles del volumen compartido.

## Criterios de aceptación

- Los tests MUST cubrir rechazo de extensión inválida.
- El estado JSON MUST evitar nombres originales y contenido clínico.
- Los logs MUST registrar métricas técnicas, no contenido sensible.

## Pasos de validación

1. Intentar subir extensión no permitida.
2. Revisar JSON de estudio y job.
3. Revisar `processor.log` y confirmar que no haya stdout/stderr crudos.
