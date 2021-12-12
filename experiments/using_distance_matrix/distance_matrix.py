import numpy as np
from bed_reader import open_bed
from sklearn.metrics.pairwise import pairwise_distances
from tqdm.auto import tqdm
from sklearn.metrics import euclidean_distances

bed_1g = open_bed("hgdp_QC_IMP.bed")

def pairwise_euc(X):
    chunks=np.array_split(np.arange(X.shape[1]), 30)
    dists=[]
    for chunk_index in tqdm(chunks):
        chunk = X.read(index=np.s_[:, chunk_index])
        dists.append(euclidean_distances(chunk, squared=True))
    return np.sqrt(sum(dists))
    
d_matrix = pairwise_euc(bed_1g)
np.savetxt('distance_matrix', d_matrix)
