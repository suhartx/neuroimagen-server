# Tareas pendientes y siguientes pasos

Este documento recoge los próximos pasos recomendados para evolucionar `neuroimagen-server` desde la base actual hacia una plataforma multiusuario más completa.

## 1. Probar lo que ya está hecho

Antes de añadir nuevas funcionalidades, hay que validar la base actual:

- Levantar el entorno local con Docker Compose.
- Comprobar el endpoint de salud del servidor.
- Subir un fichero de prueba mediante `/studies/upload`.
- Verificar que se crea el `study_id`.
- Lanzar o encolar un procesamiento.
- Verificar el estado del `job_id`.
- Comprobar que el PDF se puede descargar desde `/jobs/{job_id}/report`.
- Revisar que los datos quedan guardados en `data/state/`, `data/inputs/`, `data/outputs/` y `data/reports/`.
- Documentar errores, límites o comportamientos inesperados antes de avanzar.

## 2. Añadir base de datos real

Actualmente el sistema guarda el estado en ficheros JSON sobre disco. Para una plataforma multiusuario conviene incorporar una base de datos, por ejemplo PostgreSQL.

Debería almacenar:

- usuarios,
- estudios subidos,
- trabajos de procesamiento,
- estado de cada trabajo,
- ubicación de ficheros de entrada,
- ubicación de PDFs generados,
- fechas relevantes,
- errores,
- metadatos clínicos o técnicos necesarios.

## 3. Añadir autenticación de usuarios

El servidor todavía no tiene login ni control de acceso.

Pendiente implementar:

- registro o alta controlada de usuarios,
- inicio de sesión,
- cierre de sesión,
- autenticación mediante JWT, sesiones u otro mecanismo seguro,
- protección de endpoints,
- separación de datos por usuario.

## 4. Asociar subidas, procesamientos y PDFs a cada usuario

Cada usuario debería poder ver únicamente sus propios estudios y resultados.

Relación esperada:

```txt
usuario -> estudios subidos -> trabajos de procesamiento -> PDFs generados
```

Esto requiere cambios en los modelos, la base de datos y los endpoints.

## 5. Crear una interfaz web para usuarios finales

Actualmente existe una API backend, pero no una interfaz visual completa.

Pendiente crear una web que permita:

- iniciar sesión,
- subir ficheros,
- ver el historial de estudios,
- consultar el estado de procesamiento,
- descargar PDFs,
- mostrar errores comprensibles.

## 6. Mejorar auditoría y trazabilidad

Por tratarse de un sistema orientado a datos clínicos/técnicos, conviene registrar eventos relevantes.

Ejemplos:

- quién subió cada fichero,
- cuándo se subió,
- qué procesamiento se ejecutó,
- cuándo terminó,
- dónde quedó el PDF,
- si hubo errores,
- qué versión del procesador se usó.

## 7. Endurecer seguridad y protección de datos

Pendiente revisar:

- permisos de acceso,
- límites de tamaño de subida,
- validación de formatos,
- almacenamiento de datos sensibles,
- limpieza de ficheros temporales,
- configuración de entorno,
- exposición de servicios en red local.

## 8. Ampliar pruebas automatizadas

Una vez validada manualmente la base actual, conviene reforzar las pruebas:

- tests de subida de ficheros,
- tests de cola de procesamiento,
- tests de descarga de PDF,
- tests de errores esperados,
- tests de autenticación cuando exista,
- tests de separación de datos por usuario.

## 9. Preparar despliegue operativo

Pendiente dejar claro cómo operar el sistema en una máquina real:

- comandos de arranque,
- parada segura,
- backups,
- restauración,
- actualización del código,
- rotación o limpieza de datos,
- revisión de logs.
