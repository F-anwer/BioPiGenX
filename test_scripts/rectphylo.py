import random
from ete3 import Tree, TreeStyle, NodeStyle, faces, AttrFace, CircleFace
from Bio import Phylo
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

def get_node_color(node):
    # Define a function to assign colors based on node types (leaf or internal)
    if node.is_leaf():
        leaf_name = node.name
        # Generate a truly random color for leaf names
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))
    else:
        # Generate a random color for branch nodes based on a different criterion
        # You can modify this logic based on your requirements
        if len(node.children) > 0:
            child_colors = [get_node_color(child) for child in node.children]
            # Assign the branch color based on some property of child colors
            branch_color = "#00FF00"  # Example: green color for branches
            return branch_color
        else:
            return "#666666"  # Color for internal nodes (branches)

def get_leaf_name_color(node):
    # Generate a truly random color for leaf names
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def layout(node):
    if node.is_leaf():
        N = AttrFace("name", fsize=14)
        faces.add_face_to_node(N, node, 0, position="branch-right")
    if "weight" in node.features:
        # Creates a sphere face whose size is proportional to node's
        # feature "weight"
        C = CircleFace(radius=node.weight, color="RoyalBlue", style="sphere")
        # Let's make the sphere transparent
        C.opacity = 0.3
        # And place as a float face over the tree
        faces.add_face_to_node(C, node, 0, position="float")

if __name__ == "__main__":
    # Specify your input tree file name
    input_tree_file = os.path.join("ASR", "ASR.raxml.ancestralTree")

    # Specify the format of the input tree file (e.g., 'newick')
    input_tree_format = 'newick'

    # Build the tree from the input file
    tree = build_tree(input_tree_file, format=input_tree_format)

    # Convert the tree to an ete3 tree
    built_tree = build_tree_for_ete3(tree.root)

    # Create an empty TreeStyle
    ts = TreeStyle()

    # Set our custom layout function
    ts.layout_fn = layout

    # Assign colors to nodes based on types (leaf or internal)
    for node in built_tree.traverse():
        node.add_feature("color", get_node_color(node))

        # Customize node style
        nstyle = NodeStyle()
        nstyle["fgcolor"] = get_node_color(node)
        node.set_style(nstyle)

    # Add additional styles as needed
    style = NodeStyle()
    style["fgcolor"] = "#0f0f0f"
    style["size"] = 0
    style["vt_line_color"] = "#ff0000"
    style["hz_line_color"] = "#ff0000"
    style["vt_line_width"] = 8
    style["hz_line_width"] = 8
    style["vt_line_type"] = 0  # 0 solid, 1 dashed, 2 dotted
    style["hz_line_type"] = 0
    built_tree.set_style(style)

    # Save the final tree image
    built_tree.render("tree_colored_final.png", dpi=300, tree_style=ts)

