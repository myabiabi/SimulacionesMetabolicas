process MEMOTE_REPORT {
    tag "$model.simpleName"
    publishDir "${params.output_dir}", mode: 'copy'
    cpus 8
    memory '8 GB'
    time '240h'

    input:
    path model

    output:
    path "${model.simpleName}.html", emit: html
    path "${model.simpleName}.json", emit: json

    script:
    """
    eval "\$(mamba shell hook --shell bash)"
    mamba activate memote-env

    memote run ${model} --filename ${model.simpleName}.json --skip-unchanged=false
    memote report snapshot ${model} --filename ${model.simpleName}.html
    """
}

process COMPARE_MEMOTE {
    publishDir "${params.output_dir}", mode: 'copy'
    cpus 2
    memory '4 GB'
    time '1h'

    input:
    path jsons

    output:
    path "comparacion_memote.csv"

    script:
    """
    eval "\$(mamba shell hook --shell bash)"
    mamba activate memote-env

    python3 compare_memote.py --jsons ${jsons} --output comparacion_memote.csv
    """
}

workflow PROCESO_MEMOTE {
    take:
    models_ch

    main:
    MEMOTE_REPORT(models_ch)
    COMPARE_MEMOTE(MEMOTE_REPORT.out.json.collect())

    emit:
    html = MEMOTE_REPORT.out.html
    json = MEMOTE_REPORT.out.json
    comparison = COMPARE_MEMOTE.out
}
