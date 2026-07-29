process FILL {
    tag "$draft_rds.simpleName"
    publishDir "${params.fill_outdir}", mode: 'copy'
    errorStrategy 'ignore'
    cpus 4
    memory '16 GB'
    time '24h'

    input:
    tuple path(draft_rds), path(rxn_weights), path(rxn_genes)

    output:
    path "*-fill.RDS"

    script:
    """
    eval "\$(conda shell.bash hook)"
    conda activate gapseq

    gapseq fill -m ${draft_rds} -n ${params.fill_media} -c ${rxn_weights} -g ${rxn_genes}
    """
}

workflow PROCESO_FILL {
    take:
    drafts_ch
    main:
    FILL(drafts_ch)
}
