#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --job-name=PHATE
#SBATCH --time=03:00:00
#SBATCH --partition=prod
#SBATCH --account=kuin0009
#SBATCH --output=phate.out
#SBATCH --error=phate.err
#SBATCH --array=1-100

module purge
seed=$(head -n $SLURM_ARRAY_TASK_ID seeds | tail -n 1)
python train_phate.py $seed
