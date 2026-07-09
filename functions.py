import os
import csv
import cobra

def variables_totales(gem_path, output_dir, output_filename):
    # Nos aseguramos de que el directorio exista
    os.makedirs(output_dir, exist_ok=True)

    # Ahora usamos la variable 'output_filename' en lugar del texto fijo
    output_file = os.path.join(output_dir, output_filename)

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Model_ID",
            "Total_Reactions",
            "Total_Metabolites",
            "Total_Genes"
        ])

        for file_name in os.listdir(gem_path):
            if not file_name.endswith(".xml"):
                continue

            model_id = file_name.replace(".xml", "")
            model_path = os.path.join(gem_path, file_name)

            try:
                model = cobra.io.read_sbml_model(model_path)

                R = len(model.reactions)
                M = len(model.metabolites)
                G = len(model.genes)

                writer.writerow([model_id, R, M, G])

                print(f"{model_id}: R={R} M={M} G={G}")

            except Exception as e:
                print(f"ERROR cargando {model_id}: {e}")

    print(f"CSV guardado en: {output_file}")
    
    
import os
import glob
import cobra
import mergem

def mergem_function(ruta_input, ruta_output, lista_patrones):
    """
    Fusiona modelos metabólicos usando mergem para cada patrón en una lista.
    """
    resultados_totales = {}
    
    print(f"🚀 Iniciando procesamiento para {len(lista_patrones)} patrones...")
    
    # El ciclo FOR ahora está aquí adentro
    for patron in lista_patrones:
        
        # 1. Buscar archivos para ESTE patrón
        input_models = [
            f for f in glob.glob(os.path.join(ruta_input, "*.xml")) 
            if patron.lower() in os.path.basename(f).lower()
        ]
        
        # Validaciones para este patrón específico
        if not input_models:
            print(f"⚠️ [Saltado] No se encontraron archivos para: '{patron}'")
            continue # Salta al siguiente patrón de la lista
            
        if len(input_models) < 2:
            print(f"⚠️ [Saltado] Solo se encontró {len(input_models)} modelo para '{patron}'. Se necesitan al menos 2.")
            continue

        print(f"\n========================================")
        print(f"Iniciando consenso para: {patron.upper()}")
        print(f"Se encontraron {len(input_models)} modelos.")
        
        # 2. Ejecutar mergem
        try:
            results = mergem.merge(
                input_models, 
                set_objective='merge', 
                exact_sto=False, 
                use_prot=False, 
                extend_annot=False, 
                trans_to_db=None
            )
        except Exception as e:
            print(f"❌ Error en mergem para {patron}: {e}")
            continue

        # 3. Guardar el XML resultante
        os.makedirs(ruta_output, exist_ok=True)
        nombre_salida = f"modelo_consenso_{patron.lower()}.xml"
        output_path = os.path.join(ruta_output, nombre_salida)
        
        cobra.io.write_sbml_model(results['merged_model'], output_path)
        print(f"✅ Consenso guardado en: {output_path}")
        
        # Guardamos el resultado en nuestro diccionario usando el nombre de la bacteria
        resultados_totales[patron] = results
            
    print(f"\n🏁 ¡Proceso terminado!")
    return resultados_totales


def procesar_multiples_patrones(ruta_input, ruta_output, lista_patrones):
    """
    Recorre una lista de patrones, define el nombre de salida automáticamente 
    y ejecuta mergem para cada uno.
    
    Parameters:
    -----------
    ruta_input : str
        Ruta de la carpeta con los modelos XML individuales.
    ruta_output : str
        Ruta donde se guardarán los consensos.
    lista_patrones : list
        Lista de strings con los nombres o patrones a buscar (ej. ['mycobacterium', 'pseudomonas']).
    """
    resultados_totales = {}
    
    print(f"🚀 Iniciando procesamiento por lote para {len(lista_patrones)} patrones...")
    
    for patron in lista_patrones:
        # Generamos el nombre de salida de forma automática usando el patrón
        nombre_salida = f"modelo_consenso_{patron.lower()}.xml"
        
        # Llamamos a la función individual
        res = mergem_function(ruta_input, ruta_output, nombre_salida, patron)
        
        if res is not None:
            resultados_totales[patron] = res
            
    print(f"\n ¡Proceso terminado! Se generaron exitosamente {len(resultados_totales)} modelos consenso.")
    return resultados_totales

#imprimir lista reacciones: 
# # Load the XML/SBML model
import cobra


model = cobra.io.read_sbml_model("/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/models/rz/rz_na_cv_lb_paenibacillus.xml")

# # Print the total number of reactions
# print(f"Total reactions: {len(model.reactions)}")

# # Print a formatted list of all reactions with their IDs and stoichiometry
# for reaction in model.reactions:
#     print(f"{reaction.id}: {reaction.reaction}")


# # Load the model from your xml/sbml file

# # Print the total number of genes
# print(f"Total Genes: {len(model.genes)}")

# # Iterate through and print the ID and Name of each gene
# for gene in model.genes:
#     print(f"Gene ID: {gene.id} | Name: {gene.name}")

#Buscar nombre de elementos para mediop:import pandas as pd

# data_url = "http://bigg.ucsd.edu/static/namespace/bigg_models_metabolites.txt"
# # You can now mix common names and chemical formulas
# medio_names = ['glucose', 'ethanol', '-', 'h2o', 'phosphate']

# def defmedio(url, name_mets):
#     df = pd.read_csv(url, sep="\t")
    
#     # Use the column names identified in your previous terminal output
#     id_col = 'bigg_id' if 'bigg_id' in df.columns else df.columns[0]
#     name_col = 'name' if 'name' in df.columns else df.columns[1]
    
#     medio = []
#     for m in name_mets:
#         # This regex looks for the string anywhere in the name (case-insensitive)
#         # It handles 'O2' inside 'Oxygen' or 'Glc' inside 'Glucose'
#         matches = df[
#             (df[name_col].str.contains(m, case=False, na=False)) & 
#             (df[id_col].str.endswith('_e', na=False))
#         ]
        
#         # If we found matches, we try to find the "cleanest" one
#         if not matches.empty:
#             # Sort by the length of the name so 'Oxygen' comes before 'Oxygenated compound'
#             matches = matches.assign(name_len=matches[name_col].str.len())
#             matches = matches.sort_values('name_len').drop(columns='name_len')
            
#             # Take the top 3 most likely candidates
#             medio.append(matches.head(3))
            
#     if not medio:
#         return pd.DataFrame()
        
#     return pd.concat(medio).drop_duplicates()

# # Execute
# final_df = defmedio(data_url, medio_names)
# print(final_df[[final_df.columns[0], 'name']])
