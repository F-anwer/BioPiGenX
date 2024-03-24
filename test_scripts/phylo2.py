from Bio import Phylo
from ete3 import Tree, TreeStyle, faces, AttrFace, CircleFace
import random
import os

def build_tree(fname: str, format='newick'):
    """ Build a tree from a file """
    tree = Phylo.read(fname, format)
    return tree

def build_tree_for_ete3(clade):
    # Convert a Biopython tree to an ete3 tree
    built_tree = Tree()
    for child in clade.clades:
        child_tree = build_tree_for_ete3(child)
        built_tree.add_child(child=child_tree, name=child.name, dist=child.branch_length)
    return built_tree

def get_leaf_name_color(node):
    # Generate a truly random color for leaf names
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def layout(node):
    if node.is_leaf():
        # Add node name to leaf nodes
        N = AttrFace("name", fsize=14, fgcolor="black")
        faces.add_face_to_node(N, node, 0)

    if "weight" in node.features:
        # Creates a sphere face whose size is proportional to node's
        # feature "weight"
        C = CircleFace(radius=node.weight, color="RoyalBlue", style="sphere")
        # Let's make the sphere transparent
        C.opacity = 0.3
        # And place as a float face over the tree
        faces.add_face_to_node(C, node, 0, position="float")

if __name__ == '__main__':
    # Specify your input tree file name
    input_tree_file = os.path.join("ASR", "ASR.raxml.ancestralTree")

    # Specify the format of the input tree file (e.g., 'newick')
    input_tree_format = 'newick'

    # Build the tree from the input file
    tree = build_tree(input_tree_file, format=input_tree_format)

    # Convert the tree to an ete3 tree
    built_tree = build_tree_for_ete3(tree.root)

    # Configure the tree style for circular display
    ts = TreeStyle()
    ts.mode = "c"
    ts.arc_start = -90  # 0 degrees = 3 o'clock
    ts.arc_span = 360
    ts.show_leaf_name = False

    # Apply the layout function to the tree
    ts.layout_fn = layout

    # Save the final tree image
    built_tree.render("tree_colored_final.png", tree_style=ts)

