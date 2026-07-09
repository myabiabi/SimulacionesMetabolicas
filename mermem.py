from functions import mergem_function
mis_bacterias = ["agrobacterium", "arthrobacter", "bacillus", "bthuringensis", "mycobacterium", "paenibacillus", "pseudomonas", "pumssongensis", "rerythropolis",
                 "vparadoxus"]

# Llamas directamente a mergem_function
diccionario_resultados = mergem_function(
    ruta_input="/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/mergem/models", 
    ruta_output="/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/mergem/consensus_models", 
    lista_patrones=mis_bacterias
)