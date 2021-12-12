from itertools import zip_longest
import numpy as np
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
#import plot_hgdp

parser = argparse.ArgumentParser(description="subplots")

parser.add_argument('files', type=str, help='csv files with coordinates', nargs='+')
args = parser.parse_args()

n=len(args.files)

sns.set_theme(
    context = 'paper',
    font_scale = 3
)

def factors(n):
    out = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            out.append([i, n//i])
    return out

def get_grid(n):
    facs = factors(n)
    diff = list(map(lambda L: abs(L[0] - L[1]), facs))
    min_ind = np.argmin(diff)
    min_grid = facs[min_ind]
    
    if diff[min_ind] > 5:
        return get_grid(n+1)
    
    return min_grid

x, y = get_grid(n)
fig, axes = plt.subplots(x, y, figsize = (10*y, 10*x))
plt.tight_layout()

pops = pd.read_csv("/l/proj/kuin0009/genomic_data/hgdp/pops.csv")["pop_group"]

for file, ax in zip_longest(args.files, axes.ravel(), fillvalue='0'):
    if file == '0':
        continue
    path = Path(file)
    name = path.parts[-1].partition("_")[0]
    reduced = pd.read_csv(file)
    run = path.parts[-2][3:]

    plt.sca(ax)

    coord1, coord2 = reduced.iloc[:, :2].values.T
    xlab, ylab = reduced.keys()[:2]

    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.title(name)

    hue_order = ['Africa', 'Middle_Est', 'Central_South_Asia', 'Est_Asia', 'Oceania', 'Europe', 'America']

    sns.scatterplot(x=coord1, y=coord2, hue=pops, hue_order=hue_order, s=100, legend=False)

    """
    box = ax.get_position()

    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    """
plt.savefig("test.pdf", tight_layout=True)
plt.show()

