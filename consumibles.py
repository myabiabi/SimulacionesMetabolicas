# import cobra
# import pandas as pd
# import glob

# # Ruta a tus modelos
# ruta_modelos = '/media/abigaylmontantearenas/UBUNTU 24_0/abi/models/cc_pk_cv_mm/*.xml'
# archivos = glob.glob(ruta_modelos)

# # Lista para guardar resultados
# resultados = []

# for archivo in archivos:
#     try:
#         modelo = cobra.io.read_sbml_model(archivo)
#         nombre = archivo.split('/')[-1].replace('.xml', '')
        
#         for rxn in modelo.exchanges:
#             if rxn.lower_bound < 0:
#                 met = list(rxn.metabolites.keys())[0]
#                 resultados.append({
#                     'cepa': nombre,
#                     'met_id': met.id,
#                     'met_nombre': met.name,
#                     'lower_bound': rxn.lower_bound
#                 })
#     except Exception as e:
#         print(f"Error cargando {archivo}: {e}")

# # Convertir a dataframe
# df = pd.DataFrame(resultados)
# print(df.head(20))
# print(f"\nTotal filas: {len(df)}")
# print(f"Total cepas: {df['cepa'].nunique()}")
# print(f"Total metabolitos únicos: {df['met_id'].nunique()}")

# # Guardar
# df.to_csv('/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/1708/marinas.csv', index=False)



# import pandas as pd

# # Cargar metabolitos consumibles de tus 10 modelos
# df_consumibles = pd.read_csv('/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/1708/marinas.csv')

# # Tu medio experimental en BiGG IDs
# medio_experimental = {
#     "na1_e", "cl_e", "so4_e", "ca2_e",
#     "k_e", "co3_e", "br_e", "f_e",
#     "mg2_e", "fe2_e", "fe3_e", "pi_e",
#     "nh4_e", "no3_e", "ala__L_e", "asp__L_e",
#     "asn__L_e", "glu__L_e", "gln__L_e", "gly_e",
#     "his__L_e", "ile__L_e", "leu__L_e", "lys__L_e",
#     "met__L_e", "phe__L_e", "pro__L_e", "ser__L_e",
#     "thr__L_e", "trp__L_e", "val__L_e", "arg__L_e",
#     "cystin_e", "al3_e", "ba2_e", "cd2_e",
#     "cobalt2_e", "cr3_e", "ga3_e", "cu2_e",
#     "mn2_e", "ni2_e", "pb2_e", "sr2_e",
#     "vanad_e", "sn2_e", "zn2_e", "ti4_e",
#     "mobd_e", "ade_e", "gua_e", "cyt_e",
#     "ura_e", "nh3_e", "cellb_e", "man_e",
#     "fol_e", "pnto__R_e", "btn_e", "sel_e",
#     "ascb__L_e", "thm_e", "ribflv_e", "nac_e",
#     "pydxn_e", "cbl1_e"
# }

# # Todos los consumibles de las 10 cepas (unión)
# todos_consumibles = set(df_consumibles['met_id'].unique())

# # Grupo 1 — útiles: están en el medio Y alguna cepa puede consumirlos
# utiles = medio_experimental & todos_consumibles
# print(f"Metabolitos ÚTILES ({len(utiles)}):")
# for m in sorted(utiles):
#     print(f"  {m}")

# # Grupo 2 — irrelevantes: están en el medio pero ninguna cepa los consume
# irrelevantes = medio_experimental - todos_consumibles
# print(f"\nMetabolitos IRRELEVANTES ({len(irrelevantes)}):")
# for m in sorted(irrelevantes):
#     print(f"  {m}")

# # Grupo 3 — faltantes: las cepas pueden consumirlos pero no están en el medio
# faltantes = todos_consumibles - medio_experimental
# print(f"\nMetabolitos FALTANTES en el medio ({len(faltantes)}):")
# for m in sorted(faltantes):
#     print(f"  {m}")

# # Guardar resultados
# pd.DataFrame({'metabolito': sorted(utiles), 'grupo': 'util'}).to_csv(
#     '/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/1708/comparacion_medio_mm.csv', index=False)

import pandas as pd

# Cargar CSV con separador correcto
medio_csv = pd.read_csv(
    '/home/abigaylmontantearenas/Documents/proyecto_tesis/01_data/media/mediomarino_recetareal.csv',
    sep='\t'
)

# Renombrar columnas
medio_csv.columns = ['concentracion', 'unit', 'met_id']

# Convertir a diccionario
medio_dict = dict(zip(medio_csv['met_id'], medio_csv['concentracion']))

# Cargar metabolitos consumibles
df_consumibles = pd.read_csv('/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/1708/marinas.csv')
todos_consumibles = set(df_consumibles['met_id'].unique())

# Filtrar solo metabolitos útiles
medio_final = {k: v for k, v in medio_dict.items() if k in todos_consumibles}

print(f"Metabolitos en el medio marino: {len(medio_dict)}")
print(f"Metabolitos útiles para tus modelos: {len(medio_final)}")
print("\nMedio final para COMETS:")
for met, conc in sorted(medio_final.items()):
    print(f"  '{met}': {conc},")

# Guardar
pd.DataFrame({
    'met_id': list(medio_final.keys()),
    'concentracion': list(medio_final.values())
}).to_csv('/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/1708/medio_marino_comets.csv', index=False)