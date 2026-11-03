Reporte de Ejecución: Resiliencia y Manejo de Interrupciones en la API

1. Contexto Operativo

Durante la ejecución de la Fase 1 (Generación probabilística asistida por LLM) sobre el conjunto de datos E-R2A (17 proyectos en Java y Python), el flujo de trabajo dependió de la API de Google Gemini (gemini-flash-latest). Al utilizar la capa gratuita (Free Tier) de este servicio en la nube, el sistema estuvo expuesto a limitaciones de infraestructura y cuotas de red que son ajenas a la lógica del pipeline propuesto, pero críticas para su evaluación.

2. Limitaciones de Conectividad y Cuota Identificadas

Durante el procesamiento por lotes se describieron los siguientes tipos de interrupciones. Las cifras de cuota de este documento corresponden a esas pruebas; no representan los límites vigentes para cualquier cuenta o modelo.

Saturación del Servidor (Error 503 UNAVAILABLE): Interrupciones temporales causadas por picos globales de alta demanda en los servidores del modelo, lo que provocó el rechazo aleatorio de ciertas peticiones (ej. en los proyectos AwesomeMusic y Campus_Helper).

Agotamiento de Cuota (Error 429 RESOURCE_EXHAUSTED): Restricciones de capa gratuita que limitan el servicio a 20 peticiones diarias. Una vez superado este límite, la API deniega el acceso exigiendo un tiempo de espera de restablecimiento (aproximadamente 24 horas) o la transición a un modelo de facturación (Pay-as-you-go).

3. Arquitectura de Tolerancia a Fallos Implementada

Para mitigar estas interrupciones y permitir continuar el procesamiento, se implementaron tres estrategias en el script de generación:

Reintentos con espera fija: Se encapsuló la llamada al modelo en un bloque de hasta 3 intentos, con pausas de 10 segundos entre fallos. No es una espera exponencial. El script reintenta errores de llamada, sin reparar candidatos rechazados por fases posteriores.

Puntos de Control y Omisión (Checkpointing): El sistema evalúa la existencia previa del artefacto físico de salida (1_respuesta_llm_candidata.txt). Al reanudarse la ejecución tras un error crítico (como el 429), el motor omite los proyectos ya materializados, preservando el estado del pipeline y optimizando el consumo de la cuota restante de la API.

Control de Tasa de Peticiones (Rate Limiting): Se introdujo un retraso artificial u overhead (5 segundos por iteración) para evitar la saturación por peticiones simultáneas, respetando el límite de la API de 15 RPM (Peticiones Por Minuto).

4. Impacto en el Tiempo de Ejecución y Escalabilidad

Las esperas y los reintentos aumentan el tiempo total de procesamiento. El tiempo de respuesta del modelo es variable y estas pruebas no establecen una latencia garantizada.

Un plan de pago también puede tener cuotas, saturación y fallos temporales. No se midió la escalabilidad del pipeline ni se probó la ejecución paralela; estas incidencias solo describen las condiciones observadas durante la generación.
