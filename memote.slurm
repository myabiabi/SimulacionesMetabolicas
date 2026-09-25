#!/bin/bash
#SBATCH --job-name=ccmemote
#SBATCH --output=/mnt/data/sur/users/mmontante/02_resultados/%x.log
#SBATCH --error=/mnt/data/sur/users/mmontante/02_resultados/%x.error
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

INPUT_DIR="/mnt/data/sur/users/mmontante/02_resultados/cc/models"
OUTPUT_DIR="/mnt/data/sur/users/mmontante/1809_resultados/cc/memote"

mkdir -p "$OUTPUT_DIR"

for model in "$INPUT_DIR"/*.xml; do
    # Extract the filename without the path
    filename=$(basename "$model")
    
    echo "Processing $filename..."
 
memote run "$model" --filename "$OUTPUT_DIR/${filename%.*}.json"
   
#memote report snapshot "$model" --filename "$OUTPUT_DIR/${filename%.*}.json"
#memote run --format json "$model" --filename "$OUTPUT_DIR/${filename%.*}.json"
done
