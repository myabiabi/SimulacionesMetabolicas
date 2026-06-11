from cobra.io import read_sbml_model

# Cargar el modelo desde el XML
model = read_sbml_model("./gemsembler_output/assembly.xml")

print(f"Reacciones: {len(model.reactions)}")
print(f"Metabolitos: {len(model.metabolites)}")
print(f"Genes: {len(model.genes)}")
print(f"Objetivo: {model.objective}")

# Probar biomasa
solution = model.optimize()
print(f"\nStatus: {solution.status}")
print(f"Biomass flux: {solution.objective_value}")