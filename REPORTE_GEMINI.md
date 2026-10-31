Reporte de Ejecución: Resiliencia y Manejo de Interrupciones en la API

1. Contexto Operativo

Durante la ejecución de la Fase 1 (Generación probabilística asistida por LLM) sobre el conjunto de datos E-R2A (17 proyectos en Java y Python), el flujo de trabajo dependió de la API de Google Gemini (gemini-flash-latest). Al utilizar la capa gratuita (Free Tier) de este servicio en la nube, el sistema estuvo expuesto a limitaciones de infraestructura y cuotas de red que son ajenas a la lógica del pipeline propuesto, pero críticas para su evaluación.

2. Limitaciones de Conectividad y Cuota Identificadas

Durante el procesamiento por lotes (batch processing), se registraron dos tipos de interrupciones documentadas por el propio proveedor:

Saturación del Servidor (Error 503 UNAVAILABLE): Interrupciones temporales causadas por picos globales de alta demanda en los servidores del modelo, lo que provocó el rechazo aleatorio de ciertas peticiones (ej. en los proyectos AwesomeMusic y Campus_Helper).

Agotamiento de Cuota (Error 429 RESOURCE_EXHAUSTED): Restricciones de capa gratuita que limitan el servicio a 20 peticiones diarias. Una vez superado este límite, la API deniega el acceso exigiendo un tiempo de espera de restablecimiento (aproximadamente 24 horas) o la transición a un modelo de facturación (Pay-as-you-go).

3. Arquitectura de Tolerancia a Fallos Implementada

Para mitigar estas variables ambientales y asegurar el determinismo operativo del pipeline, se implementaron tres estrategias de resiliencia en el script de generación:

Mecanismo de Reintentos (Exponential Backoff / Retry): Se encapsuló la llamada probabilística en un bloque de reintentos finitos (hasta 3 intentos) con pausas de 10 segundos. Esto permitió superar exitosamente los errores temporales 503 sin intervención humana, "rescatando" ejecuciones como la del proyecto POCD.

Puntos de Control y Omisión (Checkpointing): El sistema evalúa la existencia previa del artefacto físico de salida (1_respuesta_llm_candidata.txt). Al reanudarse la ejecución tras un error crítico (como el 429), el motor omite los proyectos ya materializados, preservando el estado del pipeline y optimizando el consumo de la cuota restante de la API.

Control de Tasa de Peticiones (Rate Limiting): Se introdujo un retraso artificial u overhead (5 segundos por iteración) para evitar la saturación por peticiones simultáneas, respetando el límite de la API de 15 RPM (Peticiones Por Minuto).

4. Impacto en el Tiempo de Ejecución y Escalabilidad

Las medidas de tolerancia a fallos añaden un costo temporal al proceso. Aunque la inferencia individual del LLM toma solo un par de segundos, el overhead inyectado para la gestión de red incrementa el tiempo total del procesamiento por lotes.

No obstante, esta limitación es estrictamente inherente al entorno de pruebas gratuito. En un escenario de producción empresarial, la adopción de una capa de facturación por uso (Pay-as-you-go) eliminaría las restricciones de cuota (429) y la necesidad de pausas restrictivas, permitiendo paralelizar las peticiones y demostrando que la arquitectura propuesta es altamente escalable y apta para entornos industriale


siliencia y Manejo de Interrupciones en la API

1. Contexto Operativo

Durante la ejecución de la Fase 1 (Generación probabilística asistida por LLM) sobre el conjunto de datos E-R2A (17 proyectos en Java y Python), el flujo de trabajo dependió de la API de Google Gemini (gemini-flash-latest). Al utilizar la capa gratuita (Free Tier) de este servicio en la nube, el sistema estuvo expuesto a limitaciones de infraestructura y cuotas de red que son ajenas a la lógica del pipeline propuesto, pero críticas para su evaluación.

2. Limitaciones de Conectividad y Cuota Identificadas

Durante el procesamiento por lotes (batch processing), se registraron dos tipos de interrupciones documentadas por el propio proveedor:

Saturación del Servidor (Error 503 UNAVAILABLE): Interrupciones temporales causadas por picos globales de alta demanda en los servidores del modelo, lo que provocó el rechazo aleatorio de ciertas peticiones (ej. en los proyectos AwesomeMusic y Campus_Helper).

Agotamiento de Cuota (Error 429 RESOURCE_EXHAUSTED): Restricciones de capa gratuita que limitan el servicio a 20 peticiones diarias. Una vez superado este límite, la API deniega el acceso exigiendo un tiempo de espera de restablecimiento (aproximadamente 24 horas) o la transición a un modelo de facturación (Pay-as-you-go).

3. Arquitectura de Tolerancia a Fallos Implementada

Para mitigar estas variables ambientales y asegurar el determinismo operativo del pipeline, se implementaron tres estrategias de resiliencia en el script de generación:

Mecanismo de Reintentos (Exponential Backoff / Retry): Se encapsuló la llamada probabilística en un bloque de reintentos finitos (hasta 3 intentos) con pausas de 10 segundos. Esto permitió superar exitosamente los errores temporales 503 sin intervención humana, "rescatando" ejecuciones como la del proyecto POCD.

Puntos de Control y Omisión (Checkpointing): El sistema evalúa la existencia previa del artefacto físico de salida (1_respuesta_llm_candidata.txt). Al reanudarse la ejecución tras un error crítico (como el 429), el motor omite los proyectos ya materializados, preservando el estado del pipeline y optimizando el consumo de la cuota restante de la API.

Control de Tasa de Peticiones (Rate Limiting): Se introdujo un retraso artificial u overhead (5 segundos por iteración) para evitar la saturación por peticiones simultáneas, respetando el límite de la API de 15 RPM (Peticiones Por Minuto).

4. Impacto en el Tiempo de Ejecución y Escalabilidad

Las medidas de tolerancia a fallos añaden un costo temporal al proceso. Aunque la inferencia individual del LLM toma solo un par de segundos, el overhead inyectado para la gestión de red incrementa el tiempo total del procesamiento por lotes.

No obstante, esta limitación es estrictamente inherente al entorno de pruebas gratuito. En un escenario de producción empresarial, la adopción de una capa de facturación por uso (Pay-as-you-go) eliminaría las restricciones de cuota (429) y la necesidad de pausas restrictivas, permitiendo paralelizar las peticiones y demostrando que la arquitectura propuesta es altamente escalable y apta para entornos industriales.
