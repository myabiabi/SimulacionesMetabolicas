#!/bin/bash
#SBATCH --job-name=find
#SBATCH -o /mnt/data/sur/users/mmontante/logs/job_%j.log
#SBATCH -e /mnt/data/sur/users/mmontante/logs/job_%j.error
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=20G

# Activar ambiente de Conda
eval "$(conda shell.bash hook)"
conda activate gapseq

# Rutas
INDIR="/mnt/data/sur/users/mmontante/01_data/rz/protein_files"
OUTDIR="/mnt/data/sur/users/mmontante/02_resultados/gapseq_find"

mkdir -p "$OUTDIR"
cd "$OUTDIR"

# Ciclo 
for GENOME in "$INDIR"/*.{fna,faa}; do

    # Obtener el nombre base (ej. "2643221508.fna" -> "2643221508")
    PREFIX=$(basename "$GENOME")
    PREFIX="${PREFIX%.*}"

    echo "=================================================="
    echo "Modelo actual: $PREFIX"
    echo "=================================================="

    # Paso 1: gapseq find
    echo "Ejecutando gapseq find para: $PREFIX"
    gapseq find \
        -p all \
        -K "$THREADS" \
        "$GENOME"

    # Paso 2: gapseq find-transport
    echo "Ejecutando gapseq find-transport para: $PREFIX"
    gapseq find-transport \
        -K "$THREADS" \
        "$GENOME"

    echo "=================================================="
    echo "Finalizado para $PREFIX: $(date)"
    echo "=================================================="
    
done

echo "=================================================="
echo "Fin"
echo "=================================================="
