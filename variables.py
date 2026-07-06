# from functions import variables_totales

# path_rz = "/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/models/rz"
# output_dir = "/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/evaluacion/rz"

# # Ahora sí la ejecutará con los 3 argumentos correctamente
# variables_totales(path_rz, output_dir, "variables_totales_rz.csv")

# import cobra 

# # Load the XML/SBML model
import cobra


model = cobra.io.read_sbml_model("/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/models/rz/rz_na_cv_lb_paenibacillus.xml")

# # Print the total number of reactions
# print(f"Total reactions: {len(model.reactions)}")

# # Print a formatted list of all reactions with their IDs and stoichiometry
# for reaction in model.reactions:
#     print(f"{reaction.id}: {reaction.reaction}")


# # Load the model from your xml/sbml file

# # Print the total number of genes
# print(f"Total Genes: {len(model.genes)}")

# # Iterate through and print the ID and Name of each gene
# for gene in model.genes:
#     print(f"Gene ID: {gene.id} | Name: {gene.name}")

# Print the total number of metabolites
print(f"Total metabolites: {len(model.metabolites)}")
print(f"Groups: {len(model.groups)}")
print(f"Variables: {len(model.variables)}")
print(f"Medium: {model.medium}")

print(f"Tolerance: {model._tolerance}")

# Print all metabolite IDs and their names
# for metabolite in model.metabolites:
   # print(f"ID: {metabolite.id} | Name: {metabolite.name}")