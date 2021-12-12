from pandas_plink import read_plink
import numpy as np
import sys
from tqdm import tqdm

S = int(sys.argv[1]) - 1

bim, fam, bed = read_plink("/home/shussain/popviz/genomic_data/hgdp_QC_IMP")
bed = bed.astype(np.int8).T

n = bed.shape[0]

def get_pos(k):
    if k==1:
        return 0, 0
    
    T = lambda n: n*(n+1)/2
    n = np.ceil(-0.5+0.5*np.sqrt(1+8*k))
    
    return int(n-1), int(k-T(n-1)-1)

K = np.array_split(np.arange(n**2), 1000)[S]

with open(f"{S+1}.txt", 'w') as w:
    pass

for k in tqdm(K, desc=f"{S}"):
    ind1, ind2 = get_pos(k+1)

    id1 = bed[ind1, :]
    id2 = bed[ind2, :]
    
    with open(f"{S+1}.txt", 'a') as w:
        w.writelines(f"{ind1+1},{ind2+1},{np.linalg.norm(id1 - id2).compute()}\n")
    
    