import os
import csv
import cobra

def variables_totales(gem_path, output_dir):

    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "variables_totales.csv")

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
    

import mergem

def mergem_function(ruta_input, ruta_output, nombre_salida, *modelos):
    """
    Fusiona un número variable de modelos metabólicos usando mergem.
    
    Parameters:
    -----------
    ruta_input : str
        Ruta de la carpeta donde están guardados los archivos XML de entrada.
    ruta_output : str
        Ruta de la carpeta donde se guardará el modelo consenso final.
    nombre_salida : str
        Nombre del archivo XML resultante (ej. 'modelo_consenso_mycobacterium.xml').
    *modelos : str
        Nombres de los archivos de los modelos, separados por comas. 
        Soporta nombres con o sin la extensión '.xml'.
    """
    input_models = []
    
    # 1. Procesar y verificar cada modelo ingresado
    for modelo in modelos:
        # Si el usuario no escribió la extensión .xml, se agrega por defecto
        if not modelo.lower().endswith('.xml'):
            modelo += '.xml'
            
        ruta_completa = os.path.join(ruta_input, modelo)
        
        # Validar si el archivo realmente existe en la ruta dada
        if not os.path.exists(ruta_completa):
            raise FileNotFoundError(f"Error: No se encontró el archivo '{modelo}' en la ruta: {ruta_input}")
            
        input_models.append(ruta_completa)
    
    if len(input_models) < 2:
        raise ValueError("Se necesitan al menos 2 modelos para poder generar un consenso.")

    print(f"Iniciando la fusión de {len(input_models)} modelos...")
    for i, path in enumerate(input_models, start=1):
        print(f"  Modelo {i}: {os.path.basename(path)}")
    
    # 2. Ejecutar la fusión con mergem
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
        print(f"Error durante la ejecución de mergem: {e}")
        return None

    # 3. Extraer el modelo fusionado y métricas básicas
    merged_model = results['merged_model']
    num_met_merged = results['num_met_merged']
    num_reac_merged = results['num_reac_merged']

    print(f"Total de Metabolitos: {num_met_merged}")
    print(f"Total de Reacciones: {num_reac_merged}")

    # 4. Guardar el modelo consenso en la carpeta destino especificada
    os.makedirs(ruta_output, exist_ok=True) # Crea la carpeta si no existe
    
    # Asegurar extensión .xml en el archivo de salida también
    if not nombre_salida.lower().endswith('.xml'):
        nombre_salida += '.xml'
        
    output_path = os.path.join(ruta_output, nombre_salida)
    
    cobra.io.write_sbml_model(merged_model, output_path)
    print(f"Modelo consenso guardado exitosamente en: {output_path}\n")
    
    return results

