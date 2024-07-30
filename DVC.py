import os
import pandas as pd
import numpy as np
from dvc.repo import Repo
import git
import sys

def ensure_git_repo():
    if not os.path.exists('.git'):
        print("Initializing Git repository...")
        git.Repo.init(os.getcwd())
    else:
        print("Git repository already initialized.")

def init_dvc():
    if not os.path.exists('.dvc'):
        print("Initializing DVC...")
        Repo.init()
        git_repo = git.Repo()
        git_repo.index.add(['.dvc'])
        git_repo.index.commit('Initialize DVC')
    else:
        print("DVC already initialized.")

def version_data(version, filename):
    print(f"Versioning data for version {version}...")
    
 
    data = pd.read_csv(filename)
    data['new_column'] = np.random.rand(len(data))
    data.to_csv(filename, index=False)
    
   
    dvc_repo = Repo()
    dvc_repo.add(filename)
    
   
    git_repo = git.Repo()
    git_repo.index.add([f'{filename}.dvc'])
    git_repo.index.commit(f'Update data to version {version}')
    
    print(f"Data versioned as version {version}")

def main():
    if len(sys.argv) > 1:
        dataset_file = sys.argv[1]
    else:
        dataset_file = input("Enter the name of your dataset file (e.g., customers.csv): ")
    
    if not os.path.exists(dataset_file):
        print(f"Error: {dataset_file} not found. Please ensure the dataset is in the current directory.")
        return

    ensure_git_repo()
    init_dvc()

    version_data(1, dataset_file)


    for i in range(2, 4):
        version_data(i, dataset_file)

    print("Data versioning complete!")

if __name__ == "__main__":
    main()