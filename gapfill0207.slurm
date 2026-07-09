#!/bin/bash
#SBATCH --job-name=fill
#SBATCH -o logs/job_%j.log
#SBATCH -e logs/job_%j.error
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G

eval "$(conda shell.bash hook)"
conda activate gapseq

INDIR="/mnt/data/sur/users/mmontante/02_resultados/gapseq_models"
OUTDIR="/mnt/data/sur/users/mmontante/02_resultados/gapseq_fill"
MEDIA="/mnt/data/sur/users/mmontante/01_data/media/LBmed.csv"

mkdir -p "$OUTDIR"
cd "$OUTDIR"

for RXN_FILE in "$INDIR"/*-all-Reactions.tbl; do
    
    # Validar que el archivo realmente exista por si la carpeta está vacía
    [ -e "$RXN_FILE" ] || continue
    
    PREFIX=$(basename "$RXN_FILE")
    PREFIX="${PREFIX%-all-Reactions.tbl}"

    PATH_FILE="$INDIR/${PREFIX}-all-Pathways.tbl"
    TRANS_FILE="$INDIR/${PREFIX}-Transporter.tbl"

    # 1. gapseq draft
    echo "Creando borrador para $PREFIX"
    gapseq draft \
        -r "$RXN_FILE" \
        -t "$TRANS_FILE" \
        -p "$PATH_FILE"

    # 2. gapseq fill
    echo "Ejecutando Gap-filling para $PREFIX"
    gapseq fill \
        -m "${PREFIX}-draft.RDS" \
        -n "$MEDIA" \
        -b 100 \
        -K $SLURM_CPUS_PER_TASK \
        -f xml

    # [Opcional] Si tu versión de gapseq no acepta '-f xml', usa export:
    # Si el comando anterior te da error, elimina '-f xml' y descomenta lo siguiente:
    # gapseq export -m "${PREFIX}-fill.RDS" -f sbml
    echo "=================================================="
    echo "Finalizado $PREFIX: $(date)"
    echo "=================================================="

done
