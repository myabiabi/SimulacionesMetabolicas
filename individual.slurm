#!/bin/bash
#SBATCH --job-name=com_results
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

python /mnt/data/sur/users/mmontante/SimulacionesMetabolicas/sim_syncom_comets.py --gem_path ./02_data/rizo/carveme/prokka --strains ST00042 --cycles 40000 --outdir ./resultados4/com1

python /mnt/data/sur/users/mmontante/SimulacionesMetabolicas/sim_syncom_comets.py --gem_path ./02_data/rizo/carveme/prokka --strains ST00046 --cycles 40000 --outdir ./resultados4/com2

python /mnt/data/sur/users/mmontante/SimulacionesMetabolicas/sim_syncom_comets.py --gem_path ./02_data/rizo/carveme/prokka --strains ST0060 --cycles 40000 --outdir ./resultados4/com3

python /mnt/data/sur/users/mmontante/SimulacionesMetabolicas/sim_syncom_comets.py --gem_path ./02_data/rizo/carveme/prokka --strains ST00094 --cycles 40000 --outdir ./resultados4/com4

python /mnt/data/sur/users/mmontante/SimulacionesMetabolicas/sim_syncom_comets.py --gem_path ./02_data/rizo/carveme/prokka --strains ST00101 --cycles 40000 --outdir ./resultados4/com5

python /mnt/data/sur/users/mmontante/SimulacionesMetabolicas/sim_syncom_comets.py --gem_path ./02_data/rizo/carveme/prokka --strains ST00109 --cycles 40000 --outdir ./resultados4/com6

python /mnt/data/sur/users/mmontante/SimulacionesMetabolicas/sim_syncom_comets.py --gem_path ./02_data/rizo/carveme/prokka --strains ST00110 --cycles 40000 --outdir ./resultados4/com7

python /mnt/data/sur/users/mmontante/SimulacionesMetabolicas/sim_syncom_comets.py --gem_path ./02_data/rizo/carveme/prokka --strains ST00143 --cycles 40000 --outdir ./resultados4/com8

python /mnt/data/sur/users/mmontante/SimulacionesMetabolicas/sim_syncom_comets.py --gem_path ./02_data/rizo/carveme/prokka --strains ST00154 --cycles 40000 --outdir ./resultados4/com9

python /mnt/data/sur/users/mmontante/SimulacionesMetabolicas/sim_syncom_comets.py --gem_path ./02_data/rizo/carveme/prokka --strains ST00164 --cycles 40000 --outdir ./resultados4/com10


echo "[INFO] Python script finished at $(date)"

echo "========================================="
echo "Pipeline done at: $(date)"
echo "========================================="
