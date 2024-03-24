import glob
import subprocess


# Get a list of ligand files
ligand_files = glob.glob("/home/farah/Pipeline/*_lig.pdb")

# Loop through ligand files and run the command
for ligand_file in ligand_files:
    output_generate = subprocess.check_output(f"/home/farah/Pipeline/lightdock/bin/lgd_generate_conformations.py /home/farah/Pipeline/*_rec.pdb {ligand_file} /home/farah/Pipeline/swarm_0/gso_10.out 200", shell=True)

