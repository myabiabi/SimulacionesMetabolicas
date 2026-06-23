import os
from gemsembler import (
    GatheredModels,
    read_supermodel_from_json,
    get_model_of_interest,
    lp_example
)

def main():
    # 1. Definir y crear la carpeta de resultados
    output_dir = "/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/ejemplo"
    os.makedirs(output_dir, exist_ok=True)

    print("--- Paso 1: Cargando y estandarizando modelos de ejemplo ---")
    gathered = GatheredModels()
    
    # Cargar los modelos predeterminados de Lactiplantibacillus
    for model in lp_example:
        gathered.add_model(**model)
        
    # Ejecutar la conversión/estandarización de nomenclaturas
    gathered.run()
    print("¡Estandarización completada con éxito!")

    print("\n--- Paso 2: Ensamblando el Supermodel ---")
    # Crear el supermodelo (especificando la carpeta y el ID de ensamble)
    supermodel_lp = gathered.assemble_supermodel(
        output_dir, 
        assembly_id="GCF_000203855.3"
    )
    
    # Opcional: Crear la versión mixta si la necesitas
    # supermodel_lp_mix = gathered.assemble_supermodel(output_dir, assembly_id = "GCF_000203855.3", do_mix_conv_notconv=True)

    print("\n--- Paso 3: Guardando y leyendo el Supermodel en JSON ---")
    json_path = os.path.join(output_dir, "lp_supermodel.json")
    
    # Guardar a JSON
    supermodel_lp.write_supermodel_to_json(json_path)
    
    # Volver a leer desde el JSON (para asegurar que se guardó correctamente)
    supermodel_lp = read_supermodel_from_json(json_path)

    print("\n--- Paso 4: Filtrado por nivel de confianza y exportación a SBML ---")
    # Filtrar reacciones que estén presentes al menos en 2 de los modelos de entrada
    supermodel_lp.at_least_in(2)
    
    # Generar el modelo de COBRApy (interés: "core2") y guardarlo en formato SBML (.xml)
    xml_path = os.path.join(output_dir, "lp_core2.xml")
    core2 = get_model_of_interest(supermodel_lp, "core2", xml_path)
    
    print(f"\n¡Proceso completado con éxito!")
    print(f"-> Supermodelo guardado en: {json_path}")
    # El archivo SBML final se guarda automáticamente gracias al tercer argumento de get_model_of_interest
    print(f"-> Modelo COBRApy (core2) exportado a: {xml_path}")

