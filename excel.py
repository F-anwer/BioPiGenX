import os
import pandas as pd

# Define the base directory
base_directory = "/home/farah/Pipeline/"

# Define the dynamically generated output directory
output_directory = os.path.join(base_directory, "output_directory")

# Get a list of ligands from the ligand directory
ligand_directory = "/home/farah/Pipeline/lig"
all_files = os.listdir(ligand_directory)
ligands = [file for file in all_files if file.endswith(".pdb")]

# Initialize an empty list to store DataFrames
dfs = []

# Iterate over ligands
for ligand_file in ligands:
    # Define the path to the Excel file for the current ligand
    excel_file_path = os.path.join(output_directory, f'output_data_{ligand_file}.xlsx')

    # Read the Excel file into a DataFrame
    df = pd.read_excel(excel_file_path)

    # Append the DataFrame to the list
    dfs.append(df)

# Concatenate all DataFrames in the list
merged_df = pd.concat(dfs, ignore_index=True)

# Save the merged DataFrame to a single Excel file
merged_excel_path = os.path.join(output_directory, 'merged_output_data.xlsx')
merged_df.to_excel(merged_excel_path, index=False)

print(f"All Excel files merged and saved at: {merged_excel_path}")

