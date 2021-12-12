#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=2
#SBATCH --job-name=DiffMap
#SBATCH --time=24:00:00
#SBATCH --partition=prod
#SBATCH --account=kuin0009
#SBATCH --output=diffmap.%A_%a.out
#SBATCH --error=diffmap.%A_%a.err
#SBATCH --array=1-9
 
module purge
module load miniconda/3
t=$(head -n $SLURM_ARRAY_TASK_ID tvals | tail -n 1)
Rscript train.R $t
