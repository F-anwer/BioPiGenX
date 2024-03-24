import subprocess
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from Bio import Entrez, SeqIO, AlignIO, Phylo
from Bio.Align.Applications import MafftCommandline
from Bio.Align import MultipleSeqAlignment
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import panel as pn
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.glyphs import Text, Rect
from bokeh.layouts import gridplot
import numpy as np
from bokeh.io.export import export_png
from bokeh.io import export_png
from bokeh.layouts import column
from pymsaviz import MsaViz
import random

def setup_entrez(email, api_key):
    Entrez.email = email
    Entrez.api_key = api_key

def read_accession_list(file_path):
    with open(file_path, "r") as infile:
        accession_list = [line.strip() for line in infile]
    return accession_list

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_file(accession, search_db, rettype, retmode):
    handle = Entrez.efetch(db=search_db, id=accession, rettype=rettype, retmode=retmode)
    return handle.read()

def save_file(content, filename):
    with open(filename, "w") as outfile:
        outfile.write(content)

def download_and_save_files(accession_list, search_db):
    rettype = "fasta"
    retmode = "text"

    directory = "multiple_sequence_alignment"
    create_directory(directory)
    fasta_directory = os.path.join(directory, "fasta")
    fna_directory = os.path.join(directory, "fna")
    create_directory(fasta_directory)
    create_directory(fna_directory)

    for accession in accession_list:
        # Download the FNA file
        fna_content = download_file(accession, search_db, "fasta", "text")
        fna_filename = os.path.join(fna_directory, f"{accession}.fna")
        save_file(fna_content, fna_filename)

        # Download the FASTA file
        fasta_filename = os.path.join(fasta_directory, f"{accession}.fasta")
        save_file(fna_content, fasta_filename)

    print("All downloads complete")

def list_fna_files():
    """List all .fna files in the current working directory."""
    fna_files = glob.glob("multiple_sequence_alignment/fna/*.fna")
    print("List of .fna files:", fna_files)
    return fna_files

def concatenate_fna_files(fna_files, output_file):
    """Concatenate all the .fna files into a single file."""
    print(f"Concatenating {len(fna_files)} .fna files into {output_file}")
    with open(output_file, 'w') as outfile:
        for fname in fna_files:
            with open(fname) as infile:
                outfile.write(infile.read())
    print(f"Concatenation complete. Output file saved to {output_file}")
    return output_file

def perform_alignment_mafft(input_file, output_alignment):
    """Perform multiple sequence alignment using MAFFT."""
    print(f"Starting multiple sequence alignment using MAFFT on {input_file}")
    mafft_cline = MafftCommandline(input=input_file)
    stdout, stderr = mafft_cline()

    with open(output_alignment, "w") as handle:
        handle.write(stdout)

    print("Alignment complete. Aligned sequences saved to", output_alignment)
    print("Alignment process completed.")

def visualize_alignment_with_pyMSAviz(msa_file, output_path="multiple_sequence_alignment/msa_plot.png"):
    """Visualize alignment with pyMSAviz and save it to a file."""
    mv = MsaViz(msa_file, start=500, end=1500, wrap_length=60, show_consensus=True)
    mv.set_custom_color_scheme({"a": "red", "c": "skyblue", "t": "lime", "g": "orange"})
    mv.savefig(output_path)  # Save the plot to a file
    print("Alignment visualization saved to", output_path)

def main():
    # Set up Entrez with your email and API key
    setup_entrez("farhaanwer957@gmail.com", "6f5b64b999993fcbcc6cac86c9ad6782fb09")

    # Read the input file with accession numbers
    accession_list = read_accession_list("acc_id.txt")

    # Specify the search database
    search_db = "nuccore"

    # Download and save files
    download_and_save_files(accession_list, search_db)

    # List all the .fna files in the current working directory
    fasta_files = list_fna_files()

    if not fasta_files:
        print("No .fna files found in the current working directory.")
    else:
        # Concatenate all the .fna files into a single file
        concatenated_file = concatenate_fna_files(fasta_files, 'multiple_sequence_alignment/all_sequences.fna')

        # Output file for the aligned sequences
        output_alignment = "multiple_sequence_alignment/aligned_sequences.fasta"

        # Perform multiple sequence alignment using MAFFT
        perform_alignment_mafft(concatenated_file, output_alignment)

        # Visualize the alignment
        visualize_alignment_with_pyMSAviz(output_alignment)

if __name__ == "__main__":
    main()

