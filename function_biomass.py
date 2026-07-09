# -------------------------------------------------------------------------------------------------
import cometspy as c
import cobra.io
import pandas as pd
import os
import glob

def biomass_comunidades_rizo(ruta_csv_syncoms, patron_xml, 
                             threads, cycles, mass, media, folder_resultados):
    # --- CONFIGURACIÓN ---
    sim_params = c.params()
    sim_params.set_param('numRunThreads', threads)
    sim_params.set_param('maxCycles', cycles)
    
    # Formato de población inicial para COMETS (lista de listas)
    initial_mass_fmt = [[0, 0, mass]]
    os.makedirs(folder_resultados, exist_ok=True)

    # --- LECTURA DE DATOS ---
    df = pd.read_csv(ruta_csv_syncoms)
    # Primera columna: IDs de bacterias (ej: ST00046, STECOLI)
    id_bacterias_csv = [str(x).strip() for x in df.iloc[:, 0].tolist()]
    # Resto de columnas: Matriz binaria de comunidades (R1, R2...)
    matriz_bacterias = df.iloc[:, 1:].astype(int).T.values.tolist()
    
    comunidades_finales = []
    for ensayo in matriz_bacterias:
        bacterias_presentes = [nombre for nombre, valor in zip(id_bacterias_csv, ensayo) if valor == 1]
        comunidades_finales.append(bacterias_presentes)

    # --- CARGA DE MODELOS A MEMORIA ---
    modelos_base = {}
    lista_archivos = glob.glob(patron_xml)
    
    print(f"--- Cargando {len(lista_archivos)} modelos SBML a memoria ---")
    for path_completo in lista_archivos:
        archivo = os.path.basename(path_completo)
        # Extrae ID antes del guion bajo (ej: STECOLI)
        model_id_xml = archivo.split('_')[0].strip()
        try:
            modelos_base[model_id_xml] = cobra.io.read_sbml_model(path_completo)
        except Exception as e:
            print(f"Error cargando {archivo}: {e}")

    # --- CICLO DE SIMULACIÓN ---
    # Aquí es donde se imprime la comunidad que va saliendo
    for num, lista_nombres_csv in enumerate(comunidades_finales, start=1):    
        test_tube = c.layout()
        print(f"\n[INICIO] >>> Procesando Comunidad {num}: {lista_nombres_csv}")
        
        try:
            modelos_agregados = []
            for id_buscado in lista_nombres_csv:
                # Búsqueda de coincidencia
                id_match = None
                if id_buscado in modelos_base:
                    id_match = id_buscado
                else:
                    # Búsqueda flexible (por si acaso)
                    for id_xml in modelos_base.keys():
                        if id_buscado in id_xml or id_xml in id_buscado:
                            id_match = id_xml
                            break
                
                if id_match:
                    cobra_copy = modelos_base[id_match].copy()
                    processed_model = c.model(cobra_copy)
                    processed_model.initial_pop = initial_mass_fmt
                    test_tube.add_model(processed_model)
                    modelos_agregados.append(id_buscado)
                else:
                    print(f"   ! Advertencia: No se encontró modelo para '{id_buscado}'")

            # --- CONFIGURACIÓN DEL MEDIO ---
            for met, conc in media.items():
                try:
                    test_tube.set_specific_metabolite(met, conc)
                except:
                    pass

            # Nutrientes traza básicos
            trace = ['ca2_e', 'cl_e', 'cobalt2_e', 'cu2_e', 'fe2_e', 'fe3_e', 'h_e', 
                     'k_e', 'h2o_e', 'mg2_e', 'mn2_e', 'mobd_e', 'na1_e', 'ni2_e', 
                     'nh4_e', 'o2_e', 'pi_e', 'so4_e', 'zn2_e']
            for i in trace:
                if i not in media:
                    test_tube.set_specific_metabolite(i, 1000)
                test_tube.set_specific_static(i, 1000)

            # --- CORRER SIMULACIÓN ---
            experimet = c.comets(test_tube, sim_params)
            experimet.run()

            # --- GUARDAR RESULTADOS ---
            final_models = experimet.total_biomass
            if final_models is not None and not final_models.empty:
                # Añadir columna de tiempo real
                final_models['t'] = final_models['cycle'] * experimet.parameters.all_params['timeStep']
                # Renombrar columnas
                final_models.columns = ['cycle'] + modelos_agregados + ['t']
                
                csv_file_name = os.path.join(folder_resultados, f"comunidad_{num}.csv")
                final_models.to_csv(csv_file_name, index=False)
                print(f"[ÉXITO] Comunidad {num} guardada correctamente.")
            else:
                print(f"[AVISO] Comunidad {num} terminó sin biomasa.")

        except Exception as e:
            print(f"[FALLO] Error en Comunidad {num}: {e}")
