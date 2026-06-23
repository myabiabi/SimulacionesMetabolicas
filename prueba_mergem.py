
from functions import mergem_function

# Definir tus carpetas de manera explícita
carpeta_modelos = "/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/models"
carpeta_salida = "/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/models_mergem"
    
#  FORMA CORRECTA 1: Manteniendo el orden posicional
mergem_function(
    carpeta_modelos,
    carpeta_salida,
    "modelo_mergem_consenso_bacillus.xml", # Solo el string, sin 'nombre_salida='
    "rz_na_cv_lb_bacillus",
    "rz_na_rt_kb_lb_bacillus_sp"             
)