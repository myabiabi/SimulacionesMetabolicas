process FILL {
    tag "$draft_rds.simpleName"

    publishDir "${params.fill_outdir}", mode: 'copy'

    cpus 4
    memory '16 GB'
    time '24h'

    input:
    path draft_rds

    output:
    path "*-fill.RDS"

    script:
    """
    eval "\$(conda shell.bash hook)"
    conda activate gapseq

    gapseq fill -m ${draft_rds} -n ${params.fill_media}
    """
}

workflow PROCESO_FILL {
    take:
    drafts_ch

    main:
    FILL(drafts_ch)
}
