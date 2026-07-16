#!/bin/bash
#SBATCH --job-name=fill
#SBATCH -o logs/job_%j.log
#SBATCH -e logs/job_%j.error
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G

eval "$(conda shell.bash hook)"
conda activate gapseq

INDIR="/mnt/data/sur/users/mmontante/02_resultados/cc/gapseq/gapfind"
OUTDIR="/mnt/data/sur/users/mmontante/02_resultados/cc/gapseq_fill"
MEDIA="/mnt/data/sur/users/mmontante/01_data/media/LBmed.csv"

mkdir -p "$OUTDIR"
cd "$OUTDIR"

for RXN_FILE in "$INDIR"/*-all-Reactions.tbl; do
    
    
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

    for DRAFT in *-draft.RDS; do
    [ -e "$DRAFT" ] || continue
    PREFIX="${DRAFT%-draft.RDS}"
    echo "=================================================="
    echo "Procesando: $PREFIX — $(date)"
    echo "=================================================="

    # ---- Gap filling ----
    echo ">>> Gap filling: $PREFIX"
    gapseq fill \
        -m "$DRAFT" \
        -n "$MEDIA" \
        -c "${PREFIX}-rxnWeights.RDS" \
        -g "${PREFIX}-rxnXgenes.RDS" \
        -b 100

    # ---- Exportar a SBML/XML ----
    echo ">>> Exportando a XML: $PREFIX"
    gapseq export \
        -m "${PREFIX}-fill.RDS" \
        -f sbml \
        -o "${PREFIX}-model.xml"

    echo ">>> Listo: $PREFIX — $(date)"
done

echo "¡Proceso completo!"








