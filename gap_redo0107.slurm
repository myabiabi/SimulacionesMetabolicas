#!/bin/bash
#SBATCH --job-name=REDO
#SBATCH -o logs/redo_%j.log
#SBATCH -e logs/redo_%j.error
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=20G

# Activar ambiente
eval "$(conda shell.bash hook)"
conda activate gapseq

# ==========================
# Configuración
# ==========================
# Carpeta original de tus genomas de entrada (.fna o .faa)
INDIR="/mnt/data/sur/users/mmontante/01_data/cc/raw_data"

# Carpeta de salida (donde están tus tablas actuales)
OUTDIR="/mnt/data/sur/users/mmontante/02_resultados/cc/gapseq/gapfind"

# Forzar el uso exacto de los 8 cores de Slurm
THREADS=$SLURM_CPUS_PER_TASK

mkdir -p "$OUTDIR"
cd "$OUTDIR"

# ==========================
# Ciclo de Corrección
# ==========================

for GENOME in "$INDIR"/*.{fna,faa,fasta}; do
    
    [ -e "$GENOME" ] || continue

    PREFIX=$(basename "$GENOME")
    PREFIX="${PREFIX%.*}"

    echo "=================================================="
    echo "RE-EJECUTANDO: $PREFIX"
    echo "Inicio: $(date)"
    echo "=================================================="

    # Paso 1: gapseq find (Corregido el pase de THREADS)
    echo ">>> Running gapseq find..."
    gapseq find \
        -p all \
        -K $THREADS \
        "$GENOME"

    # Paso 2: gapseq find-transport (Corregido el pase de THREADS)
    echo ">>> Running gapseq find-transport..."
    gapseq find-transport \
        -K $THREADS \
        "$GENOME"

    echo "=================================================="
    echo "Finalizado $PREFIX: $(date)"
    echo "=================================================="
done

echo "¡Re-predicción completa!"
