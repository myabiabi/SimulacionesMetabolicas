#!/bin/bash
#SBATCH --job-name=ecoli
#SBATCH --output=%x.log
#SBATCH --error=%x.error
#SBATCH --time=240:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=8G

echo "========================================="
echo "Job started on: $(date)"
echo "Running on host: $(hostname)"
echo "Working directory: $(pwd)"
echo "========================================="

eval "$(mamba shell hook --shell bash)"
mamba activate memote-env

INPUT_DIR="/mnt/data/sur/users/mmontante/02_resultados/rz/models/cv_final"
OUTPUT_DIR="/mnt/data/sur/users/mmontante"

mkdir -p "$OUTPUT_DIR"

for model in "$INPUT_DIR"/*.xml; do
    # Extract the filename without the path
    filename=$(basename "$model")
    
    echo "Processing $filename..."
    
memote report snapshot "$model" --filename "$OUTPUT_DIR/${filename%.*}.html"
done
