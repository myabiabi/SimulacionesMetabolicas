#!/bin/bash
#SBATCH --job-name=nf_comets
#SBATCH --output=/home/mmontante/logs/nf_comets_%j.out
#SBATCH --error=/home/mmontante/logs/nf_comets_%j.err
#SBATCH --time=13:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --partition=normal

# ==========================================================================
# run_nextflow.sbatch
#
# Este job NO corre las simulaciones directamente: lanza Nextflow, y es
# Nextflow quien somete (con sbatch, automaticamente) una tarea de SLURM
# por cada .xml, gracias a "executor = 'slurm'" en nextflow.config.
#
# Por eso este job "cabeza" pide pocos recursos (1 cpu, poca memoria):
# solo esta orquestando, no ejecutando COMETS el mismo.
#
# AJUSTA antes de correr:
#   - --output/--error (rutas absolutas; crea la carpeta antes con mkdir -p)
#   - --time (debe ser >= el tiempo total que tarden TODAS las tareas en
#     terminar, ya que este job se queda vivo esperando a que Nextflow
#     termine de someter y monitorear todas las tareas)
#   - la ruta donde estan main.nf y nextflow.config (WORKDIR abajo)
#
# Uso:
#   mkdir -p /home/mmontante/logs
#   sbatch run_nextflow.sbatch
# ==========================================================================

set -u

# ---- Activar ambiente mamba y cargar modulos necesarios --------------------
eval "$(mamba shell hook --shell bash)"
mamba activate python3
module load COMETS
module load nextflow          # quita esta linea si nextflow ya viene con tu env de mamba

# ---- Ir a la carpeta donde estan main.nf y nextflow.config -----------------
WORKDIR="/mnt/data/sur/users/mmontante/SimulacionesMetabolicas"   # <-- ajusta esta ruta
cd "$WORKDIR" || { echo "[ERROR] No existe $WORKDIR"; exit 1; }

echo "=== Lanzando pipeline Nextflow: $(date) ==="
echo "Job ID: $SLURM_JOB_ID"
echo "Nodo (cabeza): $(hostname)"

# -resume permite reanudar si el pipeline se cae a la mitad (no reprocesa
# los .xml que ya terminaron bien)
nextflow run main.nf \
    --gem_path /mnt/data/sur/users/mmontante/02_resultados/rz/gem \
    --outbase  /mnt/data/sur/users/mmontante/02_resultados/simulaciones \
    --media lb --cycles 5 --initial_mass 1e-4 \
    -profile slurm \
    -resume

status=$?
echo "=== Pipeline finalizado: $(date) (codigo $status) ==="
exit $status
