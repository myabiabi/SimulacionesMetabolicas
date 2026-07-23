nextflow.enable.dsl=2

include { PROCESO_MEMOTE } from './memote.nf'
include { PROCESO_COMETS } from './comets.nf'
include { PROCESO_COMBOS } from './combos.nf'
include { PROCESO_DOALL } from './gap_doall.nf'
include { PROCESO_FILL } from './gap_fill.nf'

def combinationsOf(list, k) {
    def lst = list as ArrayList
    if (k == 0) return [[]]
    if (lst.size() < k) return []
    def result = []
    for (int i = 0; i <= lst.size() - k; i++) {
        def head = lst[i]
        def rest = (i + 1 < lst.size()) ? lst[(i + 1)..-1] : []
        combinationsOf(rest, k - 1).each { combo ->
            result << ([head] + combo)
        }
    }
    return result
}



workflow MEMOTE {
    models_ch = Channel.fromPath(params.memote_input)
    PROCESO_MEMOTE(models_ch)
}

workflow COMETS {
    strains_ch = Channel.fromPath("${params.gem_path}/*.xml")
                    .map { it.baseName }

    PROCESO_COMETS(strains_ch)
}


workflow COMBOS {
    cepas_ch = Channel.fromPath("${params.gem_path}/*.xml")
                    .map { it.baseName }
                    .collect()

    combos_ch = cepas_ch.flatMap { cepas ->
        def cepasList = cepas as ArrayList
        (2..4).collectMany { tam -> combinationsOf(cepasList, tam) }
    }

    PROCESO_COMBOS(combos_ch)
}

workflow DOALL {
    genomes_ch = Channel.fromPath("${params.genomes}")
    PROCESO_DOALL(genomes_ch)
}

workflow FILL {
    drafts_ch = Channel.fromPath("${params.fill_indir}/*-draft.RDS")
    PROCESO_FILL(drafts_ch)
}
