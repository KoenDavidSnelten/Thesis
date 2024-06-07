#!/bin/bash
#SBATCH --job-name=sentiment
#SBATCH --time=02:00:00
#SBATCH --partition=regular
#SBATCH --mem=4gb
#SBATCH --array=0-100
 
module purge
module load Python/3.9.6-GCCcore-11.2.0
 
source $HOME/venvs/Scriptie_env/bin/activate
 
python3 --version
which python3

python3 sentiment_analysis.py ${SLURM_ARRAY_TASK_ID}
 
deactivate