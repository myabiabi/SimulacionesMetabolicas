import os
import subprocess
import csv

# --- CONFIGURACIÓN DE RUTAS Y PARÁMETROS ---
CSV_PATH = "/mnt/data/sur/users/mmontante/01_data/rz/syncoms.csv"
SCRIPT_ORIGINAL = "/mnt/data/sur/users/mmontante/SimulacionesMetabolicas/sim_syncom_comets.py"
GEM_PATH = "/mnt/data/sur/users/mmontante/02_resultados/rz/models/cv_final"

# CAMBIO CRUCIAL: Dejamos esto relativo porque tu script original 
# ya se encarga de concatenarlo con la ruta base interna (/mnt/data/sur/users/mmontante/)

OUTDIR_BASE = "02_resultados/rz/com"

if not os.path.exists(OUTDIR_BASE):
	os.makedirs(OUTDIR_BASE)

# Parámetros fijos para las simulaciones

CYCLES = "10000"
MEDIA = "lb"
MEDIA_DIL = "0.1"
MEDIA_VOL = "0.03"

def main():
    if not os.path.exists(CSV_PATH):
        print(f"Error: No se encontró el archivo en {CSV_PATH}")
        return

    print(f"--- Iniciando Orquestador SynComs para COMETS (Modo Nativo) ---")

    # 1. Leer el archivo usando el módulo nativo 'csv'
    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
        lector = csv.DictReader(f, delimiter='\t')
        
        columnas_comunidades = [col.replace('"', '').strip() for col in lector.fieldnames[1:]]
        comunidades_dict = {com: [] for com in columnas_comunidades}
        
        for fila in lector:
            cepa_nombre = fila[lector.fieldnames[0]].replace('"', '').strip()
            
            for com in columnas_comunidades:
                clave_original = next(k for k in fila.keys() if com in k)
                valor = fila[clave_original].replace('"', '').strip()
                
                if valor == '1':
                    comunidades_dict[com].append(cepa_nombre)

    print(f"Se procesarán {len(columnas_comunidades)} comunidades de forma integral.\n")

    # 2. Iterar sobre las comunidades mapeadas para lanzar las simulaciones
    for com_nombre, cepas_presentes in comunidades_dict.items():
        
        if not cepas_presentes:
            print(f"[AVISO] La comunidad {com_nombre} está vacía en el archivo. Saltando...")
            continue
            
        print(f"\n========================================================")
        print(f" Lanzando {com_nombre} como comunidad unificada")
        print(f" Cepas miembros: {cepas_presentes}")
        print(f"========================================================")
        
        # Construir la ruta de salida relativa (ej: "./com3")
        outdir_especifico = os.path.join(OUTDIR_BASE, com_nombre)
        
        # 3. Construir el comando expandiendo las cepas dinámicamente
        comando = [
            "python3", SCRIPT_ORIGINAL,
            "--gem_path", GEM_PATH,
        ]
        
        comando.append("--strains")
        comando.extend(cepas_presentes) 
        
        comando.extend([
            "--cycles", CYCLES,
            "--media", MEDIA,
            "--media_dil", MEDIA_DIL,
            "--media_vol", MEDIA_VOL,
            "--outdir", outdir_especifico
        ])
        
        # Ejecutar la simulación
        try:
            print(f"[EJECUTANDO COMETS] Simulando interacciones en {com_nombre}...")
            resultado = subprocess.run(comando, check=True, text=True, capture_output=True)
            print(f"[ÉXITO] Comunidad {com_nombre} simulada correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Falló la simulación conjunta para {com_nombre}.")
            print(f"Detalle del error de ejecución:\n{e.stderr}")

    print("\n--- ¡Simulaciones de comunidades completadas exitosamente! ---")

if __name__ == "__main__":
    main()
