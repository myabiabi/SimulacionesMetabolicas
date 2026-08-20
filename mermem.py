#from functions import mergem_function
#mis_bacterias = ["batrophaeus", "bthuringiensis" 
                  #]

#diccionario_resultados = mergem_function(
      #ruta_input="/media/abigaylmontantearenas/UBUNTU 24_0/abi/models/cc/mergem", 
      #ruta_output="/media/abigaylmontantearenas/UBUNTU 24_0/abi/models/cc/mergem", 
      #lista_patrones=mis_bacterias
  #)

#from functions import mergem_statistics

#resultados = mergem_statistics(
    #ruta_input="/media/abigaylmontantearenas/UBUNTU 24_0/abi/models/rz",
    #ruta_output="/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/090826",
    #lista_patrones=["agrobacterium", "arthrobacter", "bacillus", "bthuringensis", "mycobacterium", "paenibacillus", "pseudomonas", "pumssongensis", "rerythropolis",
                  #"vparadoxus"]
#)


from functions import variables_totales
variables_totales(
    gem_path="/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/ecoli",
    output_dir="/home/abigaylmontantearenas/Documents/proyecto_tesis",
    output_filename="1006_ecoli_variables_totales.csv"
)


# # Uso
# from functions import buscar_metabolitos
# medio_names = ["Aluminum",
# "Borate",
# "CO2",
# "Calcium",
# "Chloride",
# "Cobalt",
# "Copper",
# "Copper",
# "Fluorine",
# "Iodide",
# "Iron Fe2+",
# "Iron Fe3+",
# "Magnesium",
# "Manganese",
# "Ammonia",
# "Nitrate",
# "Nitrite",
# "Nickel",
# "Oxygen",
# "Phosphate",
# "Potassium",
# "Proton (H+)",
# "Hydrogen sulfide",
# "Sulfate",
# "Sulfite",
# "Thiosulfate",
# "Sodium",
# "Zinc"

# ]
# final_df = buscar_metabolitos(medio_names)
# print(final_df)

# import pandas as pd

# # Example DataFrame
# df = pd.DataFrame(final_df)

# # Save to CSV (recommended syntax)
# df.to_csv('/home/abigaylmontantearenas/Documents/proyecto_tesis/01_data/media/mm.csv', index=False)
