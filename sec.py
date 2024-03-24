import os
import subprocess
from tqdm import tqdm

# Path to the s4pred directory where you cloned the GitHub repository
s4pred_directory = 's4pred'

# Directory containing input FASTA files
input_directory = 'faa_files'  # Assuming .faa files are stored in this directory

# Directory to save individual output files
output_directory = 'secondary_structure'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# List all files in the input directory with the .faa extension
input_files = [f for f in os.listdir(input_directory) if f.endswith('.faa')]

# Initialize tqdm progress bar
pbar = tqdm(input_files, desc='Progress', unit='file')

for input_file in pbar:
    input_path = os.path.join(input_directory, input_file)
    output_file = os.path.splitext(input_file)[0] + '_output.ss2'
    output_path = os.path.join(output_directory, output_file)

    # Run the s4pred script and save the output in the output directory
    s4pred_command = f'python {os.path.join(s4pred_directory, "run_model.py")} {input_path} > {output_path}'
    subprocess.call(s4pred_command, shell=True)

    pbar.set_postfix({'output_file': output_file})

