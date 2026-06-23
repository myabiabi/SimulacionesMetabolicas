from cobra.io import read_sbml_model

model = read_sbml_model(
    "/home/abigaylmontantearenas/Documents/proyecto_tesis/gemsembler_output_ecoli/assembly.xml"
)

solution = model.optimize()

print("Status:", solution.status)
print("Biomasa:", solution.objective_value)

print("Reacciones:", len(model.reactions))
print("Metabolitos:", len(model.metabolites))
print("Genes:", len(model.genes))

print(model.objective)