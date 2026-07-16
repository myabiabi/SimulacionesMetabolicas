#!/bin/bash
#SBATCH --job-name=com_results
#SBATCH --output=/mnt/data/users/mmontante/02_resultados/logs/%x.log
#SBATCH --error=/mnt/data/users/mmontante/02_resultados/logs/%x.error
#SBATCH --time=1000:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G

echo "========================================="
echo "Job started on: $(date)"
echo "Running on host: $(hostname)"
echo "Working directory: $(pwd)"
echo "========================================="

eval "$(mamba shell hook --shell bash)"
mamba activate python3
module load COMETS

echo "[INFO] Starting Python script at $(date)"

python /mnt/data/sur/users/mmontante/comunidades.py


echo "[INFO] Python script finished at $(date)"

echo "========================================="
echo "Pipeline done at: $(date)"
echo "========================================="

