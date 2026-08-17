process GAPSEQ_DOALL {
    tag "$genome.simpleName"

    publishDir "${params.outbase}", mode: 'copy'

    cpus 4
    memory '16 GB'
    time '24h'

    input:
    path genome

    output:
    path "${genome.simpleName}*"

    script:
    """
    eval "\$(conda shell.bash hook)"
    conda activate gapseq

    gapseq doall ${genome}
    """
}

workflow PROCESO_DOALL {
    take:
    genomes_ch

    main:
    GAPSEQ_DOALL(genomes_ch)
}
