import os
from gemsembler import GatheredModels, get_model_of_interest
from functions import filtrar_bacterias

DATA_DIR = "/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/2408_gemsembler_4c"
OUTPUT_DIR_BASE = "/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/2408_gemsembler_4c_output"


def procesar_bacteria(bacteria, output_dir_base=OUTPUT_DIR_BASE):
    id_bacteria = bacteria["id_bacteria"]
    output_dir = os.path.join(output_dir_base, id_bacteria)
    os.makedirs(output_dir, exist_ok=True)

    gathered = GatheredModels()
    for modelo in bacteria["modelos"]:
        gathered.add_model(**modelo)
    gathered.run()

    supermodel = gathered.assemble_supermodel(
        output_dir,
        path_final_genome_nt=bacteria["genoma_nt"]
        #path_final_genome_aa=bacteria["genoma_aa"],
    )
    #assembly model = reaccion al menos en 1 modelo"
    get_model_of_interest(supermodel, "core1", os.path.join(output_dir, f"na_{id_bacteria}_core1.xml"))
    supermodel.at_least_in(2)
    get_model_of_interest(supermodel, "core2", os.path.join(output_dir, f"na_{id_bacteria}_core2.xml"))
    supermodel.at_least_in(3)
    get_model_of_interest(supermodel, "core3", os.path.join(output_dir, f"na_{id_bacteria}_core3.xml"))

    print(f"{id_bacteria} completada.")


if __name__ == "__main__":
    for b in filtrar_bacterias(DATA_DIR):
        procesar_bacteria(b)