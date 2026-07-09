#!/bin/bash
#SBATCH --job-name=g_fill
#SBATCH -o logs/fill_%j.log
#SBATCH -e logs/fill_%j.error
#SBATCH --time=36:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=45G

eval "$(conda shell.bash hook)"
conda activate gapseq

# Aquí es donde guardaste los archivos .tbl del paso 'find'
INDIR="/mnt/data/sur/users/mmontante/02_resultados/gapseq_find"
# Aquí es donde quieres tus modelos finales (.xml)
OUTDIR="/mnt/data/sur/users/mmontante/02_resultados/gapseq_fill"
MEDIA="/mnt/data/sur/users/mmontante/01_data/media/LBmed.csv"

mkdir -p "$OUTDIR"
cd "$OUTDIR"

for RXN_FILE in "$INDIR"/*-all-Reactions.tbl; do
    
    [ -e "$RXN_FILE" ] || continue
    
    PREFIX=$(basename "$RXN_FILE")
    PREFIX="${PREFIX%-all-Reactions.tbl}"

    # Filtro de seguridad para ignorar archivos basura de R
    if [[ "$PREFIX" == "["* || "$PREFIX" == "eval"* || "$PREFIX" == ".data.table"* ]]; then
        continue
    fi

    # CONTROL DE AVANCE: Si ya existe el modelo final rellenado, se lo salta
    if [ -f "${PREFIX}-fill.xml" ] || [ -f "${PREFIX}-fill.RDS" ]; then
        echo "El modelo final para $PREFIX ya existe. Saltando..."
        continue
    fi

    PATH_FILE="$INDIR/${PREFIX}-all-Pathways.tbl"
    TRANS_FILE="$INDIR/${PREFIX}-Transporter.tbl"

    # Generar el borrador solo si no se ha creado antes
    if [ ! -f "${PREFIX}-draft.RDS" ]; then
        echo "==> Creando borrador para $PREFIX"
        gapseq draft \
            -r "$RXN_FILE" \
            -t "$TRANS_FILE" \
            -p "$PATH_FILE"
    fi

    # El paso crítico: Gap-filling con más memoria y bandera -k correcta
    echo "==> Ejecutando Gap-filling para $PREFIX: $(date)"
    gapseq fill \
        -m "${PREFIX}-draft.RDS" \
        -n "$MEDIA" \
        -k $SLURM_CPUS_PER_TASK \
        -f xml

    echo "=================================================="
    echo "Finalizado exitosamente $PREFIX: $(date)"
    echo "=================================================="

done
