import shutil
import glob
import os

# Remove files matching the patterns
file_patterns = ['T1.*', '*.log', '*.ckp', '*.out', 'ASR.*', '*.tree', '*.fna', '*.fasta', '*.faa']

for pattern in file_patterns:
    files_to_remove = glob.glob(pattern)
    for file_to_remove in files_to_remove:
        try:
            if os.path.isfile(file_to_remove) or os.path.islink(file_to_remove):
                os.remove(file_to_remove)
            elif os.path.isdir(file_to_remove):
                shutil.rmtree(file_to_remove)
        except Exception as e:
            print(f"Error while deleting {file_to_remove}: {e}")

