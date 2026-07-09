import os
import glob
from gemsembler import (
    GatheredModels,
    read_supermodel_from_json,
    get_model_of_interest
)

output_dir = "/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/gemsembler"
os.makedirs(output_dir, exist_ok=True)
id_bacteria = "mycobacterium_sp"

print("--- Paso 1: Cargando y estandarizando tus modelos ---")
gathered = GatheredModels()

genoma_nt = "/home/abigaylmontantearenas/Documents/proyecto_tesis/01_data/rz/raw/ncl_files/GCF_000744355.fna"
genoma_aa = "/home/abigaylmontantearenas/Documents/proyecto_tesis/01_data/rz/raw/protein_files/GCF_000744355.faa"

# NOTA: no pasamos path_to_genome aquí a propósito.
# Prioridad = red metabólica consensuada (reacciones/metabolitos),
# no la unificación de genes entre modelos (que requeriría resolver
# el mismatch de esquemas de ID vía BLAST, ver conversación anterior).
gathered.add_model(
    model_id="mycobacterium_carveme",
    path_to_model="/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/models/rz/rz_na_cv_lb_mycobacterium.xml",
    model_type="carveme",
)
gathered.add_model(
    model_id="mycobacterium_modelseed",
    path_to_model="/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/models/rz/rz_na_rt_kb_lb_mycobacterium.xml",
    model_type="modelseed",
)
gathered.add_model(
    model_id="mycobacterium_gapseq",
    path_to_model="/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/models/rz/rz_na_gp_lb_mycobacterium.xml",
    model_type="gapseq",
)

gathered.run()
print("¡Estandarización completada!")

print("\n--- Paso 2: Ensamblando el Supermodel ---")
supermodel_bact = gathered.assemble_supermodel(
    output_folder=output_dir,
    path_final_genome_nt=genoma_nt,
    path_final_genome_aa=genoma_aa,
)

print("\n[DIAGNÓSTICO]")
print("Sources:", supermodel_bact.sources)
print("Comparison keys (antes de at_least_in):", list(supermodel_bact.reactions.comparison.keys()))

print("\n--- Paso 3: Exportación de modelos SBML ---")

# Unión total: todas las reacciones presentes en al menos 1 de los 3 modelos
xml_union = os.path.join(output_dir, f"{id_bacteria}_union_completa.xml")
union_model = get_model_of_interest(supermodel_bact, "assembly", xml_union)
print(f"-> Unión exportada a: {xml_union}")

# Core: reacciones presentes en al menos 2 de los 3 modelos
supermodel_bact.at_least_in(2)
print("Comparison keys (después de at_least_in(2)):", list(supermodel_bact.reactions.comparison.keys()))

core_key = list(supermodel_bact.reactions.comparison.keys())[0]
print(f"Usando key de core: '{core_key}'")

xml_core2 = os.path.join(output_dir, f"{id_bacteria}_core2.xml")
core2_model = get_model_of_interest(supermodel_bact, core_key, xml_core2)
print(f"-> Core (>=2 de 3 modelos) exportado a: {xml_core2}")

# Opcional: reacciones presentes en los 3 modelos (consenso más estricto)
supermodel_bact.at_least_in(3)
print("Comparison keys (después de at_least_in(3)):", list(supermodel_bact.reactions.comparison.keys()))
core_key_3 = [k for k in supermodel_bact.reactions.comparison.keys() if k != core_key][0]

xml_core3 = os.path.join(output_dir, f"{id_bacteria}_core3.xml")
core3_model = get_model_of_interest(supermodel_bact, core_key_3, xml_core3)
print(f"-> Core estricto (3 de 3 modelos) exportado a: {xml_core3}")

print("\n--- Paso 4: Guardando el Supermodel en JSON ---")
json_path = os.path.join(output_dir, f"{id_bacteria}_supermodel.json")
supermodel_bact.write_supermodel_to_json(json_path)
print(f"-> JSON guardado en: {json_path}")

print("\n¡Proceso finalizado exitosamente!")