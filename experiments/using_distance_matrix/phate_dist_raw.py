from phate import PHATE
from sklearn.metrics import euclidean_distances
import numpy as np
from tqdm.auto import tqdm
from sklearn.datasets import make_blobs

X = make_blobs(5000, 1000, centers=5)

def pairwise_euc(X):
    chunks=np.array_split(np.arange(X.shape[1]), 30)
    dists=[]
    for chunk_index in tqdm(chunks):
        chunk = X[:, chunk_index]
        dists.append(euclidean_distances(chunk, squared=True))
    return np.sqrt(sum(dists))

mine = pairwise_euc(X[0])
model = PHATE(knn_dist='precomputed')
X_ph = model.fit_transform(mine)