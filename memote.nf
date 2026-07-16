process MEMOTE_REPORT {
    tag "$model.simpleName"


    publishDir "${params.output_dir}", mode: 'copy'

    cpus 8
    memory '8 GB'
    time '240h'

    input:
    path model

    output:
    path "${model.simpleName}.html"

    script:
    """
    eval "\$(mamba shell hook --shell bash)"
    mamba activate memote-env
    memote report snapshot ${model} --filename ${model.simpleName}.html
    """
}

workflow PROCESO_MEMOTE {
    take:
    models_ch

    main:
    MEMOTE_REPORT(models_ch)
}
