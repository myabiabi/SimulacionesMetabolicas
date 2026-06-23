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

from gemsembler.drawing import draw_one_synt_path, MET_NOT_INT_GLOBAL
from cobra.io import read_sbml_model, write_sbml_model


from gemsembler import lp_example

lp_example

gathered = GatheredModels()
for model in lp_example:
    gathered.add_model(**model)
gathered.run()

supermodel_lp = gathered.assemble_supermodel("/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados", assembly_id = "GCF_000203855.3")
supermodel_lp_mix = gathered.assemble_supermodel("/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados", assembly_id = "GCF_000203855.3", do_mix_conv_notconv=True)
supermodel_lp.write_supermodel_to_json("/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/lp_supermodel.json")
supermodel_lp = read_supermodel_from_json("/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/lp_supermodel.json")
supermodel_lp.at_least_in(2)
core2 = get_model_of_interest(supermodel_lp, "core2")
core2 = get_model_of_interest(supermodel_lp, "core2", "/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/lp_core2.xml")


