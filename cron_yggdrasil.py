#!/usr/bin/env python3
# This script starts the Yggdrasil workflow
# it has three main functions:
# 1. It checks if there are new files in the upload folder
# 2. As nextflow is crap at dealing with symlinks, 
# it sets up the output structure and symlinks the raw data there
# 3. It starts the nextflow workflow

import os
from pathlib import Path
import multiprocessing as mp
import subprocess
import shlex

def get_project_ids(path):
    # the project id is found in ./ctg.config
    # it is a comma separated list
    conf = path / 'ctg.config'
    with open(conf, 'r') as f:
        for line in f:
            if line.lstrip().startswith('params.projectids'):
                return line.split('=')[1].strip().split(',')

def setup_output_structure(output_root, path, project_ids):
    # we need to set up the output structure
    # this is done by creating a folder for each project id
    # and symlinking the raw data there
    # the output structure is:
    # /projects/fs1/Test_Jobs/<project_id>/<results>
    out_paths = []
    raw_data_paths = []
    for project_id in project_ids:
        output_path = output_root / project_id
        output_path.mkdir(parents=True, exist_ok=True)
        out_paths.append(output_path)
        # symlink the raw data directory
        raw_data = output_path / path.stem
        raw_data.symlink_to(path)
        raw_data_paths.append(raw_data)
        
    return out_paths, raw_data_paths

def start_yggdrasil(out_path, raw_data_symlink):
    # placeholder command
    cmd = shlex('nextflow run /projects/fs1/nas-sync/yggdrasil.nf' 
    '-c /projects/fs1/nas-sync/yggdrasil.config -profile slurm' 
    f'--projectid {out_path.name} --raw_data {raw_data_symlink}')
    subprocess.run(cmd, shell=True)
    


if __name__ == '__main__':
    # for the sake of multiprocessing
    upload_dir = Path('/projects/fs1/nas-sync/upload')
    output_root = Path('/projects/fs1/Test_Jobs')

    #set script umask to 0002
    os.umask(0o0002)

    # check if there are new files in the upload folder
    # we know that sync is done when ctg.sync.done is present
    # when processing is started we add cron.yggdrasil.start
    ready_for_processing = []
    for p in upload_dir.glob('*/ctg.sync.done'):
        if not (p.parent / 'yggdrasil.cron.start').exists():
            ready_for_processing.append(p.parent)
    