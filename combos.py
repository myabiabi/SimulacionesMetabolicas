import os
import subprocess
from itertools import combinations

# --- CONFIGURACIÓN DE RUTAS Y PARÁMETROS ---
SCRIPT_ORIGINAL = "/mnt/data/sur/users/mmontante/SimulacionesMetabolicas/sim_syncom_comets.py"
GEM_PATH = "/mnt/data/sur/users/mmontante/02_resultados/rz/models/cv_final"
OUTDIR_BASE = "02_resultados/rz/combinaciones"

if not os.path.exists(OUTDIR_BASE):
    os.makedirs(OUTDIR_BASE)

CYCLES = "10000"
MEDIA = "lb"
MEDIA_DIL = "0.1"
MEDIA_VOL = "0.03"

def main():
    if not os.path.exists(GEM_PATH):
        print(f"Error: No se encontró la carpeta de modelos en {GEM_PATH}")
        return

    # 1. Obtener los nombres de las cepas directamente de los archivos de la carpeta
    # Filtramos para asegurarnos de leer solo archivos de modelos (ej: .xml) y quitarles la extensión
    modelos_archivos = [f for f in os.listdir(GEM_PATH) if f.endswith('.xml')]
    cepas_disponibles = [os.path.splitext(f)[0] for f in modelos_archivos]

    if not cepas_disponibles:
        print(f"Error: No se encontraron archivos .xml en {GEM_PATH}")
        return

    print(f"Modelos detectados ({len(cepas_disponibles)}): {cepas_disponibles}\n")

    # 2. Iterar por tamaños de combinación (2 = pares, 3 = tríos, 4 = cuartetos)
    for tamaño in range(2, 5):
        # Generar todas las combinaciones posibles de la lista total de cepas
        combos = list(combinations(cepas_disponibles, tamaño))
        print(f"Lanzando {len(combos)} combinaciones de tamaño {tamaño}...")

        for combo in combos:
            # Crear un identificador único para la carpeta del combo
            combo_nombre = "_".join(combo)
            outdir_especifico = os.path.join(OUTDIR_BASE, f"tamanho_{tamaño}", combo_nombre)

            # 3. Construir el comando para el script original
            comando = [
                "python3", SCRIPT_ORIGINAL,
                "--gem_path", GEM_PATH,
            ]

            comando.append("--strains")
            comando.extend(combo) 

            comando.extend([
                "--cycles", CYCLES,
                "--media", MEDIA,
                "--media_dil", MEDIA_DIL,
                "--media_vol", MEDIA_VOL,
                "--outdir", outdir_especifico
            ])

            # Ejecutar la simulación
            try:
                print(f"[EJECUTANDO COMETS] Combo {combo_nombre}...")
                resultado = subprocess.run(comando, check=True, text=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] Falló la simulación para {combo_nombre}.")
                print(f"Detalle del error:\n{e.stderr}")

    print("\n--- ¡Todas las combinaciones globales completadas exitosamente! ---")

if __name__ == "__main__":
    main()

