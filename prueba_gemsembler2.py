import os
from gemsembler import (
    GatheredModels,
    read_supermodel_from_json,
    get_model_of_interest
)

output_dir = "/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/models/ensamble_gemsembler"
os.makedirs(output_dir, exist_ok=True)
id_bacteria = "mycobacterium_sp"

print("--- Paso 1: Cargando y estandarizando tus modelos ---")
gathered = GatheredModels()

gathered.add_model(
    model_id="mycobacterium_carveme",
    path_to_model="/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/models/rz_na_cv_lb_mycobacterium.xml",
    model_type="carveme"
)
gathered.add_model(
    model_id="mycobacterium_modelseed",
    path_to_model="/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/models/rz_na_rt_kb_lb_mycobacterium_sp.xml",
    model_type="modelseed"
)

gathered.run()
print("¡Estandarización completada!")

print("\n--- Paso 2: Ensamblando el Supermodel ---")
supermodel_bact = gathered.assemble_supermodel(
    output_folder=output_dir,
    assembly_id="GCF_000744355.1"  # tu accession real aquí
)

# Diagnóstico: ver qué niveles están disponibles
print("\n[DIAGNÓSTICO]")
print("Sources:", supermodel_bact.sources)
print("Comparison keys (antes de at_least_in):", list(supermodel_bact.reactions.comparison.keys()))

print("\n--- Paso 3: Exportación de modelos SBML ---")

# Unión total: usar "assembly" directamente, no requiere comparación previa
xml_union = os.path.join(output_dir, f"{id_bacteria}_union_completa.xml")
union_model = get_model_of_interest(supermodel_bact, "assembly", xml_union)
print(f"-> Unión exportada a: {xml_union}")

# Core: presente en AMBOS modelos
supermodel_bact.at_least_in(2)
print("Comparison keys (después de at_least_in(2)):", list(supermodel_bact.reactions.comparison.keys()))

# Usamos la primera key que aparezca en comparison (la que acaba de crear at_least_in(2))
core_key = list(supermodel_bact.reactions.comparison.keys())[0]
print(f"Usando key de core: '{core_key}'")

xml_core = os.path.join(output_dir, f"{id_bacteria}_core2.xml")
core_model = get_model_of_interest(supermodel_bact, core_key, xml_core)
print(f"-> Core (consenso) exportado a: {xml_core}")

print("\n--- Paso 4: Guardando el Supermodel en JSON ---")
json_path = os.path.join(output_dir, f"{id_bacteria}_supermodel.json")
supermodel_bact.write_supermodel_to_json(json_path)
print(f"-> JSON guardado en: {json_path}")

print("\n¡Proceso finalizado exitosamente!")