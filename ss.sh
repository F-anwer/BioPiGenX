#!/bin/bash

# Add execute permissions to annotate.sh
chmod +x annotate.sh

# Run annotate.sh and then the Python script
./annotate.sh && python - <<END
import os
import fnmatch
import shutil

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

# Set the directory you want to start from
directory = 'annotation'

# Find all .faa files in the directory and its subdirectories
for file in find_files(directory, '*.faa'):
    # Create a new file name by combining the directory and the basename
    new_file = os.path.join(os.getcwd(), os.path.basename(file))

    # Copy the file to the current directory
    shutil.copy(file, new_file)
END

