from Bio import AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
import os
from pycirclize import Circos
from pycirclize.utils import load_example_tree_file, ColorCycler
import numpy as np
np.random.seed(0)

def create_directory(directory):
    """Create a directory if it does not exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def build_phylogenetic_tree(input_file, output_directory):
    # Read the alignment from the input file
    alignment = AlignIO.read(input_file, "fasta")

    # Create a distance calculator and a tree constructor
    calculator = DistanceCalculator('identity')
    constructor = DistanceTreeConstructor(calculator, method='nj')

    # Calculate the distance matrix
    dm = calculator.get_distance(alignment)

    # Build the tree
    tree = constructor.build_tree(alignment)

    # Define the output file for the tree
    tree_output_file = os.path.join(output_directory, "phylogenetic_tree.nwk")

    # Save the tree to a Newick file
    Phylo.write(tree, tree_output_file, "newick")

    print(f"Phylogenetic tree saved to {tree_output_file}")

    # Visualization
    tree_file_path = tree_output_file
    circos, tv = Circos.initialize_from_tree(
        tree_file_path,
        start=-350,
        end=0,
        r_lim=(10, 80),
        leaf_label_size=5,
        leaf_label_rmargin=21,
        line_kws=dict(color="lightgrey", lw=1),
        ignore_branch_length=True,
    )

    # Set multi-colors for nodes
    ColorCycler.set_cmap("Set2")
    for node_label in tv.all_node_labels:
        tv.set_node_line_props(node_label, color=ColorCycler())

    # Plot heatmap
    sector = circos.sectors[0]
    heatmap_track = sector.add_track((80, 100))
    matrix_data = np.random.randint(0, 100, (5, tv.leaf_num))
    heatmap_track.heatmap(matrix_data, cmap="viridis")
    heatmap_track.yticks([0.5, 1.5, 2.5, 3.5, 4.5], list("EDCBA"), vmax=5, tick_length=0)

    # Add colorbar
    vmin2, vmax2 = -100, 100
    circos.colorbar(bounds=(0.68, 1.05, 0.3, 0.01), vmin=vmin2, vmax=vmax2, orientation="horizontal", cmap="viridis")

    # Save the figure as a PNG file within the output directory
    fig = circos.plotfig()
    output_plot_file = os.path.join(output_directory, "tree_plot.png")
    fig.savefig(output_plot_file, dpi=300, bbox_inches="tight")
    print(f"Tree plot saved to {output_plot_file}")

def main():
    input_file = os.path.join("multiple_sequence_alignment", "aligned_sequences.fasta")
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return

    output_directory = "phylogenetic_output"
    create_directory(output_directory)

    build_phylogenetic_tree(input_file, output_directory)

    print("Output files saved in the 'phylogenetic_output' directory.")
    print("Current working directory:", os.getcwd())

if __name__ == "__main__":
    main()

