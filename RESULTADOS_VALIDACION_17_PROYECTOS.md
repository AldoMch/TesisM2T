# Resultados de validación: 17 proyectos E-R2A

Generado por `fase5_reporte_validacion.py` el 2026-11-02 16:54 (America/Lima).

## Resumen

- Proyectos E-R2A evaluados: **17**
- Modelos aceptados en la fase 3 (`3_modelo_validado.json`): **16/17**
- Modelos con Cobertura(R_A) = 100 %: **16/16**
- Archivos PlantUML estructuralmente válidos (incluidos históricos rechazados): **17/17**
- PlantUML renderizados a SVG: **n/d**
- Proyectos aceptados sin incidencias en esta revisión: **16/17**
- Renderizador: no disponible: solo se aplicó la validación estructural

## Tabla comparativa

| # | Lenguaje | Proyecto | Estado | \|R\| entrada | \|R_A\| | \|C\| | \|K\| | Cobertura(R_A) | Revisión estructural | Render SVG | Nodos GT | Relaciones GT | \|C\|/Nodos GT | \|K\|/Rel. GT |
|---:|---|---|---|---:|---:|---:|---:|---:|:---:|:---:|---:|---:|---:|---:|
| 1 | JAVA | AI-DrivenTextAdventureGame | ✅ OK | 16 | 16 | 11 | 18 | 100.0 % | ✅ | n/d | 25 | 10 | 0.44 | 1.80 |
| 2 | JAVA | AwesomeMusic | ❌ Rechazado F3 | 12 | — | — | — | — | ✅ histórico | — | 36 | 2 | — | — |
| 3 | JAVA | Campus_Helper | ✅ OK | 16 | 16 | 10 | 14 | 100.0 % | ✅ | n/d | 38 | 12 | 0.26 | 1.17 |
| 4 | JAVA | deepcode | ✅ OK | 22 | 22 | 14 | 25 | 100.0 % | ✅ | n/d | 46 | 21 | 0.30 | 1.19 |
| 5 | JAVA | ModelSharePlatform | ✅ OK | 20 | 20 | 14 | 25 | 100.0 % | ✅ | n/d | 18 | 2 | 0.78 | 12.50 |
| 6 | JAVA | POCD | ✅ OK | 14 | 14 | 13 | 15 | 100.0 % | ✅ | n/d | 33 | 4 | 0.39 | 3.75 |
| 7 | JAVA | SmartRecipe | ✅ OK | 21 | 21 | 11 | 17 | 100.0 % | ✅ | n/d | 20 | 4 | 0.55 | 4.25 |
| 8 | JAVA | TextAnnotationSystem | ✅ OK | 15 | 15 | 12 | 18 | 100.0 % | ✅ | n/d | 21 | 10 | 0.57 | 1.80 |
| 9 | Python | asp | ✅ OK | 11 | 11 | 13 | 14 | 100.0 % | ✅ | n/d | 24 | 28 | 0.54 | 0.50 |
| 10 | Python | easylatex | ✅ OK | 9 | 9 | 8 | 11 | 100.0 % | ✅ | n/d | 22 | 3 | 0.36 | 3.67 |
| 11 | Python | eivas | ✅ OK | 9 | 9 | 7 | 10 | 100.0 % | ✅ | n/d | 38 | 5 | 0.18 | 2.00 |
| 12 | Python | Indoor_Fitness_App | ✅ OK | 8 | 8 | 8 | 12 | 100.0 % | ✅ | n/d | 29 | 10 | 0.28 | 1.20 |
| 13 | Python | labhire | ✅ OK | 8 | 8 | 9 | 16 | 100.0 % | ✅ | n/d | 40 | 3 | 0.23 | 5.33 |
| 14 | Python | modelevolution | ✅ OK | 10 | 10 | 9 | 10 | 100.0 % | ✅ | n/d | 14 | 10 | 0.64 | 1.00 |
| 15 | Python | mytorch | ✅ OK | 11 | 11 | 10 | 14 | 100.0 % | ✅ | n/d | 53 | 4 | 0.19 | 3.50 |
| 16 | Python | prompthub | ✅ OK | 10 | 10 | 10 | 17 | 100.0 % | ✅ | n/d | 51 | 5 | 0.20 | 3.40 |
| 17 | Python | retool | ✅ OK | 10 | 10 | 7 | 10 | 100.0 % | ✅ | n/d | 19 | 5 | 0.37 | 2.00 |
| | | **Promedio** | | 13.1 | 13.1 | 10.4 | 15.4 | 100.0 % | | | 31 | 8.1 | 0.39 | 3.07 |

## Estadísticas descriptivas

| Métrica | n | Media | Mediana | Mín. | Máx. |
|---|---:|---:|---:|---:|---:|
| \|R_A\| (requisitos del modelo) | 16 | 13.1 | 11.0 | 8.0 | 22.0 |
| \|C\| (componentes generados) | 16 | 10.4 | 10.0 | 7.0 | 14.0 |
| \|K\| (conectores generados) | 16 | 15.4 | 14.5 | 10.0 | 25.0 |
| Cobertura(R_A) % | 16 | 100.0 | 100.0 | 100.0 | 100.0 |
| Nodos GT | 17 | 31.0 | 29.0 | 14.0 | 53.0 |
| Relaciones GT | 17 | 8.1 | 5.0 | 2.0 | 28.0 |
| \|C\| / Nodos GT | 16 | 0.39 | 0.37 | 0.18 | 0.78 |
| \|K\| / Relaciones GT | 16 | 3.07 | 2.00 | 0.50 | 12.50 |

## Desglose del Ground Truth (`AD/ad.puml`)

| Proyecto | `rectangle` | `component` | `database` | `package` | `node` | `interface` | **Nodos** | `-->` | `..>` | `--` | `..` | **Relaciones** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| AI-DrivenTextAdventureGame | 19 | 0 | 1 | 5 | 0 | 0 | **25** | 5 | 0 | 0 | 5 | **10** |
| AwesomeMusic | 33 | 0 | 2 | 1 | 0 | 0 | **36** | 2 | 0 | 0 | 0 | **2** |
| Campus_Helper | 27 | 0 | 1 | 8 | 2 | 0 | **38** | 5 | 0 | 2 | 5 | **12** |
| deepcode | 31 | 0 | 2 | 13 | 0 | 0 | **46** | 7 | 0 | 0 | 14 | **21** |
| ModelSharePlatform | 8 | 0 | 6 | 4 | 0 | 0 | **18** | 2 | 0 | 0 | 0 | **2** |
| POCD | 27 | 0 | 0 | 6 | 0 | 0 | **33** | 4 | 0 | 0 | 0 | **4** |
| SmartRecipe | 12 | 0 | 2 | 6 | 0 | 0 | **20** | 4 | 0 | 0 | 0 | **4** |
| TextAnnotationSystem | 15 | 0 | 0 | 6 | 0 | 0 | **21** | 3 | 7 | 0 | 0 | **10** |
| asp | 7 | 14 | 3 | 0 | 0 | 0 | **24** | 28 | 0 | 0 | 0 | **28** |
| easylatex | 6 | 13 | 3 | 0 | 0 | 0 | **22** | 3 | 0 | 0 | 0 | **3** |
| eivas | 25 | 0 | 1 | 12 | 0 | 0 | **38** | 5 | 0 | 0 | 0 | **5** |
| Indoor_Fitness_App | 25 | 0 | 0 | 4 | 0 | 0 | **29** | 2 | 2 | 6 | 0 | **10** |
| labhire | 28 | 0 | 4 | 8 | 0 | 0 | **40** | 3 | 0 | 0 | 0 | **3** |
| modelevolution | 8 | 0 | 2 | 4 | 0 | 0 | **14** | 10 | 0 | 0 | 0 | **10** |
| mytorch | 35 | 0 | 2 | 16 | 0 | 0 | **53** | 4 | 0 | 0 | 0 | **4** |
| prompthub | 13 | 0 | 1 | 0 | 37 | 0 | **51** | 4 | 1 | 0 | 0 | **5** |
| retool | 14 | 0 | 3 | 0 | 0 | 2 | **19** | 5 | 0 | 0 | 0 | **5** |
| **Promedio** | 19.6 | 1.6 | 1.9 | 5.5 | 2.3 | 0.1 | 31.0 | 5.6 | 0.6 | 0.5 | 1.4 | 8.1 |

## Incidencias

- **JAVA/AwesomeMusic** (❌ Rechazado F3):
  - El id de requisito 'AwesomeMusic-R008' está duplicado en requirements.
  - `4_codigo_final.puml` existe, pero se descarta porque su modelo fue rechazado.

## Definiciones

- **\|R\| entrada**: líneas de `req_final.jsonl` del dataset (requisitos que recibió el LLM).
- **\|R_A\|**: IDs únicos de requisitos en `3_modelo_validado.json`. Debe coincidir con \|R\| entrada.
- **\|C\| / \|K\|**: componentes y conectores del modelo validado.
- **Cobertura(R_A)** = \|{r ∈ R_A : ∃ c ∈ C, r ∈ c.tracesTo}\| / \|R_A\| × 100. Es una cobertura *declarada*: no prueba que el componente satisfaga el requisito.
- **Revisión estructural**: `@startuml`/`@enduml`, delimitadores balanceados, solo líneas `component` y `-->`, alias únicos, conectores entre alias declarados y mismo número de componentes/conectores que el modelo.
- Esta revisión local no sustituye el L0 completo de R2ABench: sin renderizador no se acredita renderizado.
- Un PUML marcado como **histórico** se revisa como archivo, pero no se acepta ni se incluye en las métricas de modelos validados si tiene un reporte de rechazo de una fase previa.
- **Render SVG**: compilación real con PlantUML (`n/d` si no está instalado).
- **Nodos GT**: declaraciones `rectangle`, `component`, `database`, `package`, `node`, `interface` en `AD/ad.puml`. Incluye contenedores (`package`), así que no equivale a \|C\|: el generador solo emite `component` planos.
- **Relaciones GT**: `-->` sólida dirigida (incluye `->`, `<--`, `-down->`), `..>` punteada dirigida, `--` sólida no dirigida, `..` punteada no dirigida. Se omiten comentarios, notas y leyendas.
- Los cocientes \|C\|/Nodos GT y \|K\|/Rel. GT comparan **tamaño**, no correspondencia. La correspondencia (L1) y la calidad semántica (L2) requieren `R2ABench/evaluation_script`.
- Los promedios se calculan sobre los proyectos en los que la métrica existe (ver n en la tabla descriptiva).
