process COMETS_RUN {
    tag "$strain"

    errorStrategy 'ignore'    // <-- ignora el modelo fallido y continúa
    
    publishDir "${params.outbase}/${strain}", mode: 'copy'

    cpus 1

    input:
    val strain

    output:
    path "out_${strain}"

    script:
    """
    eval "\$(mamba shell hook --shell bash)"
    mamba activate python3
    module load COMETS

    python ${params.comets_script} \\
      --gem_path ${params.gem_path} \\
      --strains ${strain} \\
      --media ${params.media} \\
      --cycles ${params.cycles} \\
      --outdir out_${strain}
    """
}

workflow PROCESO_COMETS {
    take:
    strains_ch

    main:
    COMETS_RUN(strains_ch)
}
