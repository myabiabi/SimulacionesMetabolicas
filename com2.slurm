#!/bin/bash
#SBATCH --job-name=com2
#SBATCH --output=%x.log
#SBATCH --error=%x.error
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


python /mnt/data/sur/users/mmontante/SimulacionesMetabolicas/sim_syncom_comets.py 
    --gem_path ./02_resultados/rz/models/finalmodels_cv 
    --strains bacillus agrobacterium pseudomonas mycobacterium arthrobacter 
    --cycles 150000 
    --outdir ./02_resultados/rz/310726simulaciones/com2


echo "[INFO] Python script finished at $(date)"

echo "========================================="
echo "Pipeline done at: $(date)"
echo "========================================="
