# El pipeline, paso a paso

Este ejemplo parte de dos requisitos: registrar usuarios y guardar sus datos. Todos los archivos son ejemplos inventados para explicar el proceso.

El recorrido es:

**Requisitos → propuesta de la IA → revisión → archivo PlantUML**

### Antes de empezar: preparar los requisitos

El programa lee los [requisitos originales](00_preparacion/req_final.jsonl) y los [ordena en un JSON](00_preparacion/input.json), conservando su texto y sus identificadores.

### 1. Pedir una propuesta a la IA

La IA recibe los requisitos, unas [instrucciones](01_generacion/instrucciones.txt), el [formato que debe seguir](01_generacion/architecture.schema.json) y un [ejemplo resuelto](01_generacion/demonstration.json).

Devuelve una [respuesta como esta](01_generacion/response.txt): propone un servicio de usuarios, un repositorio y una conexión entre ambos.

### 2. Leer la respuesta

El programa comprueba si puede leer la respuesta como JSON, un formato que organiza datos en campos y listas.

Si puede, obtiene el [candidato](02_parseo/candidate.json). Es la misma propuesta, ahora lista para revisarla.

### 3. Revisar la propuesta

Se comprueba que los campos estén completos, los identificadores no se repitan y las conexiones apunten a componentes existentes. También se revisa que los requisitos conserven su texto.

El campo `tracesTo` indica qué requisito pretende atender cada componente. Por ejemplo, `["REQ-01"]` lo asocia con el registro de usuarios. Esa asociación no prueba que el diseño resuelva bien el requisito.

Si cumple las reglas, se guarda un [reporte de aceptación](03_validacion/validation.json).

### 4. Crear el archivo del diagrama

El programa convierte la propuesta aceptada en [generated.puml](04_transformacion/generated.puml). Este archivo describe las cajas y las flechas del diagrama.

Aquí ya no interviene la IA. Después, PlantUML puede convertir ese archivo en una imagen.

### ¿Qué pasa si algo falla?

Se guarda el motivo y termina el intento, sin generar PlantUML. Puedes ver tres ejemplos:

- [Texto que no se puede leer como JSON](rechazos/parseo/response.txt).
- [Un campo con el tipo de dato equivocado](rechazos/esquema/response.json): `tracesTo` debería ser una lista.
- [Una conexión hacia un componente inexistente](rechazos/consistencia/response.json): aparece `CMP_99`, pero nadie lo declaró.

### Después: evaluar el resultado

La salida se compara con una [arquitectura de referencia](05_evaluacion/referencia_sintetica.puml). Esa referencia se usa solo al evaluar; no se entrega a la IA.

También se compara con una [salida directa de la IA en PlantUML](05_evaluacion/baseline.puml), llamada línea base, que omite el paso intermedio de JSON y validación.

Esta carpeta explica el recorrido. No contiene resultados de una evaluación real.
