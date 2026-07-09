#!/usr/bin/env nextflow

/*
 * ==========================================================================
 * main.nf - Simulacion COMETS por cada modelo .xml
 *
 * Nextflow: por cada archivo .xml en --gem_path se lanza una tarea
 * independiente (en paralelo, segun los recursos del cluster).
 *
 * USO:
 *   nextflow run main.nf \
 *       --gem_path /workspace/gemsembler/mycobacterium \
 *       --outbase  ./gemsembler/mycobacterium \
 *       --media lb --cycles 10 --initial_mass 1e-4 \
 *       -profile slurm
 *
 * (el -profile slurm viene definido en nextflow.config)
 * ==========================================================================
 */

nextflow.enable.dsl=2

// ---- Parametros (puedes sobreescribirlos desde la linea de comandos) -----
params.gem_path      = "/mnt/data/sur/users/mmontante/02_resultados/rz/gem"
params.outbase       = "/mnt/data/sur/users/mmontante/02_resultados/simulaciones"
params.script        = "/mnt/data/sur/users/mmontante/SimulacionesMetabolicas/sim_syncom_comets.py"
params.media         = "lb"
params.cycles        = 5
params.initial_mass  = "1e-4"

// ---- Canal de entrada: uno por cada archivo .xml --------------------------
Channel
    .fromPath("${params.gem_path}/*.xml")
    .set { xml_ch }

process simular_comets {

    tag "${xml.baseName}"

    // Copia el resultado de cada tarea a su carpeta final dentro de outbase.
    // Nextflow SIEMPRE corre cada tarea en un directorio de trabajo nuevo,
    // asi que la restriccion de "el outdir no debe existir antes" se
    // cumple automaticamente (cada tarea tiene su propio outdir limpio).
    publishDir "${params.outbase}/${xml.baseName}", mode: 'copy', overwrite: false

    input:
        path xml

    output:
        path "resultado_${xml.baseName}"

    script:
    """
    eval "\$(mamba shell hook --shell bash)"
    mamba activate python3
    module load COMETS

    python3 ${params.script} \\
        --gem_path ${params.gem_path} \\
        --strains ${xml.baseName} \\
        --initial_mass ${params.initial_mass} \\
        --cycles ${params.cycles} \\
        --media ${params.media} \\
        --outdir resultado_${xml.baseName}
    """
}

workflow {
    simular_comets(xml_ch)
}
