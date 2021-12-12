#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --job-name=umap
#SBATCH --time=02:00:00
#SBATCH --partition=prod
#SBATCH --account=kuin0009
#SBATCH --output=umap.out
#SBATCH --error=umap.err

module purge

python train_umap.py
