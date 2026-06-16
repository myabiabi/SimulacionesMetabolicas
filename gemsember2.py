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
from gemsembler.drawing import draw_one_synt_path, MET_NOT_INT_GLOBAL

# 3. Configuración de modelos de entrada
# Ajustado según el origen real de tus archivos (.faa para CarveMe y .fna para KBase)
st_example = [
    {
        "model_id": "arthrobacter_carveme",
        "path_to_model": "./02_resultados/models/rz_na_cv_lb_arthrobacter.xml",
        "model_type": "carveme",
        "path_to_genome": "01_data/rz/protein_files/GCF_000374945.faa" 
    },
    {
        "model_id": "arthrobacter_kbase",
        "path_to_model": "./02_resultados/models/rz_na_rt_kb_lb_arthrobacter.xml",
        "model_type": "modelseed",
        "path_to_genome": "01_data/rz/ncl_files/GCF_000374945.fna" 
    }
]

# 4. Inicializar y correr el recolector
gathered = GatheredModels()
for model in st_example:
    gathered.add_model(**model)
gathered.run()

# 5. Ensamblar el supermodelo
# Aquí le das ambos archivos de referencia finales para que Gemsembler haga el mapeo cruzado
supermodel_lp = gathered.assemble_supermodel(
    "./gemsembler_output/",
    path_final_genome_nt="01_data/rz/ncl_files/GCF_000374945.fna", 
    path_final_genome_aa="01_data/rz/protein_files/GCF_000374945.faa"
)

print("Tipo de superobjeto:", type(supermodel_lp))
print("Métodos disponibles:", dir(supermodel_lp))

# 6. Verificar niveles de confianza disponibles (ej. 'core', 'extended', etc.)
levels = supermodel_lp.get_all_confidence_levels()
print("Niveles de confianza disponibles:", levels)


# Opción A: Exportar un nivel específico (ej. "core2")
print("Exportando nivel core2...")
core2_model = get_model_of_interest(
    supermodel_lp,
    "core2",
    "./gemsembler_output/st_core2.xml"
)

# Opción B: Exportar todos los niveles en lote a la carpeta de salida
print("Exportando todos los niveles disponibles...")
all_models = get_models_with_all_confidence_levels(
    supermodel_lp,
    "./gemsembler_output/"
)