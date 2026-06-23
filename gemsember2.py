import os
import cobra
from cobra.io import read_sbml_model, write_sbml_model

# 1. Imports principales de gemsembler (Limpiados y sin duplicados)
from gemsembler import (
    GatheredModels,
    read_supermodel_from_json,
    get_models_with_all_confidence_levels,
    get_model_of_interest
)

# 2. Funciones downstream para análisis posterior
from gemsembler.downstream import (
    glycolysis,
    pentose_phosphate,
    tca,
    biomass,
    get_met_neighborhood,
    run_growth_full_flux_analysis,
    pathway_of_interest,
    GLYCOLYSIS_GLOBAL,
    PENTOSE_PHOSPHATE_PATHWAY_GLOBAL,
    TCA_GLOBAL,
    COFACTORS_GLOBAL
)

from gemsembler import (
    GatheredModels,
    get_model_of_interest,
    get_models_with_all_confidence_levels
)

# ==========================
# Modelos de entrada
# ==========================

ecoli_example = [
    {
        "model_id": "ecoli_carveme",
        "path_to_model": "./02_resultados/modelos_core/ec_na_cv_na_ecoli.xml",
        "model_type": "carveme"
    },
    {
        "model_id": "ecoli_modelseed",
        "path_to_model": "./02_resultados/modelos_core/ec_na_kb_na_ecoli.xml",
        "model_type": "modelseed"
    }
]

# ==========================
# Directorio de salida
# ==========================

output_dir = "./gemsembler_output_ecoli/"

# ==========================
# Cargar modelos
# ==========================

gathered = GatheredModels()

for model in ecoli_example:
    gathered.add_model(**model)

# ==========================
# Conversión y ensamblaje
# ==========================

gathered.run()

supermodel_ecoli = gathered.assemble_supermodel(
    output_dir,
    path_final_genome_nt="/home/abigaylmontantearenas/Documents/proyecto_tesis/01_data/others/ecoli.fna",
    path_final_genome_aa="/home/abigaylmontantearenas/Documents/proyecto_tesis/01_data/others/ecoli.faa"
)

# ==========================
# Revisar niveles disponibles
# ==========================

print("\nNiveles disponibles:")

if hasattr(supermodel_ecoli, "get_all_confidence_levels"):
    print(supermodel_ecoli.get_all_confidence_levels())

print("\nAtributos del supermodelo:")
print(dir(supermodel_ecoli))

# ==========================
# Generar modelos de confianza
# ==========================

try:
    supermodel_ecoli.at_least_in(2)

    core2_model = get_model_of_interest(
        supermodel_ecoli,
        "core2",
        f"{output_dir}/ecoli_core2.xml"
    )

    print("Modelo core2 exportado correctamente.")

except Exception as e:
    print(f"\nNo fue posible generar core2: {e}")

# ==========================
# Exportar todos los modelos
# ==========================

try:
    all_models = get_models_with_all_confidence_levels(
        supermodel_ecoli,
        output_dir
    )

    print("Todos los niveles exportados correctamente.")

except Exception as e:
    print(f"\nError exportando todos los niveles: {e}")