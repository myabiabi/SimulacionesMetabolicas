#!/bin/bash
#SBATCH --job-name=fill_export
#SBATCH -o /mnt/data/sur/users/mmontante/logs/fill_export_%j.log
#SBATCH -e /mnt/data/sur/users/mmontante/logs/fill_export_%j.error
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G

eval "$(conda shell.bash hook)"
conda activate gapseq

WORKDIR="/mnt/data/sur/users/mmontante/02_resultados/gapseq_fill"
MEDIA="/mnt/data/sur/users/mmontante/01_data/media/LBmed.csv"

mkdir -p "$WORKDIR/logs"
cd "$WORKDIR"

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
