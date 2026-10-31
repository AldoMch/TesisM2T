import os
import json

def ejecutar_fase_2_batch():
    #Materializa los JSON de la fase 1
    base_salidas = "salidas_evaluacion"
    
    print("Iniciando Fase 2: Análisis Sintáctico y Materialización...\n")
    
    # Recorrer los lenguajes (JAVA, Python)
    for lenguaje in ["JAVA", "Python"]:
        ruta_lenguaje = os.path.join(base_salidas, lenguaje)
        if not os.path.exists(ruta_lenguaje):
            continue
            
        # Recorrer cada proyecto
        for proyecto in os.listdir(ruta_lenguaje):
            ruta_proyecto = os.path.join(ruta_lenguaje, proyecto)
            archivo_entrada = os.path.join(ruta_proyecto, "1_respuesta_llm_candidata.txt")
            archivo_salida = os.path.join(ruta_proyecto, "2_candidato_materializado.json")
            archivo_error = os.path.join(ruta_proyecto, "reporte_de_errores.json")
            
            # Si no hay entrada, saltar
            if not os.path.exists(archivo_entrada):
                continue
                
            # Si ya se procesó (ya sea con éxito o con error), saltar
            if os.path.exists(archivo_salida) or os.path.exists(archivo_error):
                print(f"[{proyecto}] Omitido (Ya procesado en Fase 2)")
                continue
                
            print(f"-> Procesando: {proyecto}")
            
            # 1. Leer el texto crudo
            with open(archivo_entrada, 'r', encoding='utf-8') as f:
                texto_crudo = f.read()
                
            texto_limpio = texto_crudo.strip()
            if texto_limpio.startswith("```json"):
                texto_limpio = texto_limpio[7:]
            if texto_limpio.endswith("```"):
                texto_limpio = texto_limpio[:-3]
            texto_limpio = texto_limpio.strip()
            
            # 3. EL NÚCLEO DE LA FASE 2: Intento de Parseo
            try:
                # Si esto funciona, la sintaxis JSON es perfecta
                modelo_json = json.loads(texto_limpio)
                
                # Guardar el artefacto exitoso
                with open(archivo_salida, 'w', encoding='utf-8') as f:
                    json.dump(modelo_json, f, indent=2, ensure_ascii=False)
                print("   Éxito: JSON materializado correctamente.")
                
            except json.JSONDecodeError as e:
                # Si esto falla, pasa a reporte de errores
                error_report = {
                    "fase_fallo": "Fase 2 (Materialización JSON)",
                    "error_tipo": "Parseo fallido",
                    "descripcion": "El LLM no generó un JSON sintácticamente válido.",
                    "detalle_python": str(e)
                }
                
                with open(archivo_error, 'w', encoding='utf-8') as f:
                    json.dump(error_report, f, indent=2, ensure_ascii=False)
                print("   Fallo: Error de sintaxis JSON. Flujo abortado para este proyecto.")

if __name__ == "__main__":
    ejecutar_fase_2_batch()
    print("\nProcesamiento de Fase 2 completado.")