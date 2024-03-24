from Bio import Phylo
import subprocess
import os
import shutil
import matplotlib.pyplot as plt



# Get the current working directory
current_dir = os.getcwd()

# Specify the full paths to the input files
aligned_trimmed_file = os.path.join(current_dir, "aligned_trimmed.fasta")

# Run modeltest-ng
subprocess.run(["modeltest-ng", "-i", aligned_trimmed_file, "-d", "aa"])

# Run raxml-ng to generate the best tree
subprocess.run(["raxml-ng", "--msa", aligned_trimmed_file, "--model", "LG+G4", "--prefix", "T1", "--threads", "2"])

# Check if the output files were created successfully
best_tree_file = os.path.join(current_dir, "T1.raxml.bestTree")
if os.path.isfile(best_tree_file):
    # Draw the best tree with bootstrap values
    tree_best = Phylo.read(best_tree_file, "newick")
    Phylo.draw(tree_best)
else:
    print("Error: T1.raxml.bestTree not found. Check the raxml-ng command.")

# Specify the output directory for ancestral reconstruction
ancestral_output_dir = os.path.join(current_dir, "ASR")

# Create the ASR directory if it doesn't exist
if not os.path.exists(ancestral_output_dir):
    os.makedirs(ancestral_output_dir)

# Run raxml-ng for ancestral sequence reconstruction
subprocess.run(["raxml-ng", "--ancestral", "--msa", aligned_trimmed_file, "--tree", best_tree_file, "--model", "LG+G4", "--prefix", "ASR"])

# Move the output files to the ASR directory
for file_suffix in ["ancestralTree", "ancestralProbs", "ancestralStates", "log"]:
    source_file = f"{current_dir}/ASR.raxml.{file_suffix}"
    dest_file = f"{ancestral_output_dir}/ASR.raxml.{file_suffix}"
    shutil.move(source_file, dest_file)

# Check if the ancestral tree file was moved successfully
ancestral_tree_file = os.path.join(ancestral_output_dir, "ASR.raxml.ancestralTree")
if os.path.isfile(ancestral_tree_file):
    # Draw the ancestral tree
    tree_ancestral = Phylo.read(ancestral_tree_file, "newick")
    Phylo.draw(tree_ancestral)
else:
    print(f"Error: {ancestral_tree_file} not found. Check the raxml-ng command.")
    
    
# Draw the best tree with bootstrap values
tree_best = Phylo.read(best_tree_file, "newick")
# Save the best tree as a PNG image
Phylo.draw(tree_best, do_show=False)
plt.savefig(os.path.join(current_dir, "best_tree.png"))
plt.close()

# Draw the ancestral tree
tree_ancestral = Phylo.read(ancestral_tree_file, "newick")
# Save the ancestral tree as a PNG image
Phylo.draw(tree_ancestral, do_show=False)
plt.savefig(os.path.join(ancestral_output_dir, "ancestral_tree.png"))
plt.close()

