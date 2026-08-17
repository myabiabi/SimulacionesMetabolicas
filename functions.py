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
#import mergem

def mergem_function(ruta_input, ruta_output, lista_patrones):
    """
    Fusiona modelos metabólicos usando mergem para cada patrón en una lista.
    """
    resultados_totales = {}
    
    print(f" Iniciando para {len(lista_patrones)} patrones...")
    
    # El ciclo FOR ahora está aquí adentro
    for patron in lista_patrones:
        
        # 1. Buscar archivos para ESTE patrón
        input_models = [
            f for f in glob.glob(os.path.join(ruta_input, "*.xml")) 
            if patron.lower() in os.path.basename(f).lower()
        ]
        
        # Validaciones para este patrón específico
        if not input_models:
            print(f"No se encontraron archivos para: '{patron}'")
            continue # Salta al siguiente patrón de la lista
            
        if len(input_models) < 2:
            print(f"Solo se encontró {len(input_models)} modelo para '{patron}'. Se necesitan al menos 2.")
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
            print(f"Error {patron}: {e}")
            continue

        # 3. Guardar el XML resultante
        os.makedirs(ruta_output, exist_ok=True)
        nombre_salida = f"modelo_consenso_{patron.lower()}.xml"
        output_path = os.path.join(ruta_output, nombre_salida)
        
        cobra.io.write_sbml_model(results['merged_model'], output_path)
        print(f"Consenso guardado en: {output_path}")
        
        # Guardamos el resultado en nuestro diccionario usando el nombre de la bacteria
        resultados_totales[patron] = results
            
    print(f"fin")
    return resultados_totales


import os
import glob
from itertools import combinations
#import mergem
import cobra
import pandas as pd

def mergem_statistics(ruta_input, ruta_output, lista_patrones):
    """
    Para cada patrón en la lista, busca todos los modelos .xml que lo
    contengan en el nombre y calcula la distancia/similitud de Jaccard
    para TODOS los pares posibles de esos modelos (no solo el consenso
    global).

    Devuelve un diccionario:
        resultados_totales[patron] = {
            "pares": {(archivo1, archivo2): jacc_valor, ...},
            "tabla": DataFrame con columnas [modelo_1, modelo_2, jaccard]
        }
    """
    resultados_totales = {}

    print(f"Iniciando para {len(lista_patrones)} patrones...")
    os.makedirs(ruta_output, exist_ok=True)

    for patron in lista_patrones:

        # 1. Buscar archivos para ESTE patrón
        input_models = [
            f for f in glob.glob(os.path.join(ruta_input, "*.xml"))
            if patron.lower() in os.path.basename(f).lower()
        ]

        # Validaciones
        if not input_models:
            print(f"No se encontraron archivos para: '{patron}'")
            continue

        if len(input_models) < 2:
            print(f"Solo se encontró {len(input_models)} modelo para '{patron}'. Se necesitan al menos 2.")
            continue

        print(f"\n========================================")
        print(f"Calculando Jaccard por pares para: {patron.upper()}")
        print(f"Se encontraron {len(input_models)} modelos.")

        # 2. Generar TODOS los pares posibles para este patrón
        couples = list(combinations(input_models, 2))
        print(f"Se evaluarán {len(couples)} combinaciones posibles.")

        pares_resultado = {}
        filas_tabla = []

        # 3. Ejecutar mergem PAR POR PAR
        for modelo_a, modelo_b in couples:
            nombre_a = os.path.basename(modelo_a)
            nombre_b = os.path.basename(modelo_b)

            try:
                results = mergem.merge(
                    [modelo_a, modelo_b],
                    set_objective='merge',
                    exact_sto=False,
                    use_prot=False,
                    extend_annot=False,
                    trans_to_db=None
                )

                # jacc_matrix es 2x2 para un par; el valor de interés
                # es el elemento fuera de la diagonal (comparación entre
                # los dos modelos distintos)
                jacc_matrix = results['jacc_matrix']
                jacc_valor = jacc_matrix[0][1]

                pares_resultado[(nombre_a, nombre_b)] = jacc_valor
                filas_tabla.append({
                    "modelo_1": nombre_a,
                    "modelo_2": nombre_b,
                    "jaccard": jacc_valor
                })

                print(f"  {nombre_a} vs {nombre_b} -> Jaccard = {jacc_valor:.4f}")

            except Exception as e:
                print(f"  Error comparando {nombre_a} vs {nombre_b}: {e}")
                continue

        # 4. Guardar tabla de resultados para este patrón
        tabla_df = pd.DataFrame(filas_tabla)
        nombre_csv = f"jaccard_pares_{patron.lower()}.csv"
        ruta_csv = os.path.join(ruta_output, nombre_csv)
        tabla_df.to_csv(ruta_csv, index=False)
        print(f"Tabla de Jaccard guardada en: {ruta_csv}")

        resultados_totales[patron] = {
            "pares": pares_resultado,
            "tabla": tabla_df
        }

    print("fin")
    return resultados_totales



import glob
import os

def filtrar_bacterias(data_dir="/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/mergem/models"):
    bacterias = []
    for carpeta in sorted(glob.glob(os.path.join(data_dir, "*"))):
        if not os.path.isdir(carpeta):
            continue
        id_bacteria = os.path.basename(carpeta)

        genoma_nt = os.path.join(carpeta, "genome.fna")
        genoma_aa = os.path.join(carpeta, "genome.faa")

        modelos = []

        # --- AQUÍ va el cambio, reemplazando el for anterior ---
        tipos_archivo = {
            "rz_pk_lb_carveme": "carveme",
            "rz_pk_lb_modelseed": "modelseed",
            "rz_pk_lb_gapseq": "gapseq",
        }

        for nombre_archivo, tipo_real in tipos_archivo.items():
            path_modelo = os.path.join(carpeta, f"{nombre_archivo}.xml")
            if os.path.exists(path_modelo):
                modelos.append({
                    "model_id": f"{id_bacteria}_{tipo_real}",
                    "path_to_model": path_modelo,
                    "model_type": tipo_real,
                })
        # --------------------------------------------------------

        if not modelos:
            print(f"{id_bacteria}: no se encontraron modelos")
            continue

        bacterias.append({
            "id_bacteria": id_bacteria,
            "genoma_nt": genoma_nt,
            "genoma_aa": genoma_aa,
            "modelos": modelos,
        })

    return bacterias
import pandas as pd

BIGG_METS_URL = "http://bigg.ucsd.edu/static/namespace/bigg_models_metabolites.txt"


def _load_bigg_metabolites(url: str = BIGG_METS_URL) -> pd.DataFrame:
    """Descarga la tabla de metabolitos de BiGG."""
    df = pd.read_csv(url, sep="\t")
    id_col = 'bigg_id' if 'bigg_id' in df.columns else df.columns[0]
    name_col = 'name' if 'name' in df.columns else df.columns[1]
    return df.rename(columns={id_col: 'bigg_id', name_col: 'name'})


def buscar_metabolitos(nombres, compartimento="_e", top_n=3, url=BIGG_METS_URL):
    """
    Busca IDs de BiGG para una lista de nombres/fórmulas de metabolitos.
    Solo considera coincidencias 'exactas' o que 'empiezan con' el término buscado.
    Los metabolitos sin coincidencia se agregan igual, con bigg_id/name en NaN,
    y se conserva el orden original de la lista de entrada.

    Parameters
    ----------
    nombres : list[str]
        Nombres o fórmulas a buscar (ej. ['glucose', 'ethanol', 'h2o']).
    compartimento : str
        Sufijo del bigg_id a filtrar (ej. '_e' para extracelular).
        Usa None para no filtrar por compartimento.
    top_n : int
        Número máximo de candidatos a devolver por nombre buscado.
    url : str
        URL (o path local) del archivo de metabolitos de BiGG.

    Returns
    -------
    pd.DataFrame con columnas: query, bigg_id, name, match_type
    """
    df = _load_bigg_metabolites(url)

    if compartimento:
        df = df[df['bigg_id'].str.endswith(compartimento, na=False)]

    resultados = []
    for m in nombres:
        nombre_lower = df['name'].str.lower().fillna("")
        m_lower = m.lower()

        # 1) match exacto de nombre completo
        exact = df[nombre_lower == m_lower]
        # 2) el nombre empieza con la búsqueda (ej. 'glucose' -> 'Glucose exchange')
        starts = df[nombre_lower.str.startswith(m_lower) & ~(nombre_lower == m_lower)]

        encontrado = False
        for subset, tipo in [(exact, "exacto"), (starts, "empieza_con")]:
            if not subset.empty:
                encontrado = True
                subset = subset.assign(name_len=subset['name'].str.len()) \
                                .sort_values('name_len') \
                                .drop(columns='name_len')
                subset = subset.head(top_n).copy()
                subset['query'] = m
                subset['match_type'] = tipo
                resultados.append(subset[['query', 'bigg_id', 'name', 'match_type']])

        if not encontrado:
            print(f"⚠️  No se encontraron coincidencias para: '{m}'")
            resultados.append(pd.DataFrame([{
                'query': m,
                'bigg_id': pd.NA,
                'name': pd.NA,
                'match_type': 'no_encontrado'
            }]))

    resultado_final = pd.concat(resultados, ignore_index=True).drop_duplicates(subset=['query', 'bigg_id'], keep='first')

    # Conservar el orden original de `nombres`
    resultado_final['query'] = pd.Categorical(resultado_final['query'], categories=nombres, ordered=True)
    resultado_final = resultado_final.sort_values('query').reset_index(drop=True)

    return resultado_final


# Uso
#medio_names = ['glucose', 'ethanol', 'h2o', 'phosphate']
#final_df = buscar_metabolitos(medio_names)
#print(final_df)

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

