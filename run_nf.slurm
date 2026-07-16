#!/bin/bash
#SBATCH --job-name=comets
#SBATCH --output=/mnt/data/sur/users/mmontante/02_resultados/nf_work/nf_logs/logs/%x.log
#SBATCH --error=/mnt/data/sur/users/mmontante/02_resultados/nf_work/nf_logs/logs/%x.error
#SBATCH --time=240:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=2G

cd /mnt/data/sur/users/mmontante/SimulacionesMetabolicas


echo "========================================="
echo "Job started on: $(date)"
echo "Running on host: $(hostname)"
echo "Working directory: $(pwd)"
echo "========================================="

module load nextflow/24.04.1
export JAVA_HOME=/opt/apps/oracle-java/20.0.1

#nextflow run main.nf -entry MEMOTE -profile memote
nextflow run main.nf -entry COMETS -profile comets -resume
