# Import necessary modules
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from Bio import SeqIO, AlignIO
from Bio.Align.Applications import MafftCommandline
from Bio.Align import MultipleSeqAlignment
from Bio.SeqRecord import SeqRecord
import panel as pn
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.glyphs import Text, Rect
from bokeh.layouts import gridplot
import numpy as np
from bokeh.io.export import export_png
from bokeh.layouts import column


def create_directory(directory):
    """Create a directory if it does not exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def concatenate_fasta_files(fasta_files, output_file):
    """Concatenate all the FASTA files into a single file."""
    print(f"Concatenating {len(fasta_files)} FASTA files into {output_file}")
    with open(output_file, 'w') as outfile:
        for fname in fasta_files:
            with open(fname) as infile:
                outfile.write(infile.read())
    print(f"Concatenation complete. Output file saved to {output_file}")
    return output_file


def perform_alignment_mafft(input_file, output_alignment):
    """Perform multiple sequence alignment using MAFFT."""
    print(f"Starting multiple sequence alignment using MAFFT on {input_file}")
    mafft_cline = MafftCommandline(input=input_file, thread=2)  # Adjust the number of threads as needed
    try:
        stdout, stderr = mafft_cline()
        print(stdout)  # Print stdout for debugging purposes
        print(stderr)  # Print stderr for debugging purposes
        if os.path.exists(output_alignment):
            os.remove(output_alignment)  # Remove the file if it already exists
        with open(output_alignment, "w") as handle:
            handle.write(stdout)
        print("Alignment complete. Aligned sequences saved to", output_alignment)
        print("Alignment process completed.")
    except Exception as e:
        print("An error occurred during MAFFT execution:", e)




def view_alignment(aln, fontsize="9pt", plot_width=800):
    """Bokeh sequence alignment view"""
    seqs = [rec.seq for rec in aln]
    ids = [rec.id for rec in aln]
    text = [i for s in list(seqs) for i in s]
    colors = get_colors(seqs)
    N = len(seqs[0])
    S = len(seqs)
    width = .4
    x = np.arange(1, N + 1)
    y = np.arange(0, S, 1)
    xx, yy = np.meshgrid(x, y)
    gx = xx.ravel()
    gy = yy.flatten()
    recty = gy + .5
    h = 1 / S
    source = ColumnDataSource(dict(x=gx, y=gy, recty=recty, text=text, colors=colors))
    plot_height = len(seqs) * 15 + 50
    x_range = Range1d(0, N + 1, bounds='auto')
    if N > 100:
        viewlen = 100
    else:
        viewlen = N
    view_range = (0, viewlen)
    tools = "xpan, xwheel_zoom, reset, save"
    p = figure(title=None, width=plot_width, height=50,
               x_range=x_range, y_range=(0, S), tools=tools,
               min_border=0, toolbar_location='below')
    rects = Rect(x="x", y="recty", width=1, height=1, fill_color="colors",
                 line_color=None, fill_alpha=0.6)
    p.add_glyph(source, rects)
    p.yaxis.visible = False
    p.grid.visible = False
    p1 = figure(title=None, width=plot_width, height=plot_height,
                x_range=view_range, y_range=ids, tools="xpan,reset",
                min_border=0, toolbar_location='below')  
    glyph = Text(x="x", y="y", text="text", text_align='center', text_color="black",
                 text_font="courier", text_font_size=fontsize)
    p1.add_glyph(source, glyph)
    rects = Rect(x="x", y="recty", width=1, height=1, fill_color="colors",
                 line_color=None, fill_alpha=0.4)
    p1.add_glyph(source, rects)
    p1.grid.visible = False
    p1.xaxis.major_label_text_font_style = "bold"
    p1.yaxis.minor_tick_line_width = 0
    p1.yaxis.major_tick_line_width = 0
    return p, p1


def visualize_alignment_with_bokeh(alignment, output_directory):
    p, p1 = view_alignment(alignment, plot_width=900)
    layout = column(p, p1)
    output_path = os.path.join(output_directory, "alignment_plot.png")
    export_png(layout, filename=output_path)
    pn.pane.Bokeh(layout).show()


def get_colors(seqs):
    # make colors for nucleotides in sequence
    text = [i for s in list(seqs) for i in s]
    # Use color scheme for nucleotides
    clrs = {'a': '#FF0000', 'c': '#0000FF', 'g': '#FFA500', 't': '#FFFF00'}
    problematic_nucleotides = [i for i in text if i not in clrs]
    if problematic_nucleotides:
        print("Problematic nucleotides:", set(problematic_nucleotides))
    colors = [clrs.get(i, '#999999') for i in text]  # Use '#999999' for unknown nucleotides
    return colors


def main():
    fasta_files = glob.glob(os.path.join("fasta", "*.fasta"))
    if not fasta_files:
        print("No FASTA files found in the 'fasta' directory.")
        return
    output_directory = "output"
    create_directory(output_directory)
    concatenated_file = concatenate_fasta_files(fasta_files, os.path.join(output_directory, 'all_sequences.fasta'))
    output_alignment = os.path.join(output_directory, "aligned_sequences.fasta")
    perform_alignment_mafft(concatenated_file, output_alignment)
    if os.path.exists(output_alignment):
        alignment = AlignIO.read(output_alignment, "fasta")
        visualize_alignment_with_bokeh(alignment, output_directory)
        print("Alignment visualization saved in the 'output' directory.")
    else:
        print("No alignment file found. Visualization could not be generated.")
    print("Current working directory:", os.getcwd())


if __name__ == "__main__":
    main()
