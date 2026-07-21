process COMBO_RUN {
    tag "$combo_nombre"

    publishDir "${params.outbase}/tamanho_${combo.size()}", mode: 'copy'

    cpus 1

    input:
    val combo

    output:
    path "${combo.join('_')}"

    script:
    combo_nombre = combo.join('_')
    strains_args = combo.join(' ')
    """
    eval "\$(mamba shell hook --shell bash)"
    mamba activate python3
    module load COMETS

    python3 ${params.comets_script} \\
      --gem_path ${params.gem_path} \\
      --strains ${strains_args} \\
      --cycles ${params.cycles} \\
      --media ${params.media} \\
      --media_dil ${params.media_dil} \\
      --media_vol ${params.media_vol} \\
      --outdir ${combo_nombre}
    """
}

workflow PROCESO_COMBOS {
    take:
    combos_ch

    main:
    COMBO_RUN(combos_ch)
}
