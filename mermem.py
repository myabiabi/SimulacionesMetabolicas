# from functions import mergem_function
# mis_bacterias = ["agrobacterium", "arthrobacter", "bacillus", "bthuringensis", "mycobacterium", "paenibacillus", "pseudomonas", "pumssongensis", "rerythropolis",
#                  "vparadoxus"]

# # Llamas directamente a mergem_function
# diccionario_resultados = mergem_function(
#     ruta_input="/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/models/rz", 
#     ruta_output="/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/mergem/consensus_models_all", 
#     lista_patrones=mis_bacterias
# )

#from functions import mergem_statistics

#resultados = mergem_statistics(
    #ruta_input="/media/abigaylmontantearenas/UBUNTU 24_0/abi/models/rz",
    #ruta_output="/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/090826",
    #lista_patrones=["agrobacterium", "arthrobacter", "bacillus", "bthuringensis", "mycobacterium", "paenibacillus", "pseudomonas", "pumssongensis", "rerythropolis",
                  #"vparadoxus"]
#)






from functions import variables_totales
variables_totales(
    gem_path="/media/abigaylmontantearenas/UBUNTU 24_0/abi/models/cc",
    output_dir="/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/111026",
    output_filename="111026_cc_variables_totales.csv"
)