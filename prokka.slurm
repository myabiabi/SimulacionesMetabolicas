#!/bin/bash
 #SBATCH --job-name=prokka
 #SBATCH --output=%x.log
 #SBATCH --error=%x.error
 #SBATCH --time=240:00:00
 #SBATCH --cpus-per-task=8
 #SBATCH --mem=8G
  
 # Info del script
 # prueba de prokka
 date
 echo "===== Beginning pipeline ====="
 eval "$(conda shell.bash hook )"
 conda activate prokka

 # comand line 


INPUT_DIR="/mnt/data/sur/users/mmontante/01_raw_data/strain_genomes"
BASE_OUTPUT_DIR="/mnt/data/sur/users/mmontante/04_resultados/rizo/"

# Fecha actual
TODAY=$(date +%F)

# Carpeta de salida
OUTPUT_DIR="${BASE_OUTPUT_DIR}prokka_${TODAY}"

# Debug

# Crear carpeta
mkdir -p "$OUTPUT_DIR"



 
 for file in "$INPUT_DIR"/*.fna; do
     # Nombre base del archivo (sin ruta, sin extensión)
     base=$(basename "$file" .fna)
 
     echo "Anotando genoma: $base"
 
     prokka "$file" \
         --outdir "$OUTPUT_DIR/$base" \
         --prefix "$base" \
         --cpus 8 \
         --kingdom Bacteria
 done


 echo "===== Pipeline done ====="
 date




