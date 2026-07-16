process COMETS_RUN {
    tag "$strain"

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
      --media_dil ${params.media_dil} \\
      --media_vol ${params.media_vol} \\
      --outdir out_${strain}
    """
}

workflow PROCESO_COMETS {
    take:
    strains_ch

    main:
    COMETS_RUN(strains_ch)
}
