import os
from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from pymsaviz import MsaViz

# Define the visualize_alignment_with_pyMSAviz function
def visualize_alignment_with_pyMSAviz(msa_file, output_path="plot.png"):
    """Visualize alignment with pyMSAviz and save it to a file."""
    mv = MsaViz(msa_file, start=40, end=500, wrap_length=60, show_consensus=True)
    mv.set_custom_color_scheme({"a": "red", "c": "skyblue", "t": "lime", "g": "orange"})
    mv.savefig(output_path)  # Save the plot to a file
    print("Alignment visualization saved to", output_path)


def calculate_identity(seq1, seq2):
    """Calculate sequence identity."""
    length = max(len(seq1), len(seq2))
    matches = sum(a == b for a, b in zip(seq1, seq2))
    return (matches / length) * 100


def group_sequences(alignment, identity_threshold=80):
    """Group sequences based on identity threshold."""
    groups = []
    for seq in alignment:
        assigned = False
        for group in groups:
            for existing_seq in group:
                identity = calculate_identity(seq.seq, existing_seq.seq)
                if identity >= identity_threshold:
                    group.append(seq)
                    assigned = True
                    break
            if assigned:
                break
        if not assigned:
            groups.append([seq])
    return groups


def write_groups(groups, output_prefix, output_folder):
    """Write each group to a separate file."""
    for i, group in enumerate(groups, 1):
        identity_values = [calculate_identity(seq.seq, group[0].seq) for seq in group]
        min_identity = min(identity_values)
        max_identity = max(identity_values)
        output_file = os.path.join(output_folder, f"{output_prefix}_identity_{min_identity}-{max_identity}.fasta")
        with open(output_file, "w") as f:
            AlignIO.write(MultipleSeqAlignment(group), f, "fasta")
            print(f"Group {i} written to {output_file}")


# Example usage
alignment_file = "aligned_sequences.fasta"
output_prefix = "aligned_sequences_group"
output_folder = "multiple_sequence_alignment"

alignment = AlignIO.read(alignment_file, "fasta")

groups = group_sequences(alignment)
write_groups(groups, output_prefix, output_folder)


def visualize_all_alignments(folder_path, output_folder):
    """Visualize all alignments in a folder."""
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Iterate over each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".fasta"):  # Assuming all alignment files are in FASTA format
            # Generate the output path for the visualization
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.png")
            
            # Generate the full path to the alignment file
            msa_file = os.path.join(folder_path, filename)
            
            # Visualize the alignment and save it to the output path
            visualize_alignment_with_pyMSAviz(msa_file, output_path)


# Example usage
alignment_folder = "multiple_sequence_alignment"
output_folder = "alignment_visualizations"

visualize_all_alignments(alignment_folder, output_folder)

