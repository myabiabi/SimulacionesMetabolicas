# from functions import mergem_function
# mis_bacterias = ["agrobacterium", "arthrobacter", "bacillus", "bthuringensis", "mycobacterium", "paenibacillus", "pseudomonas", "pumssongensis", "rerythropolis",
#                  "vparadoxus"]

# # Llamas directamente a mergem_function
# diccionario_resultados = mergem_function(
#     ruta_input="/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/models/rz", 
#     ruta_output="/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/mergem/consensus_models_all", 
#     lista_patrones=mis_bacterias
# )

from functions import variables_totales

variables_totales(
    gem_path="/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/models/rz",
    output_dir="/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/evaluacion/rz",
    output_filename="rz_variables_totales.csv"
)