
from functions import mergem_function

carpeta_modelos = "/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/models"
carpeta_salida = "/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/models_mergem"
    
mergem_function(
    carpeta_modelos,
    carpeta_salida,
    "modelo_mergem_consenso_bacillus.xml",
    "rz_na_cv_lb_bacillus",
    "rz_na_rt_kb_lb_bacillus_sp"             
)