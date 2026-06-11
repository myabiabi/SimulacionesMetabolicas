from gemsembler import (
    GatheredModels,  # Object to collect input models and build a supermodel
    read_supermodel_from_json,  # Function to read a save supermodel
    get_models_with_all_confidence_levels,  # creates cobrapy models at all confidence levels
    get_model_of_interest  # creates one cobrapy model
)

from gemsembler.downstream import (
    glycolysis,  # returns table and/or interactive maps of glycolysis
    pentose_phosphate,  # returns table and/or interactive maps of pentose phosphate
    tca,  # # returns table and/or interactive maps of TCA
    # table_reactions_confidence,  # returns a pandas dataframe with reaction IDs, confidence and additional info
    # calc_dist_for_synt_path,
    biomass,
    get_met_neighborhood,
    # run_metquest_results_analysis,
    run_growth_full_flux_analysis,
    # write_metabolites_production_output,
    pathway_of_interest,
    # get_met_neighborhood,
    GLYCOLYSIS_GLOBAL,
    PENTOSE_PHOSPHATE_PATHWAY_GLOBAL,
    TCA_GLOBAL,
    COFACTORS_GLOBAL
)
import os
import cobra
from gemsembler.drawing import draw_one_synt_path, MET_NOT_INT_GLOBAL
from cobra.io import read_sbml_model, write_sbml_model

st_example = [
    {
        "model_id": "st60_carveme",
        "path_to_model": "./02_resultados/models/rz_na_cv_lb_GCF_000374945.xml",
        "model_type": "carveme",
        "path_to_genome": "01_data/protein_files/GCF_000374945.faa"
    },

    {
        "model_id": "st60_kbase",
        "path_to_model": "./02_resultados/models/rz_na_rt_kb_lb_arthrobacter_sp.xml",
        "model_type": "modelseed",
        "path_to_genome": "01_data/amino_files/GCF_000374945.1_ASM37494v1_genomic.fna"
    }
]

gathered = GatheredModels()
for model in st_example:
    gathered.add_model(**model)
gathered.run()

supermodel_lp = gathered.assemble_supermodel(
    "./gemsembler_output/",
    path_final_genome_nt="01_data/amino_files/GCF_000374945.1_ASM37494v1_genomic.fna",
    path_final_genome_aa="01_data/protein_files/GCF_000374945.faa"
)

print(type(supermodel_lp))
print(dir(supermodel_lp))


# Ver qué niveles de confianza están disponibles
print(supermodel_lp.get_all_confidence_levels())

# Opción A: exportar un nivel específico (ej. "core2" o "assembly")
core2_model = get_model_of_interest(
    supermodel_lp,
    "core2",
    "./gemsembler_output/st60_core2.xml"
)

# Opción B: exportar todos los niveles de una vez
all_models = get_models_with_all_confidence_levels(
    supermodel_lp,
    "./gemsembler_output/"
)

# Opción C: si las funciones anteriores no escriben el .xml directamente,
# exportar manualmente con COBRApy
from cobra.io import write_sbml_model

write_sbml_model(core2_model, "./gemsembler_output/st60_core2.xml")


