#!/usr/bin/env python3
import os
import subprocess
import pandas as pd

# --- CONFIGURACIÓN DE RUTAS Y PARÁMETROS ---
CSV_PATH = "/workspace/modelajemetabolico2026/syncoms.csv"
SCRIPT_ORIGINAL = "/workspace/modelajemetabolico2026/scr/sim_syncom_comets.py"
GEM_PATH = "/workspace/mergem"
OUTDIR_BASE = "./mergem/mergem_all"

# Parámetros fijos para las simulaciones
INITIAL_MASS = "1e-4"
CYCLES = "10"
MEDIA = "lb"

def main():
    # 1. Leer el archivo de comunidades (delimitado por tabuladores)
    if not os.path.exists(CSV_PATH):
        print(f"Error: No se encontró el archivo CSV en {CSV_PATH}")
        return
        
    df = pd.read_csv(CSV_PATH, sep='\t')
    
    # Limpiar nombres de las cepas (quitar comillas y espacios extras de los extremos)
    df.iloc[:, 0] = df.iloc[:, 0].astype(str).str.replace('"', '').str.strip()
    
    lista_cepas = df.iloc[:, 0].tolist()
    columnas_comunidades = df.columns[1:]
    
    print(f"--- Iniciando Orquestador SynComs para COMETS ---")
    print(f"Se procesarán {len(columnas_comunidades)} comunidades de forma integral.\n")

    # 2. Iterar sobre cada columna (Comunidad)
    for com_columna in columnas_comunidades:
        com_nombre_limpio = com_columna.replace('"', '').strip()
        
        # Filtrar las cepas presentes (donde el valor es 1)
        cepas_presentes = []
        for idx, valor in enumerate(df[com_columna].fillna(0)):
            if int(valor) == 1:
                cepas_presentes.append(lista_cepas[idx])
        
        if not cepas_presentes:
            print(f"[AVISO] La comunidad {com_nombre_limpio} está vacía. Saltando...")
            continue
            
        print(f"\n========================================================")
        print(f" Lanzando {com_nombre_limpio} como comunidad unificada")
        print(f" Cepas miembros: {cepas_presentes}")
        print(f"========================================================")
        
        # --- NOTA SOBRE PASAR MÚLTIPLES ARGUMENTOS ---
        # Pasamos las cepas separadas por un espacio dentro del mismo argumento.
        # En tu script original, asegúrate de que `--strains` reciba esto como una lista
        # (usando nargs='+' en argparse) o sepáralas haciendo: cepas = args.strains.split()
        strains_argumento = " ".join(cepas_presentes)
        
        # Definir la carpeta de salida específica para esta comunidad
        outdir_especifico = os.path.join(OUTDIR_BASE, com_nombre_limpio)
        
        # 3. Construir el comando mandando todo junto
        comando = [
            "python3", SCRIPT_ORIGINAL,
            "--gem_path", GEM_PATH,
            "--strains", strains_argumento,  # <-- Aquí van las 5 cepas juntas juntas
            "--initial_mass", INITIAL_MASS,
            "--cycles", CYCLES,
            "--media", MEDIA,
            "--outdir", outdir_especifico
        ]
        
        # Ejecutar la simulación de la comunidad completa
        try:
            print(f"[EJECUTANDO COMETS] Simulando interacciones en {com_nombre_limpio}...")
            resultado = subprocess.run(comando, check=True, text=True, capture_output=True)
            print(f"[ÉXITO] Comunidad {com_nombre_limpio} simulada correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Falló la simulación conjunta para {com_nombre_limpio}.")
            print(f"Detalle del error de ejecución:\n{e.stderr}")

    print("\n--- ¡Simulaciones de comunidades completadas! ---")

if __name__ == "__main__":
    main()