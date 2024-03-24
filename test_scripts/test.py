# docking_script.py

# Load dependencies
import sys
from biopandas.pdb import PandasPdb
import openmm as mm
from openmm import *
from openmm.app import *
from openmm.unit import *
import os
import urllib.request
import numpy as np
import pandas as pd
import subprocess

# Define the directory
pipeline_directory = "/home/farah/Pipeline/"

# Automatically detect receptor and ligand files
pdb_files = [f for f in os.listdir(pipeline_directory) if f.endswith(".pdb")]

# Filter files based on some criteria (you may need to adjust this based on your file naming conventions)
receptor_file = next((f for f in pdb_files if "oprD" in f), None)
ligand_file = next((f for f in pdb_files if "1" in f), None)

# Check if both receptor and ligand files are found
if receptor_file is None or ligand_file is None:
    print("Error: Could not find receptor or ligand files.")
    sys.exit(1)

# Full paths to receptor and ligand files
path_to_oprD_pdb = os.path.join(pipeline_directory, receptor_file)
path_to_1_pdb = os.path.join(pipeline_directory, ligand_file)

# LightDock setup
output_setup = subprocess.check_output("cd /home/farah/Pipeline/lightdock && chmod +x /home/farah/Pipeline/lightdock/setup.sh && /home/farah/Pipeline/lightdock/setup.sh", shell=True)

# Set LIGHTDOCK_HOME and PATH
os.environ["LIGHTDOCK_HOME"] = "/home/farah/Pipeline/lightdock"
os.environ["PATH"] = os.environ["PATH"] + ":" + os.environ["LIGHTDOCK_HOME"] + "/bin"
sys.path.append(os.environ["LIGHTDOCK_HOME"])

# LightDock long test setup
os.environ["LIGHTDOCK_LONG_TEST"] = "true"
output_long_test = subprocess.check_output(f"/home/farah/Pipeline/lightdock/bin/lgd_setup.py {path_to_oprD_pdb} {path_to_1_pdb} --noxt --noh --now -anm", shell=True)

# New command
output_run = subprocess.check_output(f"/home/farah/Pipeline/lightdock/bin/lgd_run.py /home/farah/Pipeline/setup.json 10 -c 1 -l 0", shell=True)

output_generate = subprocess.check_output(f"/home/farah/Pipeline/lightdock/bin/lgd_generate_conformations.py {path_to_oprD_pdb} {path_to_1_pdb} /home/farah/Pipeline/swarm_0/gso_10.out 200", shell=True)

# Additional command with output redirection
# Define the base directory
base_directory = "/home/farah/Pipeline/"

# Define the dynamically generated output directory
output_directory = os.path.join(base_directory, "output_directory")

# Ensure the output directory exists; if not, create it
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Additional command with output redirection to the dynamically generated output directory
output_cluster = subprocess.check_output(
    f"/home/farah/Pipeline/lightdock/bin/lgd_cluster_bsas.py /home/farah/Pipeline/swarm_0/gso_10.out > {os.path.join(output_directory, 'cluster_output.txt')}",
    shell=True
)

# Access standard output and standard error
output_cluster = result_cluster.stdout.decode("utf-8")
error_cluster = result_cluster.stderr.decode("utf-8")



