import cometspy as c
import cobra.io
import pandas as pd
import os
import glob 

def comets(ruta_csv_syncoms, patron_xml, threads, cycles, mass, media, newpath):
    # 1. Guardar la ruta original 
    original_path = os.getcwd()
    
    root_path = os.path.abspath(newpath)
    os.makedirs(root_path, exist_ok=True)
    
    # --- CARGAR DATOS DE COMUNIDADES ---
    df = pd.read_csv(ruta_csv_syncoms)
    id_bacterias = df.iloc[:, 0].tolist()
    matriz_bacterias = df.iloc[:, 1:].astype(int).T.values.tolist()
    
    comunidades_finales = []
    for ensayo in matriz_bacterias:
        bacterias_presentes = [nombre for nombre, valor in zip(id_bacterias, ensayo) if valor == 1]
        comunidades_finales.append(bacterias_presentes)

    # --- CARGAR MODELOS A MEMORIA ---
    modelos_base = {}
    lista_archivos = glob.glob(patron_xml)
    
    print(f"Cargando {len(lista_archivos)} modelos SBML...")
    for path_completo in lista_archivos:
        archivo = os.path.basename(path_completo)
        model_id = archivo.split('_')[0]
        try:
            modelos_base[model_id] = cobra.io.read_sbml_model(path_completo)
        except Exception as e:
            print(f"Error cargando {archivo}: {e}")

    # --- PARAMETROS DE SIMULACIÓN ---
    sim_params = c.params()
    sim_params.set_param('numRunThreads', threads)
    sim_params.set_param('maxCycles', cycles)
    sim_params.set_param('writeMediaLog', True)
    sim_params.set_param('MediaLogRate', 1)
    sim_params.set_param('writeTotalBiomassLog', True)
    sim_params.set_param('writeFluxLog', True)
    sim_params.set_param('FluxLogRate', 1)

    initial_mass = [0, 0, mass]

    # --- LOOP DE SIMULACIÓN ---
    for num, lista_nombres in enumerate(comunidades_finales, start=1):
        # VOLVER A LA RAÍZ de resultados para evitar anidamiento
        os.chdir(root_path)
        
        folder_name = f"comunidad_{num}"
        os.makedirs(folder_name, exist_ok=True)
        
        # ENTRAR a la carpeta de la comunidad actual
        os.chdir(folder_name)
        
        print(f"\n>>> Simulando Comunidad {num} en: {os.getcwd()}")
        

        try:
            test_tube = c.layout()
            
            # Cargar modelos y guardar sus nombres para las columnas del CSV
            modelos_agregados = []
            for model_id in lista_nombres:
                if model_id in modelos_base:
                    cobra_copy = modelos_base[model_id].copy()
                    processed_model = c.model(cobra_copy)
                    processed_model.initial_pop = initial_mass
                    test_tube.add_model(processed_model)
                    modelos_agregados.append(model_id) # Se guarda para el encabezado del CSV
                else:
                    print(f"Advertencia: {model_id} no encontrado en archivos XML")

            # --- CONFIGURAR MEDIO DE CULTIVO --- 
            for met, conc in media.items():
                try:
                    test_tube.set_specific_metabolite(met, conc)
                except:
                    pass

            trace_metabolites = ['ca2_e', 'cl_e', 'cobalt2_e', 'cu2_e', 'fe2_e', 'fe3_e', 'h_e', 
                                 'k_e', 'h2o_e', 'mg2_e', 'mn2_e', 'mobd_e', 'na1_e', 'ni2_e', 
                                 'nh4_e', 'o2_e', 'pi_e', 'so4_e', 'zn2_e']

            for i in trace_metabolites:
                if i not in media:
                    try:
                        test_tube.set_specific_metabolite(i, 1000)
                    except:
                        pass
                test_tube.set_specific_static(i, 1000)

            # --- EJECUTAR COMETS ---
            experiment = c.comets(test_tube, sim_params)
            # Al haber usado os.chdir(), COMETS escribe aquí por defecto
            experiment.run(delete_files=False)
            
            # --- PROCESAR Y GUARDAR RESULTADOS ---
            final_models = experiment.total_biomass

            if final_models is not None and not final_models.empty:
                # Calcular tiempo real (ciclos * timeStep)
                time_step = experiment.parameters.all_params['timeStep']
                final_models['t'] = final_models['cycle'] * time_step
                
                # Ajustar nombres de columnas: 'cycle' + nombres bacterias + 't'
                final_models.columns = ['cycle'] + modelos_agregados + ['t']

                # Guardar CSV (ya estamos dentro de Comunidad_X)
                final_models.to_csv(f"comunidad_{num}_biomasa.csv", index=False)
                print(f"Biomasa guardada exitosamente.")
            
            # Guardar metabolitos
            df_metabolites = experiment.get_metabolite_time_series()
            if df_metabolites is not None:
                df_metabolites.to_csv(f"comunidad_{num}_metabolitos.csv", index=False)
                print(f"Metabolitos guardados exitosamente.")

            # Guardar media log
            media_log = experiment.media

            if media_log is not None and not media_log.empty:
                media_log.to_csv(f"comunidad_{num}_media.csv", index=False)
                print("Media log guardado exitosamente.")

        except Exception as e:
            print(f"Error crítico en Comunidad {num}: {e}")

    # 3. Al finalizar, volver a la carpeta donde empezamos
    os.chdir(original_path)
    print(f"\nProceso finalizado. Resultados en: {root_path}")

def media(name="lb", dil=0.1, vol=0.03):
    name = name.lower()  
    res = {}

    if name == "lb":
        res = {
            "na1_e": 186.931246 * vol * dil,
            "cl_e": 171.820893 * vol * dil,
            "ca2_e": 0.0800938 * vol * dil,
            "fe2_e": 0.0456128 * vol * dil,
            "fe3_e": 0.0456128 * vol * dil,
            "so4_e": 0.390397 * vol * dil,
            "pi_e": 4.438244 * vol * dil,
            "mg2_e": 1.746966 * vol * dil,
            "k_e": 2.579814 * vol * dil,
            "ala__L_e": 6.73446 * vol * dil,
            "asp__L_e": 5.897688 * vol * dil,
            "asn__L_e": 0.832583 * vol * dil,
            "glu__L_e": 13.457487 * vol * dil,
            "gln__L_e": 0.136849 * vol * dil,
            "gly_e": 4.262859 * vol * dil,
            "his__L_e": 164.3497 * vol * dil,
            "ile__L_e": 5.336383 * vol * dil,
            "leu__L_e": 7.280351 * vol * dil,
            "lys__L_e": 5.814351 * vol * dil,
            "met__L_e": 1.675513 * vol * dil,
            "phe__L_e": 3.934815 * vol * dil,
            "pro__L_e": 6.601119 * vol * dil,
            "ser__L_e": 2.854614 * vol * dil,
            "thr__L_e": 2.182673 * vol * dil,
            "trp__L_e": 0.514129 * vol * dil,
            "tyr__L_e": 1.048617 * vol * dil,
            "val__L_e": 6.530201 * vol * dil,
            "arg__L_e": 3.61645 * vol * dil,
            "cys__L_e": 0.332928 * vol * dil,
            "cd2_e": 6.67176686E-05 * vol * dil,
            "cobalt2_e": 2.96947381E-04 * vol * dil,
            "cu_e": 0.0052891188 * vol * dil,
            "cu2_e": 0.0052891188 * vol * dil,
            "mn2_e": 0.0110323638 * vol * dil,
            "ni2_e": 0.00207757313 * vol * dil,
            "zn2_e": 0.493722 * vol * dil,
            "ade_e": 0.327092 * vol * dil,
            "gua_e": 0.30603 * vol * dil,
            "csn_e": 0.196213 * vol * dil,
            "ura_e": 0.281475 * vol * dil,
            "nh4_e": 2.301592 * vol * dil,
            "man_e": 1.271121 * vol * dil,
            "pnto__R_e": 0.00241749721 * vol * dil,
            "btn_e": 2.75720165E-05 * vol * dil,
            "ascb__L_e": 8.51692028E-05 * vol * dil,
            "thm_e": 0.00207077178 * vol * dil,
            "nac_e": 0.0163268622 * vol * dil,
            "pydx_e": 0.000443314813 * vol * dil,
            "chol_e": 0.0153595085 * vol * dil,
            "adocbl_e": 2.58226354E-09 * vol * dil,
            "o2_e": 18.2 * vol,
            "h2o_e": 55509.29781 * vol,
            "h_e": 1E-04 * vol
        }
    elif name == "lb+ribose":
        res = media("lb", dil)
        res["2dr5p_e"] = 0.1 * dil

    elif name == "mm":
        res = {
        "na1_e": 895.059287633637 * vol * dil,
        "cl_e": 734.866026900668 * vol * dil,
        "so4_e": 345.797458779573 * vol * dil,
        "ca2_e": 28.837264148495 * vol * dil,
        "k_e": 89.116996725451 * vol * dil,
        "co3_e": 27181.9458806657 * vol * dil,
        "br_e": 67.226890756303 * vol * dil,
        "f_e": 9.587727708533 * vol * dil,
        "mg2_e": 66.795742959209 * vol * dil,
        "fe2_e": 0.01742 * vol * dil,
        "fe3_e": 56.698299480836 * vol * dil,
        "pi_e": 19.990004997501 * vol * dil,
        "nh4_e": 19.990004997501 * vol * dil,
        "no3_e": 0.63108 * vol * dil,
        "ala__L_e": 0.398 * vol * dil,
        "asp__L_e": 0.0756 * vol * dil,
        "asn__L_e": 0.638 * vol * dil,
        "glu__L_e": 0.01368 * vol * dil,
        "gln__L_e": 0.4 * vol * dil,
        "gly_e": 0.0838 * vol * dil,
        "his__L_e": 0.228 * vol * dil,
        "ile__L_e": 0.312 * vol * dil,
        "leu__L_e": 0.314 * vol * dil,
        "lys__L_e": 0.0536 * vol * dil,
        "met__L_e": 0.1574 * vol * dil,
        "phe__L_e": 0.1738 * vol * dil,
        "pro__L_e": 0.1522 * vol * dil,
        "ser__L_e": 0.1344 * vol * dil,
        "thr__L_e": 0.0244 * vol * dil,
        "trp__L_e": 0.0662 * vol * dil,
        "val__L_e": 0.298 * vol * dil,
        "arg__L_e": 0.1492 * vol * dil,
        "cystin_e": 0.00832 * vol * dil,
        "al3_e": 0.0001148 * vol * dil,
        "ba2_e": 0.00000946 * vol * dil,
        "cd2_e": 0.00001334 * vol * dil,
        "cobalt2_e": 0.0000594 * vol * dil,
        "cr3_e": 0.0001186 * vol * dil,
        "ga3_e": 0.00000129 * vol * dil,
        "cu2_e": 0.00099 * vol * dil,
        "mn2_e": 0.00096 * vol * dil,
        "ni2_e": 0.000109 * vol * dil,
        "pb2_e": 0.000001678 * vol * dil,
        "sr2_e": 0.00001256 * vol * dil,
        "vanad_e": 0.000858 * vol * dil,
        "sn2_e": 0.000000758 * vol * dil,
        "zn2_e": 0.0566 * vol * dil,
        "ti4_e": 0.0000626 * vol * dil,
        "mobd_e": 0.0000614 * vol * dil,
        "ade_e": 0.0654 * vol * dil,
        "gua_e": 0.0612 * vol * dil,
        "cyt_e": 0.0392 * vol * dil,
        "ura_e": 0.0562 * vol * dil,
        "nh3_e": 0.488 * vol * dil,
        "cellb_e": 0.00204 * vol * dil,
        "man_e": 0.254 * vol * dil,
        "fol_e": 0.0000508 * vol * dil,
        "pnto__R_e": 0.000484 * vol * dil,
        "btn_e": 0.00000548 * vol * dil,
        "sel_e": 0.000001098 * vol * dil,
        "ascb__L_e": 0.00001704 * vol * dil,
        "thm_e": 0.000414 * vol * dil,
        "ribflv_e": 0.0001062 * vol * dil,
        "nac_e": 0.00326 * vol * dil,
        "pydxn_e": 0.0000886 * vol * dil,
        "cbl1_e": 0.000000000516 * vol * dil,
        "o2": 18.2 * vol,
        "h2o": 55509.2978073827 * vol,
        "h": 0.0001 * vol,
    }
    elif name == "mm+ribose":
        res = media("mm", dil)
        res["2dr5p_e"] = 0.1 * dil
    
    elif name == "mm2":
        res = {
            "na1_e":      0.895059287633637 * vol * dil,
            "cl_e":       0.734866026900668 * vol * dil,
            "so4_e":      0.345797458779573 * vol * dil,
            "ca2_e":      0.028837264148495 * vol * dil,
            "k_e":        0.089116996725451 * vol * dil,
            "mg2_e":      0.066795742959209 * vol * dil,
            "fe2_e":      1.74E-05          * vol * dil,
            "fe3_e":      0.056698299480836 * vol * dil,
            "pi_e":       0.019990004997501 * vol * dil,
            "nh4_e":      0.019990004997501 * vol * dil,
            "no3_e":      0.00063108        * vol * dil,
            "ala__L_e":   0.000398          * vol * dil,
            "asp__L_e":   7.56E-05          * vol * dil,
            "asn__L_e":   0.000638          * vol * dil,
            "glu__L_e":   1.37E-05          * vol * dil,
            "gln__L_e":   0.0004            * vol * dil,
            "gly_e":      8.38E-05          * vol * dil,
            "his__L_e":   0.000228          * vol * dil,
            "ile__L_e":   0.000312          * vol * dil,
            "leu__L_e":   0.000314          * vol * dil,
            "lys__L_e":   5.36E-05          * vol * dil,
            "met__L_e":   0.0001574         * vol * dil,
            "phe__L_e":   0.0001738         * vol * dil,
            "pro__L_e":   0.0001522         * vol * dil,
            "ser__L_e":   0.0001344         * vol * dil,
            "thr__L_e":   2.44E-05          * vol * dil,
            "trp__L_e":   6.62E-05          * vol * dil,
            "val__L_e":   0.000298          * vol * dil,
            "arg__L_e":   0.0001492         * vol * dil,
            "cd2_e":      1.33E-08          * vol * dil,
            "cobalt2_e":  5.94E-08          * vol * dil,
            "cu2_e":      9.9E-07           * vol * dil,
            "mn2_e":      9.6E-07           * vol * dil,
            "ni2_e":      1.09E-07          * vol * dil,
            "zn2_e":      5.66E-05          * vol * dil,
            "mobd_e":     6.14E-08          * vol * dil,
            "ade_e":      6.54E-05          * vol * dil,
            "gua_e":      6.12E-05          * vol * dil,
            "ura_e":      5.62E-05          * vol * dil,
            "cellb_e":    2.04E-06          * vol * dil,
            "man_e":      0.000254          * vol * dil,
            "fol_e":      5.08E-08          * vol * dil,
            "pnto__R_e":  4.84E-07          * vol * dil,
            "btn_e":      5.48E-09          * vol * dil,
            "sel_e":      1.10E-09          * vol * dil,
            "ascb__L_e":  1.70E-08          * vol * dil,
            "thm_e":      4.14E-07          * vol * dil,
            "ribflv_e":   1.06E-07          * vol * dil,
            "nac_e":      3.26E-06          * vol * dil,
            "o2_e":       0.0182            * vol,
            "h2o_e":      55.5092978073827  * vol,
            "h_e":        1E-07             * vol,
        }
    elif name == "mm2+ribose":
        res = media("mm2", vol, dil)
        res["2dr5p_e"] = 0.1 * vol * dil

    else:
        raise ValueError(f"Unrecognized media '{name}'. Supported: 'lb', 'mm', 'mm2', 'mm+ribose'")

    return res


def load_strains(layout, models, initial_mass = 1e-8):
    for strain, gem in models.items():
        # print(f"==============Cargando modelo para {strain} desde {gem}==============")
        gem_i = cobra.io.read_sbml_model(gem)
        # print(f"=========================Modelo cargado para {strain}==============")
        gem_i = c.model(gem_i)
        # gem_i.optimizer = "GLOP"
        # print(f"=========================Modelo procesado para {strain}==============")
        gem_i.id = strain
        # print(f"=========================ID establecido para {strain}==============")
        gem_i.initial_pop = [0, 0, initial_mass]
        # print(f"=========================Biomasa inicial para {strain}==============")
        layout.add_model(gem_i)
        # print(f"=========================Modelo añadido {strain}==============")

    return layout
    
def set_sim_params(args):
    # Def simulation parameters
    sim_params = c.params()
    # print(sim_params.show_params().to_string())

    # Set sim parameters
    sim_params.set_param("writeBiomassLog", True) 
    sim_params.set_param("BiomassLogName", os.path.join(args.outdir, "biomass.txt"))
    sim_params.set_param("BiomassLogRate", 1) 

    sim_params.set_param("writeFluxLog", True) 
    sim_params.set_param("FluxLogName", os.path.join(args.outdir, "flux.txt"))
    sim_params.set_param("FluxLogRate", 1)

    sim_params.set_param("writeMediaLog", True) 
    sim_params.set_param("MediaLogName", os.path.join(args.outdir, "media.txt"))
    sim_params.set_param("MediaLogRate", 1)

    sim_params.set_param("writeTotalBiomassLog", True) 
    sim_params.set_param("TotalBiomassLogName", os.path.join(args.outdir, "total_biomass.txt"))
    sim_params.set_param("totalBiomassLogRate", 1)

    sim_params.set_param("writeVelocityMultiConvLog", False) 
    sim_params.set_param("velocityMultiConvLogName", os.path.join(args.outdir, "velocity.txt"))
    sim_params.set_param("velocityMultiConvLogRate", 1)

    sim_params.set_param("numRunThreads", args.threads)
    # sim_params.set_param("randomSeed", args.seed)
    sim_params.set_param("timeStep", 0.1) # hr
    sim_params.set_param("maxCycles", args.cycles)
    sim_params.set_param("maxSpaceBiomass", 10) # gr DW
    sim_params.set_param("minSpaceBiomass", 1e-11) # gr DW
    sim_params.set_param("spaceWidth", 3.107233) # cm

    return sim_params
