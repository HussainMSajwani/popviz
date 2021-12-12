from sklearn.base import BaseEstimator
from sklearn.neighbors import kneighbors_graph
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize

import numpy as np
from scipy.sparse.linalg import eigsh

class DiffusionMaps(BaseEstimator):
    
    def __init__(
        self,
        n_components=2,
        knn=5,
        affinity="heat",
        epsilon=None,
        t=1,
        n_pca=None,
        metric="euclidean",
        density_normalize=False,
        random_state=None,
        n_jobs=1,
        verbose=True
    ):
        self.n_components = n_components
        self.knn = knn
        self.affinity = affinity
        self.epsilon = epsilon
        self.t = t
        self.n_pca = n_pca
        self.metric = metric
        self.density_normalize = density_normalize
        self.random_state=random_state
        self.verbose = verbose
        self.n_jobs = n_jobs

        self.kernel = None

    def _find_epsilon(self, D):
        p=0.01
        n = D.shape[1]
        k = np.ceil(p*n)
        k = int(k if k>2 else 2)  # use k of at least 2
        d_sort =  np.sort(D, axis=0)
        dist_knn = d_sort[k+1:] # find dists. to kth nearest neighbor
        epsilon = 2*np.percentile(dist_knn, 75)**2
        print(f"k, epsilon used:{k}, {epsilon}")
        return 10

    def fit(self, X):
        self.X = X
        #preliminary check
        if (self.knn is None) and (self.affinity == "knn"):
            raise Exception("must use knn parameter to set affinity = knn")
        #if distance matrix is provided, use it. Otherwise compute it either on the first n_pca PCs or on raw data.
        if self.metric == "precomputed":
            D = X
        elif not self.n_pca is None:
            PCs = PCA(n_components=self.n_pca, random_state=self.random_state).fit_transform()
            D = euclidean_distances(PCs)
        else:
            D = euclidean_distances(X)
        #figure out if to use fully connected graph or use knn graph
        if not self.knn is None:
            symmetrize_kernel = True
            #knn graph with heat kernel weights
            if self.affinity == "heat":
                mode = "distance"
            #knn graph with adjacency weights
            elif self.affinity == "knn":
                mode = "connectivity"
            else:
                raise NotImplementedError

            self._kernel = kneighbors_graph(
                X=D, 
                n_neighbors=self.knn, 
                metric=self.metric, 
                mode=mode
                ).toarray()
        else:
            symmetrize_kernel = False
            self._kernel = D

        if self.affinity == "heat":
            if self.epsilon is None:
                self.epsilon = self._find_epsilon(D)
            self.kernel = np.exp(-1 * np.power(self._kernel, 2)/self.epsilon)
        elif self.affinity == "knn":
            self.kernel = self._kernel
        else:
            raise NotImplementedError
        #symmetrize kernel if knn kernel was used
        if symmetrize_kernel:
            self.kernel = (self.kernel + self.kernel.T)/2

        self.degree = np.diag(np.sum(self.kernel, axis=0))
        degree_inv = np.diag(1 / np.sum(self.kernel, axis=0))
        #\alpha=1 normalization 
        if self.density_normalize:
            self.kernel = degree_inv @ self.kernel @ degree_inv

        self.P = self.kernel @ degree_inv
        self.symmetric_diff_op = np.sqrt(degree_inv) @ self.kernel @ np.sqrt(degree_inv) 

        return self

    def transform(self, X):
        if np.all(X != self.X):
            raise NotImplementedError("OOS extenstion not yet implemented")

        _eigenvalues, _eigenvectors = eigsh(np.linalg.matrix_power(self.symmetric_diff_op, self.t), k=self.n_components+1)
        #self.eigenvalues, self.eigenvectors = np.linalg.eig(self.symmetric_diff_op)
        _index = np.argsort(_eigenvalues)[::-1]
        self.eigenvalues = _eigenvalues[_index][1:]
        self.eigenvectors = _eigenvectors[:, _index][:, 1:]
        return self.eigenvectors

    def fit_transform(self, X):
        self.fit(X)
        embedding = self.transform(X)
        return embedding


        

