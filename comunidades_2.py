import os
import subprocess
import csv

# --- RUTAS Y PARÁMETROS ---
CSV_PATH = "/mnt/data/sur/users/mmontante/01_data/rz/syncoms.csv"
SCRIPT = "/mnt/data/sur/users/mmontante/SimulacionesMetabolicas/sim_syncom_comets.py"
GEM_PATH = "/mnt/data/sur/users/mmontante/02_resultados/rz/models/final_models"


OUTDIR_BASE = "02_resultados/rz/110926simulaciones"

if not os.path.exists(OUTDIR_BASE):
	os.makedirs(OUTDIR_BASE)

# Parámetros fijos para las simulaciones

CYCLES = "5000"
MEDIA = "lb2"
#MEDIA_DIL = "0.1"
#MEDIA_VOL = "0.03"


print(f"\n========================================================")
print(f" Iniciando lectura de comunidades ")
print(f"========================================================")

def main():
    if not os.path.exists(CSV_PATH):
        print(f"Error: No se encontró el archivo en {CSV_PATH}")
        return

    print(f"--- Iniciando SynComs para COMETS ---")

    # 1. Leer el archivo usando el 'csv'
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

    print(f"Se procesarán {len(columnas_comunidades)}")

    # 2. Iterar sobre las comunidades
    for com_nombre, cepas_presentes in comunidades_dict.items():
        
        if not cepas_presentes:
            print(f"La comunidad {com_nombre} está vacía en el archivo. Saltando...")
            continue
            
        print(f"\n========================================================")
        print(f" {com_nombre} ")
        print(f" Cepas miembros: {cepas_presentes}")
        print(f"========================================================")
        
        # Ruta de salida relativa (ej: "./com3")
        outdir_especifico = os.path.join(OUTDIR_BASE, com_nombre)
        
	
        print(f" Iniciando simulaciones ")
        

        # 3. Instrucciones COMETS
        comando = [
            "python3", SCRIPT,
            "--gem_path", GEM_PATH,
        ]
        
        comando.append("--strains")
        comando.extend(cepas_presentes) 
        
        comando.extend([
            "--cycles", CYCLES,
            "--media", MEDIA,
            "--outdir", outdir_especifico
        ])
        
        # Ejecutar la simulación
        try:
            print(f"Simulando interacciones en {com_nombre}...")
            resultado = subprocess.run(comando, check=True, text=True, capture_output=True)
            print(f"Comunidad {com_nombre} correcto.")
        except subprocess.CalledProcessError as e:
            print(f"Falló la simulación para {com_nombre}.")

    print("\n--- Simulaciones de comunidades completadas exitosamente ---")

if __name__ == "__main__":
    main()
