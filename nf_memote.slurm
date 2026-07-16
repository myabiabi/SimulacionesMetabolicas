#!/bin/bash
#SBATCH --job-name=nf_memote
#SBATCH --output=%x.log
#SBATCH --error=%x.error
#SBATCH --time=240:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G

echo "========================================="
echo "Job started on: $(date)"
echo "Running on host: $(hostname)"
echo "Working directory: $(pwd)"
echo "========================================="

module load nextflow/24.04.1
export JAVA_HOME=/opt/apps/oracle-java/20.0.1
eval "$(mamba shell hook --shell bash)"

cd /mnt/data/sur/users/mmontante/SimulacionesMetabolicas

nextflow run main_final.nf \
    -entry memote \
    -c nextflow_final.config \
    -resume
