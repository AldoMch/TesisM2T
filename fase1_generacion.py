import json
import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Configuración inicial
load_dotenv()
client = genai.Client()

def extraer_requisitos(ruta_jsonl):
    #Lee el archivo de entrada y extrae el texto de los requisitos.
    requisitos = []
    with open(ruta_jsonl, 'r', encoding='utf-8') as f:
        for linea in f:
            data = json.loads(linea.strip())
            # formato del few-shot (ID: Texto)
            requisitos.append(f"{data.get('req_id')}: {data.get('requirement')}")
    return "\n".join(requisitos)

def ejecutar_fase_1_batch():
    #Ejecuta la Fase 1 aislando el prompt  y procesando el dataset
    base_dataset = "R2ABench/Dataset/E-R2A"
    base_salidas = "salidas_evaluacion"
    
    # 1. EL PROMPT ESTÁTICO (Incluye el ejemplo Few-Shot)
    instruccion_sistema = """
    Rol: Actúa como un asistente de arquitectura de software.

    Tarea:
    Analiza los requisitos proporcionados y genera un único objeto
    JSON que represente un modelo arquitectónico candidato.

    Restricciones:
    1. No escribas explicaciones ni bloques Markdown. Solo devuelve el JSON.
    2. Conserva los identificadores y las descripciones de los requisitos de entrada. No agregues ni elimines requisitos.
    3. Declara identificadores únicos para los componentes.
    4. Asocia cada componente con uno o más requisitos existentes mediante el campo tracesTo.
    5. Cada conector debe referenciar componentes declarados.
    6. Usa solamente los campos definidos en la plantilla (requirements, components, connectors).
    7. Usa tipos de relación compatibles con las responsabilidades de los componentes.

    Ejemplo de entrada:
    REQ-01: El sistema debe permitir registrar usuarios.
    REQ-02: El sistema debe almacenar los datos de usuarios.

    Ejemplo de salida:
    {
      "requirements": [
        {
          "id": "REQ-01",
          "description": "El sistema debe permitir registrar usuarios."
        },
        {
          "id": "REQ-02",
          "description": "El sistema debe almacenar los datos de usuarios."
        }
      ],
      "components": [
        {
          "id": "CMP_01",
          "name": "Servicio de Usuarios",
          "layer": "business",
          "responsibility": "Gestionar el registro de usuarios.",
          "tracesTo": ["REQ-01"]
        },
        {
          "id": "CMP_02",
          "name": "Repositorio de Usuarios",
          "layer": "data",
          "responsibility": "Persistir los datos de usuarios.",
          "tracesTo": ["REQ-02"]
        }
      ],
      "connectors": [
        {
          "source": "CMP_01",
          "target": "CMP_02",
          "type": "repository"
        }
      ]
    }
    """

    # 2. RECORRER LAS CARPETAS JAVA Y PYTHON
    for lenguaje in ["JAVA", "Python"]:
        ruta_lenguaje = os.path.join(base_dataset, lenguaje)
        
        if not os.path.exists(ruta_lenguaje):
            print(f"Advertencia: No se encontró la ruta {ruta_lenguaje}")
            continue
            
        proyectos = os.listdir(ruta_lenguaje)
        
        for proyecto in proyectos:
            ruta_proyecto = os.path.join(ruta_lenguaje, proyecto)
            archivo_entrada = os.path.join(ruta_proyecto, "req_final.jsonl")
            
            # Verificar que sea un directorio válido con requisitos
            if os.path.isdir(ruta_proyecto) and os.path.exists(archivo_entrada):
                print(f"\n-> Procesando proyecto: {lenguaje} / {proyecto}")
                
                # Replicar la estructura de carpetas en salidas_evaluacion
                ruta_salida_proyecto = os.path.join(base_salidas, lenguaje, proyecto)
                os.makedirs(ruta_salida_proyecto, exist_ok=True)
                archivo_salida = os.path.join(ruta_salida_proyecto, "1_respuesta_llm_candidata.txt")
                
                # Comprobación de seguridad: omitir si ya fue generado antes
                if os.path.exists(archivo_salida):
                    print("   [Omitido] Este proyecto ya fue procesado previamente.")
                    continue
                
                requisitos_dinamicos = extraer_requisitos(archivo_entrada)
                
                # Prompt del usuario estructurado
                prompt_usuario = f"Ahora analiza los siguientes requisitos:\n{requisitos_dinamicos}\n\nDevuelve únicamente el objeto JSON."
                
                max_reintentos = 3
                for intento in range(max_reintentos):
                    try:
                        print(f"   Consultando a Gemini (Intento {intento + 1}/{max_reintentos})...")
                        response = client.models.generate_content(
                            model='gemini-flash-latest',
                            contents=prompt_usuario,
                            config=types.GenerateContentConfig(
                                system_instruction=instruccion_sistema,
                                response_mime_type="application/json",
                                temperature=0.2,
                            )
                        )
                        
                        with open(archivo_salida, 'w', encoding='utf-8') as f:
                            f.write(response.text)
                        print(f"   Salida guardada en: {archivo_salida}")
                        break  # Si tiene éxito, rompe el bucle de reintentos
                        
                    except Exception as e:
                        print(f"   Fallo temporal: {e}")
                        if intento < max_reintentos - 1:
                            print("   Esperando 10 segundos antes de reintentar...")
                            time.sleep(10)
                        else:
                            print(f"   Error definitivo al procesar {proyecto}.")


                # 3. CONTROL DE RATE LIMIT (15 peticiones por minuto)
                print("   Esperando 5 segundos para respetar los límites de la API...")
                time.sleep(5)

# --- Ejecución ---
if __name__ == "__main__":
    print("Iniciando procesamiento por lotes (Fase 1 con Few-Shot)...")
    ejecutar_fase_1_batch()
    print("\nProcesamiento completo.")