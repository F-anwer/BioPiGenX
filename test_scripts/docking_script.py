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

# LightDock setup
output_setup = subprocess.check_output("cd /home/farah/Pipeline/lightdock && chmod +x /home/farah/Pipeline/lightdock/setup.sh && /home/farah/Pipeline/lightdock/setup.sh", shell=True)

# Set LIGHTDOCK_HOME and PATH
os.environ["LIGHTDOCK_HOME"] = "/home/farah/Pipeline/lightdock"
os.environ["PATH"] = os.environ["PATH"] + ":" + os.environ["LIGHTDOCK_HOME"] + "/bin"
sys.path.append(os.environ["LIGHTDOCK_HOME"])

# LightDock long test setup
os.environ["LIGHTDOCK_LONG_TEST"] = "true"
output_long_test = subprocess.check_output(f"/home/farah/Pipeline/lightdock/bin/lgd_setup.py /home/farah/Pipeline/oprD.pdb /home/farah/Pipeline/1.pdb --noxt --noh --now -anm", shell=True)

# New command
output_run = subprocess.check_output("/home/farah/Pipeline/lightdock/bin/lgd_run.py /home/farah/Pipeline/setup.json 10 -c 1 -l 0", shell=True)

output_generate = subprocess.check_output("/home/farah/Pipeline/lightdock/bin/lgd_generate_conformations.py /home/farah/Pipeline/oprD.pdb /home/farah/Pipeline/1.pdb /home/farah/Pipeline/swarm_0/gso_10.out 200", shell=True)

