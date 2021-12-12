import umap
from bed_reader import open_bed
import numpy as np
from pandas import DataFrame

hgdp = open_bed("/l/proj/kuin0009/genomic_data/hgdp/hgdp_QC_IMP.bed").read()

um = umap.UMAP(n_components=4)
embedding = um.fit_transform(hgdp)

DataFrame(
{f"umap{i+1}": embedding[:, i] for i in range(4)}
).to_csv("UMAP_out.csv", index=False)