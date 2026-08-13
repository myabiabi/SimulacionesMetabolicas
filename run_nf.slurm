#!/bin/bash
#SBATCH --job-name=29726com
#SBATCH --output=/mnt/data/sur/users/mmontante/02_resultados/nf_work/%x.log
#SBATCH --error=/mnt/data/sur/users/mmontante/02_resultados/nf_work/%x.error
#SBATCH --time=240:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=2G

cd /mnt/data/sur/users/mmontante/SimulacionesMetabolicas


echo "========================================="
echo "Job started on: $(date)"
echo "Running on host: $(hostname)"
echo "Working directory: $(pwd)"
echo "========================================="

#module load nextflow/24.04.1
#export JAVA_HOME=/opt/apps/oracle-java/20.0.1
module load nextflow/25.10.4
#export JAVA_HOME=/opt/apps/oracle-java/20.0.1
module load oracle-java/20.0.1
export JAVA_HOME=/opt/apps/oracle-java/20.0.1
export NXF_JVM_ARGS="-XX:TieredStopAtLevel=1 -Xmx1g"

#nextflow run main.nf -entry MEMOTE -profile memote
nextflow run main.nf -entry COMETS -profile comets -resume
#nextflow run main.nf -entry COMBOS -profile combos -resume
#nextflow run main.nf -entry FILL -profile gapseq -resume
#nextflow run main.nf -entry DOALL -profile doall -resume
