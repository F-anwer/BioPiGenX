import os
import fnmatch
import shutil
import subprocess

# Set executable permission for the script
subprocess.run(["chmod", "+x", "annotate.sh"])

# Run the annotate.sh script
subprocess.run(["./annotate.sh"])

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

# Set the directory you want to start from
directory = 'annotation'

# Create a new folder to store .faa files
output_folder = 'faa_files'
os.makedirs(output_folder, exist_ok=True)

# Find all .faa files in the directory and its subdirectories
for file in find_files(directory, '*.faa'):
    # Create a new file name in the output folder
    new_file = os.path.join(output_folder, os.path.basename(file))

    # Copy the .faa file to the output folder
    shutil.copy(file, new_file)

print("All .faa files have been copied to the 'faa_files' folder.")

