import os
import sys

# agregar ruta
sys.path.append('/home/abigaylmontantearenas/Documents/proyecto_tesis/04_scr/PhyloMint')

from lib import BuildGraphNetX, CalculateIndexes

input_dir = '/media/abigaylmontantearenas/KINGSTON/septiembre/bacterias/cc/gems/final_models'
output_path = '/media/abigaylmontantearenas/KINGSTON/septiembre/bacterias/cc/gems/phylomint'

maxcc = 5

# obtener archivos xml
files = [f for f in os.listdir(input_dir) if f.endswith('.xml')]

# # guardar datos
ConfidenceDic = {}
nonSeedSetDic = {}

# calcular seed sets
for f in files:
    path = os.path.join(input_dir, f)
    name = f.replace('.xml', '')

    print(f'Procesando: {name}')
    DG = BuildGraphNetX.buildDG(path)
    conf, seed, nonseed = BuildGraphNetX.getSeedSet(DG, maxComponentSize=maxcc)

    ConfidenceDic[name] = conf
    nonSeedSetDic[name] = nonseed

# calcular índices
with open(output_path, 'w') as out:
    out.write('A\tB\tCompetition\tComplementarity\n')

    for A in files:
        for B in files:
            A_name = A.replace('.xml', '')
            B_name = B.replace('.xml', '')

            comp = CalculateIndexes.MetabolicCompetitionIdx(
                ConfidenceDic[A_name], ConfidenceDic[B_name]
            )

            coop = CalculateIndexes.MetabolicCooperationIdx(
                ConfidenceDic[A_name],
                ConfidenceDic[B_name],
                nonSeedSetDic[B_name]
            )

            out.write(f'{A_name}\t{B_name}\t{comp}\t{coop}\n')

#import os
#from lib import BuildGraphNetX

#sbml_path = '/home/abigaylmontantearenas/Documents/proyecto_tesis/02_data/rizo/carveme/prokka/ST00042_prokka_carveme_lb.xml'

# construir grafo
#DG = BuildGraphNetX.buildDG(sbml_path)

# obtener seed set
#seed_set = BuildGraphNetX.getSeedSet(DG, maxComponentSize=5)

#print("Seed set:", seed_set)
#print("Tamaño:", len(seed_set))

