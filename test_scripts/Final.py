import os
import subprocess
import pandas as pd
import shutil

# Load dependencies
import sys
from biopandas.pdb import PandasPdb
import openmm as mm
from openmm import *
from openmm.app import *
from openmm.unit import *

# Define the base directory
base_directory = "/home/farah/Pipeline/"

# Define the dynamically generated output directory
output_directory = os.path.join(base_directory, "output_directory")

# Get a list of ligands from the ligand directory
ligand_directory = "/home/farah/Pipeline/lig"
all_files = os.listdir(ligand_directory)
ligands = [file for file in all_files if file.endswith(".pdb")]

# Iterate over ligands
for ligand_file in ligands:
    ligand_path = os.path.join(ligand_directory, ligand_file)
    
    # LightDock setup
    output_setup = subprocess.check_output(
        f"cd {os.path.join(base_directory, 'lightdock')} && "
        f"chmod +x {os.path.join(base_directory, 'lightdock', 'setup.sh')} && "
        f"{os.path.join(base_directory, 'lightdock', 'setup.sh')}",
        shell=True
    )

    # Set LIGHTDOCK_HOME and PATH
    os.environ["LIGHTDOCK_HOME"] = os.path.join(base_directory, "lightdock")
    os.environ["PATH"] = os.environ["PATH"] + ":" + os.environ["LIGHTDOCK_HOME"] + "/bin"
    sys.path.append(os.environ["LIGHTDOCK_HOME"])

    # LightDock long test setup
    os.environ["LIGHTDOCK_LONG_TEST"] = "true"
    output_long_test = subprocess.check_output(
        f"{os.path.join(base_directory, 'lightdock', 'bin', 'lgd_setup.py')} {os.path.join(base_directory, 'oprD.pdb')} {ligand_path} --noxt --noh --now -anm",
        shell=True
    )

    # New command
    output_run = subprocess.check_output(
        f"{os.path.join(base_directory, 'lightdock', 'bin', 'lgd_run.py')} {os.path.join(base_directory, 'setup.json')} 10 -c 1 -l 0",
        shell=True
    )

    output_generate = subprocess.check_output(
        f"{os.path.join(base_directory, 'lightdock', 'bin', 'lgd_generate_conformations.py')} {os.path.join(base_directory, 'oprD.pdb')} {ligand_path} {os.path.join(base_directory, 'swarm_0', 'gso_10.out')} 200",
        shell=True
    )

    # Additional command with output redirection to the dynamically generated output directory
    output_cluster = subprocess.check_output(
        f"{os.path.join(base_directory, 'lightdock', 'bin', 'lgd_cluster_bsas.py')} {os.path.join(base_directory, 'swarm_0', 'gso_10.out')} > {os.path.join(output_directory, 'cluster_output.txt')}",
        shell=True
    )

    # Define the path to cluster_output.txt
    cluster_output_file = os.path.join(output_directory, 'cluster_output.txt')

    # Read the first row from the cluster.repr file
    cluster_repr_file = "/home/farah/Pipeline/swarm_0/cluster.repr"
    with open(cluster_repr_file, 'r') as f:
        cluster_repr_content = f.readline().strip().split('\t')

    # Initialize an empty list to store glowworm pairs and RMSD values
    glowworm_pairs = []
    rmsd_values = []

    # Find the glowworm pairs and RMSD values in cluster_output.txt and add them to the lists
    with open(cluster_output_file, 'r') as f:
        for line in f:
            if "RMSD between" in line:
                values = line.split()
                glowworm1 = values[4]
                glowworm2 = values[6]
                rmsd = float(values[-1])
                glowworm_pairs.append((glowworm1, glowworm2))
                rmsd_values.append(rmsd)

    # Create a DataFrame with glowworm pairs and RMSD values
    df = pd.DataFrame({'Glowworm1': [pair[0] for pair in glowworm_pairs],
                       'Glowworm2': [pair[1] for pair in glowworm_pairs],
                       'RMSD': rmsd_values})

    # Find the minimum RMSD and update the 'Min_RMSD' column
    min_rmsd = df['RMSD'].min()
    df['Min_RMSD'] = min_rmsd

    # Create column names for additional_columns based on cluster.repr content
    additional_columns = pd.DataFrame([line.split('\t') for line in cluster_repr_content])

    # Check for duplicate column names and rename if necessary
    additional_columns.columns = additional_columns.columns.where(~additional_columns.columns.duplicated(), lambda x: x + '_duplicate')

    # Concatenate the DataFrames
    final_df = pd.concat([df, additional_columns], axis=1)

    # Select only the first row of the DataFrame
    first_row_df = final_df.head(1)

    # Save the first row to an Excel file
    excel_output_path = os.path.join(output_directory, f'output_data_{ligand_file}.xlsx')
    first_row_df.to_excel(excel_output_path, index=False)
    print(f"Excel file saved at: {excel_output_path}")

    # Check if there is any content in the cluster.repr file
    if cluster_repr_content:
        # Extract the last entry from the first row
        last_pdb_entry_full = cluster_repr_content[-1]

        # Extract the specific filename 'lightdock_28.pdb'
        last_pdb_entry_parts = last_pdb_entry_full.split(':')
        specific_filename = last_pdb_entry_parts[-1]

        # Search for the corresponding PDB file (specifically 'lightdock_28.pdb') in /home/farah/Pipeline/swarm_0 folder
        pdb_file_path = os.path.join("/home/farah/Pipeline/swarm_0", specific_filename)
        if os.path.exists(pdb_file_path):
            # Extract receptor and ligand names from the original paths
            receptor_name = os.path.splitext(os.path.basename("/home/farah/Pipeline/oprD.pdb"))[0]
            ligand_name = os.path.splitext(os.path.basename(ligand_path))[0]

            # Remove "_lightdock_*" from the specific filename
            new_specific_filename = '_'.join(specific_filename.split('_lightdock_')[:-1])

            # Construct the new PDB file name with receptor and ligand names and ".pdb" extension
            new_pdb_filename = f"{receptor_name}_AbAMP{ligand_name}{new_specific_filename}.pdb"

            # Move the PDB file to the output directory with the new name
            output_pdb_file_path = os.path.join(output_directory, new_pdb_filename)
            shutil.copy(pdb_file_path, output_pdb_file_path)
            print(f"PDB file '{new_pdb_filename}' copied to: {output_pdb_file_path}")
        else:
            print(f"Error: PDB file '{specific_filename}' not found in /home/farah/Pipeline/swarm_0")
    else:
        print("Error: No content found in cluster.repr file.")

    # Cleanup command
    cleanup_command = "rm -rf setup.json init/ swarm_* *.npy lightdock_* lightdock.info* /home/farah/Pipeline/lig/lightdock_*"
    subprocess.check_output(cleanup_command, shell=True)

