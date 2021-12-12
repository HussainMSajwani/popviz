from phate import PHATE
from scipy.sparse.linalg import eigsh
import numpy as np

class ModifiedPHATE(PHATE):

    def __init__(self, n_components=2, knn=5, decay=2, n_landmark=2000, t=1, gamma=1, n_pca=None, mds_solver="sgd", knn_dist="euclidean", knn_max=None, mds_dist="euclidean", mds="metric", n_jobs=1, random_state=None, verbose=1, potential_method=None, alpha_decay=None, njobs=None, **kwargs):

        super().__init__(n_components=n_components, knn=knn, decay=decay, n_landmark=n_landmark, t=t, gamma=gamma, n_pca=n_pca, mds_solver=mds_solver, knn_dist=knn_dist, knn_max=knn_max, mds_dist=mds_dist, mds=mds, n_jobs=n_jobs, random_state=random_state, verbose=verbose, njobs=njobs, **kwargs)

    def fit(self, X):
        super().fit(X)
        self.symmetric_diff_op = self.graph.diff_aff if isinstance(self.graph.diff_aff, np.ndarray) else self.graph.diff_aff.toarray()
        return self

    def _transform(self, X=None, t_max=100, plot_optimal_t=False, ax=None):
        return super().transform(X=X, t_max=t_max, plot_optimal_t=plot_optimal_t, ax=ax)

    def transform(self, X=None, t_max=100, plot_optimal_t=False, ax=None):
        self._transform(X=X, t_max=t_max, plot_optimal_t=plot_optimal_t, ax=ax)

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


