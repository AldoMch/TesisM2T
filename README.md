# Tesis M2T: piloto reproducible

Esta implementación está junto a `R2ABench`, sin modificar sus datos, scripts ni resultados. El primer hito implementado es local y no usa una API: leer un caso real, adaptarlo, validar un candidato controlado, transformarlo a PlantUML y ejecutar las métricas L1 reales del benchmark en un control de identidad.

## Hallazgos de la inspección

Los casos E-R2A de Java y Python usan una línea JSON por requisito en `req_final.jsonl`. Los campos observados son `req_id`, `requirement`, `source` y `category`; `source` contiene evidencia del SRS. Los diagramas `AD/ad.puml` usan `package`, `rectangle`, `database` y flechas dirigidas.

R2ABench L1 primero extrae un grafo PlantUML y requiere una alineación semántica de nodos para comparar una predicción con una referencia. Esa alineación puede venir de una caché válida o de un juez configurado. Por ello este proyecto solo crea una alineación de identidad para el control “archivo contra copia idéntica”; no es una alineación semántica aplicable a resultados generados.

## Ejecutar el piloto local

Desde la raíz del repositorio, usa Python 3.12 y las dependencias del benchmark más `jsonschema`:

```bash
python3 -m pip install -r requirements.txt
python3 -m src.prepare_requirements R2ABench/Dataset/E-R2A/JAVA/AI-DrivenTextAdventureGame/req_final.jsonl --out results/pilot/input.json
python3 -m src.create_controlled_candidate results/pilot/input.json --out results/pilot/controlled_candidate.json
python3 -m src.run_pipeline --requirements R2ABench/Dataset/E-R2A/JAVA/AI-DrivenTextAdventureGame/req_final.jsonl --candidate results/pilot/controlled_candidate.json --out results/pilot/proposal/run_01
```

`controlled_candidate.json` es un artefacto de prueba: conserva y enlaza todos los requisitos, pero no pretende ser una arquitectura de calidad. Sirve para probar el contrato sin ocultar una llamada a un modelo.

Para comprobar la interfaz estructural real de R2ABench contra una copia de la referencia, crea la copia fuera del benchmark y ejecuta:

```bash
cp R2ABench/Dataset/E-R2A/JAVA/AI-DrivenTextAdventureGame/AD/ad.puml results/pilot/reference_copy.puml
python3 -m src.evaluate_run --pred results/pilot/reference_copy.puml --reference R2ABench/Dataset/E-R2A/JAVA/AI-DrivenTextAdventureGame/AD/ad.puml --identity-alignment --parser-only --out results/pilot/identity_evaluation.json
```

El resultado esperado del control es `l1_structural_similarity: 100.0`. En `AI-DrivenTextAdventureGame`, las relaciones de referencia conectan contenedores y no entidades, por lo que el evaluador informa `l1_edge_f1: null`; no corresponde interpretarlo como una F1 de cero. `--parser-only` es explícito: la instalación actual no tiene un renderizador PlantUML configurado, así que L0 completo no puede afirmarse aún. Cuando configures `PLANTUML_CMD`, omite ese indicador para ejecutar el L0 real.

## Contrato y límites

El esquema está en `schemas/architecture.schema.json`. Además del esquema, el validador exige IDs únicos, conectores hacia componentes existentes, conservación exacta de IDs y textos de requisitos, trazas existentes y cobertura declarada de todos los requisitos preparados. La cobertura declarada no demuestra que el componente satisfaga el requisito; esa pertinencia se evalúa separadamente.

El transformador solo representa componentes, bases de datos, externos y relaciones. `layer` es opcional en el JSON y no se convierte en agrupamiento, por lo que este piloto no reclama comparar capas mediante L1.

## Ejecutar una llamada al modelo

El cliente usa el protocolo `/chat/completions` compatible con OpenAI. Configura `OPENAI_BASE_URL`, `OPENAI_MODEL` y `OPENAI_API_KEY` en tu entorno; la clave se usa para la solicitud y nunca se escribe en `results/`. Con el mismo caso y la misma demostración sintética, ejecuta una sola repetición de cada método:

```bash
python3 -m src.run_llm --method proposal --requirements R2ABench/Dataset/E-R2A/JAVA/AI-DrivenTextAdventureGame/req_final.jsonl --out results/pilot/AI-DrivenTextAdventureGame/proposal/run_01
python3 -m src.run_llm --method baseline --requirements R2ABench/Dataset/E-R2A/JAVA/AI-DrivenTextAdventureGame/req_final.jsonl --out results/pilot/AI-DrivenTextAdventureGame/baseline/run_01
```

La propuesta registra `input.json`, `request.json`, `response.txt`, y según avance, `candidate.json`, `parse.json`, `validation.json`, `generated.puml` y `metadata.json`. La línea base recibe los mismos requisitos y guarda su PlantUML directo. Después de obtener una alineación semántica válida del benchmark, usa `src.evaluate_run --alignment` para escribir `evaluation.json` sin repetir la generación.

## Verificación

```bash
python3 -m unittest discover -s tests -q
(cd R2ABench && python3 -m unittest discover -s evaluation_script/tests -q)
```

El siguiente paso, una vez revisado este piloto, es implementar el cliente LLM, guardar `request.json` y `response.txt` por intento, y comparar la propuesta con una línea base que reciba los mismos requisitos.
