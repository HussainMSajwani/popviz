import phate
from bed_reader import open_bed
import numpy as np
from pandas import DataFrame
import sys

seed = int(sys.argv[1])

hgdp = open_bed("/l/proj/kuin0009/genomic_data/hgdp/hgdp_QC_IMP.bed").read()

ph = phate.PHATE(n_components=4, n_jobs=4, random_state=seed)
embedding = ph.fit_transform(hgdp)

DataFrame(
{f"phate{i+1}": embedding[:, i] for i in range(4)}
).to_csv(f"PHATE_{seed}_out.csv", index=False)
