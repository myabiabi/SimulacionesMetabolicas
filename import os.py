import os
import csv
import cobra

def variables_totales(gem_path, output_dir):

    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "variables_totales.csv")

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Model_ID",
            "Total_Reactions",
            "Total_Metabolites",
            "Total_Genes"
        ])

        for file_name in os.listdir(gem_path):
            if not file_name.endswith(".xml"):
                continue

            model_id = file_name.replace(".xml", "")
            model_path = os.path.join(gem_path, file_name)

            try:
                model = cobra.io.read_sbml_model(model_path)

                R = len(model.reactions)
                M = len(model.metabolites)
                G = len(model.genes)

                writer.writerow([model_id, R, M, G])

                print(f"{model_id}: R={R} M={M} G={G}")

            except Exception as e:
                print(f"ERROR cargando {model_id}: {e}")

    print(f"CSV guardado en: {output_file}")
    

