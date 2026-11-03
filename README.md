# Tesis M2T: de requisitos a PlantUML

El proyecto genera un borrador de arquitectura de componentes a partir de requisitos. Usa los **17 proyectos de E-R2A** incluidos en R2ABench: **8 de JAVA y 9 de Python**. Las referencias del benchmark se utilizan únicamente en la revisión posterior.

La generación tiene cuatro fases. Solo la primera consulta a Gemini; las demás son algoritmos locales.

| Fase | Script | Entrada | Salida o fallo |
|---|---|---|---|
| 1. Generación | [fase1_generacion.py](fase1_generacion.py) | `req_final.jsonl` de cada proyecto E-R2A | `1_respuesta_llm_candidata.txt`; si falla la API, mensaje en consola |
| 2. Materialización | [fase2_parseo.py](fase2_parseo.py) | Respuesta textual de fase 1 | `2_candidato_materializado.json` o `reporte_de_errores.json` |
| 3. Validación | [fase3_validacion.py](fase3_validacion.py) | Candidato materializado | `3_modelo_validado.json` o `reporte_de_errores_fase3.json` |
| 4. Transformación M2T | [fase4_m2t.py](fase4_m2t.py) | Modelo aprobado en fase 3 | `4_codigo_final.puml`; si falla la transformación, mensaje en consola |

## Qué hace cada fase

**Fase 1.** Lee `req_id` y `requirement` de cada línea del JSONL y los envía como pares ID/texto. El prompt y una única demostración de entrada y salida están dentro del script: es una configuración *one-shot*. Usa `gemini-flash-latest`, temperatura `0.2` y salida solicitada como JSON. Guarda el texto recibido sin validarlo. La categoría y la evidencia `source` del JSONL no se envían, ni se incorpora el SRS completo. No lee `AD/ad.puml`.

Hace hasta tres intentos de llamada por proyecto, con esperas fijas de 10 segundos entre fallos, y una pausa de 5 segundos después de procesarlo. Son reintentos de API; no hay reparación guiada por errores de validación.

**Fase 2.** Elimina espacios exteriores y los delimitadores de un bloque Markdown JSON, si aparecen. Usa `json.loads()` para leer el texto y lo guarda con dos espacios de sangría. No corrige comas ni completa campos. Poder leerlo como JSON no acredita que cumpla el modelo arquitectónico.

**Fase 3.** Revisa las claves `requirements`, `components` y `connectors`, sus listas, los IDs y las referencias. Exige IDs únicos en requisitos y componentes; cada traza debe apuntar a un requisito declarado y cada extremo de conector a un componente existente. También exige cobertura declarada del 100 %: todos los requisitos del candidato deben aparecer en algún `tracesTo`.

Aquí R_A es el conjunto de requisitos declarados en el candidato. Esta fase no compara sus textos ni sus IDs con el archivo original del benchmark y no evalúa si las asociaciones son pertinentes. No utiliza JSON Schema.

**Fase 4.** Ordena componentes por ID y conectores por origen, destino y etiqueta. Limpia los IDs para obtener alias alfanuméricos y resuelve colisiones con sufijos numéricos. Emite una declaración `component` por componente y una flecha dirigida por conector, escapando los nombres. Para la etiqueta usa el primer campo de texto disponible entre `type`, `protocol`, `name` y `description`; si no hay ninguno, usa `relates_to`. `layer` y `responsibility` no se representan visualmente.

## Archivos por proyecto

```text
R2ABench/Dataset/E-R2A/
├── JAVA/<Proyecto>/req_final.jsonl
├── JAVA/<Proyecto>/AD/ad.puml
└── Python/<Proyecto>/...               # misma organización

salidas_evaluacion/
├── JAVA/
│   └── <Proyecto>/
│       ├── 1_respuesta_llm_candidata.txt
│       ├── 2_candidato_materializado.json
│       ├── 3_modelo_validado.json
│       ├── 4_codigo_final.puml
│       └── 4_codigo_final.svg         # solo si hay renderizador y se genera
└── Python/
    └── <Proyecto>/...                 # mismos nombres
```

Un rechazo en fase 2 genera `reporte_de_errores.json`; en fase 3, `reporte_de_errores_fase3.json`. Los artefactos posteriores pueden faltar. Un PlantUML antiguo puede seguir existiendo después de una revalidación fallida: el reporte lo identifica como histórico y lo excluye de los resultados aceptados.

## Ejecución

Desde la raíz, con Python 3.12:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-generation.txt
```

Configura `GEMINI_API_KEY` en `.env`, siguiendo [.env.example](.env.example), o en el entorno. Esa clave solo se necesita para la fase 1. El cliente Gemini se crea al importar ese script.

```bash
.venv/bin/python fase1_generacion.py
python3 fase2_parseo.py
python3 fase3_validacion.py
python3 fase4_m2t.py
```

Cada fase omite las salidas ya procesadas. La fase 2 y la fase 3 también omiten proyectos con su reporte de error; la fase 4 omite aquellos que no tienen modelo aprobado. Para aplicar reglas nuevas de fase 3 a resultados existentes:

```bash
python3 fase3_validacion.py --revalidar
```

La revalidación conserva el contenido de los candidatos que cumplen las reglas. Si uno deja de cumplirlas, elimina su antiguo `3_modelo_validado.json` y guarda el reporte de rechazo. No borra su PlantUML histórico.

## Revisión posterior y reporte

[fase5_reporte_validacion.py](fase5_reporte_validacion.py) recorre los proyectos definidos en E-R2A, incluso si les faltan salidas, y genera [RESULTADOS_VALIDACION_17_PROYECTOS.md](RESULTADOS_VALIDACION_17_PROYECTOS.md):

```bash
python3 fase5_reporte_validacion.py
```

Comprueba los delimitadores, declaraciones, alias y referencias del PlantUML generado, y contrasta su cantidad de componentes y conectores con el modelo. Reporta requisitos, componentes, conectores, cobertura declarada y conteos del diagrama de referencia, con medias y el número de casos disponibles. Incluye los rechazos.

Si encuentra `plantuml` en el sistema o un JAR indicado mediante `PLANTUML_JAR` o `--plantuml-jar`, intenta generar SVG. Si no lo encuentra, hace únicamente la revisión estructural y lo indica en el reporte. Se puede forzar esta última opción:

```bash
python3 fase5_reporte_validacion.py --sin-render
```

Los conteos GT incluyen `rectangle`, `component`, `database`, `package`, `node` e `interface`, desglosados en el reporte. Las relaciones se cuentan por declaración, distinguiendo dirigidas y no dirigidas; no se confunden las declaraciones de contenedores con componentes planos.

Esta revisión compara tamaños y detecta problemas técnicos. No calcula similitud arquitectónica L1 ni calidad semántica L2. Esas evaluaciones requieren las interfaces y configuraciones de [R2ABench/evaluation_script](R2ABench/evaluation_script/README.md). El benchmark se conserva sin cambios.

Las incidencias históricas de generación se describen en [REPORTE_GEMINI.md](REPORTE_GEMINI.md).
