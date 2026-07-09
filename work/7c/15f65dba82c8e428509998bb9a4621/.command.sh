#!/bin/bash -ue
eval "$(mamba shell hook --shell bash)"
mamba activate python3
module load COMETS

python3 /mnt/data/sur/users/mmontante/SimulacionesMetabolicas/sim_syncom_comets.py \
    --gem_path /mnt/data/sur/users/mmontante/02_resultados/rz/gem \
    --strains rz_pk_gp_lb_ST00143 \
    --initial_mass 1e-4 \
    --cycles 5 \
    --media lb \
    --outdir resultado_rz_pk_gp_lb_ST00143
