nextflow.enable.dsl=2

include { PROCESO_MEMOTE } from './memote.nf'
include { PROCESO_COMETS } from './comets.nf'

workflow MEMOTE {
    models_ch = Channel.fromPath(params.memote_input)
    PROCESO_MEMOTE(models_ch)
}

workflow COMETS {
    strains_ch = Channel.fromPath("${params.gem_path}/*.xml")
                    .map { it.baseName }

    PROCESO_COMETS(strains_ch)
}




// workflow por defecto (opcional), por si corres sin -entry
workflow {
    MEMOTE()
}
