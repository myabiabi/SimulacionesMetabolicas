import os
from gemsembler import (
    GatheredModels,
    read_supermodel_from_json,
    get_model_of_interest
)

def main():
    # 1. Rutas de tu proyecto de tesis 
    # Añadimos una subcarpeta de salida para mantener el orden en tu directorio
    output_dir = "/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/models/ensamble_gemsembler"
    os.makedirs(output_dir, exist_ok=True)

    print("--- Paso 1: Cargando y estandarizando tus modelos ---")
    gathered = GatheredModels()
    
    # Modelo 1: CarveMe
    gathered.add_model(
        model_path="/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/models/rz_na_cv_lb_mycobacterium.xml",
        tool="carveme"
    )
    
    # Modelo 2: ModelSEED (Corrección de indentación en el paréntesis de cierre)
    gathered.add_model(
        model_path="/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/models/rz_na_rt_kb_lb_mycobacterium_sp.xml",
        tool="modelseed"
    )

    # Ejecutar la conversión/estandarización de nomenclaturas de tus bacterias
    gathered.run()
    print("¡Estandarización de tus modelos completada con éxito!")

    print("\n--- Paso 2: Ensamblando el Supermodel ---")
    id_bacteria = "mycobacterium_sp" 
    
    supermodel_bact = gathered.assemble_supermodel(
        output_dir, 
        assembly_id=id_bacteria
    )

    print("\n--- Paso 3: Guardando y leyendo el Supermodel en JSON ---")
    json_path = os.path.join(output_dir, f"{id_bacteria}_supermodel.json")
    supermodel_bact.write_supermodel_to_json(json_path)
    supermodel_bact = read_supermodel_from_json(json_path)

    print("\n--- Paso 4: Filtrado por nivel de confianza y exportación a SBML ---")
    # REGLA DE UNIÓN: Conserva todo lo predicho por al menos 1 herramienta (Unión completa)
    supermodel_bact.at_least_in(1)
    
    # Se genera el archivo SBML de unión con el identificador core1
    xml_path = os.path.join(output_dir, f"{id_bacteria}_union_core1.xml")
    core1 = get_model_of_interest(supermodel_bact, "core1", xml_path)
    
    print(f"\n¡Proceso completado con tus datos!")
    print(f"-> Supermodelo guardado en: {json_path}")
    print(f"-> Modelo COBRApy de unión exportado a: {xml_path}")

if __name__ == "__main__":
    main()