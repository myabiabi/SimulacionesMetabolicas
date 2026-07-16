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
OUTDIR="/mnt/data/sur/users/mmontante/02_resultados/cc/gapseq/gapseq_fill"
MEDIA="/mnt/data/sur/users/mmontante/01_data/media/LBmed.csv"

mkdir -p "$OUTDIR"
cd "$OUTDIR"

for RXN_FILE in "$INDIR"/*-all-Reactions.tbl; do
    
    [ -e "$RXN_FILE" ] || continue
    
    PREFIX=$(basename "$RXN_FILE")
    PREFIX="${PREFIX%-all-Reactions.tbl}"

    PATH_FILE="$INDIR/${PREFIX}-all-Pathways.tbl"
    TRANS_FILE="$INDIR/${PREFIX}-Transporter.tbl"

    echo "=================================================="
    echo "Procesando: $PREFIX"
    echo "=================================================="

    # 1. gapseq draft (Forzamos el nombre de salida con -u para evitar errores)
    echo "Creando borrador para $PREFIX..."
    gapseq draft \
        -r "$RXN_FILE" \
        -t "$TRANS_FILE" \
        -p "$PATH_FILE" \
        -u "$PREFIX"

    # NOTA: El comando anterior creará un archivo llamado "${PREFIX}-draft.RDS"
    if [ ! -f "${PREFIX}-draft.RDS" ]; then
        echo "ERROR: No se pudo crear ${PREFIX}-draft.RDS. Saltando..."
        continue
    fi

    # 2. gapseq fill
    echo "Ejecutando Gap-filling para $PREFIX..."
    gapseq fill \
        -m "${PREFIX}-draft.RDS" \
        -n "$MEDIA" \
        -b 100 \
        -K $SLURM_CPUS_PER_TASK

    # 3. Exportar explícitamente a XML (SBML)
    # 'gapseq fill' genera "${PREFIX}-fill.RDS". Usamos 'export' para obtener el XML real.
    if [ -f "${PREFIX}-fill.RDS" ]; then
        echo "Exportando modelo final a XML para $PREFIX..."
        gapseq export \
            -m "${PREFIX}-fill.RDS" \
            -f sbml
    else
        echo "ERROR: El gap-filling falló y no generó ${PREFIX}-fill.RDS"
    fi

    echo "Finalizado $PREFIX: $(date)"
    echo "=================================================="

done
