import sys
from Bio import AlignIO, SeqIO
from Bio.Seq import Seq
from Bio.Align import MultipleSeqAlignment
from Bio.Phylo.TreeConstruction import DistanceCalculator
import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.models import Range1d
from bokeh.plotting import figure
from bokeh.models.glyphs import Rect
from bokeh.models.glyphs import Text
from bokeh.layouts import gridplot
import panel as pn
from bokeh.io import export_png



# Read the original alignment from "aligned.fasta" in FASTA format
aln = AlignIO.read("aligned_sequences.fasta", "fasta")

# Find the first and last columns with no gaps ("-")
for fcol in range(aln.get_alignment_length()):
    if not "-" in aln[:, fcol]:
        position1 = fcol
        print("First full column is {}".format(fcol))
        break

for lcol in reversed(range(aln.get_alignment_length())):
    if not "-" in aln[:, lcol]:
        position2 = lcol + 1
        print("Last full column is {}".format(lcol))
        break

# Extract the trimmed alignment
trimmed_alignment = aln[:, position1:position2]

print("New alignment:")
print(trimmed_alignment)

# Write the trimmed alignment to a new FASTA file
with open("aligned_trimmed.fasta", "w") as handle:
    count = SeqIO.write(trimmed_alignment, handle, "fasta")

# Read the trimmed alignment from the saved file
trimmed_alignment_read = AlignIO.read("aligned_trimmed.fasta", "fasta")

def sequence_cleaner(fasta_file, min_length=0):
    sequences = {}
    for seq_record in SeqIO.parse(fasta_file, "fasta"):
        sequence = str(seq_record.seq).upper()
        if len(sequence) >= min_length:
            if sequence not in sequences:
                sequences[sequence] = seq_record.id
            else:
                sequences[sequence] += "_" + seq_record.id

    with open("clear_" + fasta_file, "w+") as output_file:
        for sequence in sequences:
            output_file.write(">" + sequences[sequence] + "\n" + sequence + "\n")
    print("CLEAN!!!\nPlease check clear_" + fasta_file)


# Function to view the sequence alignment using Bokeh
def view_alignment(aln, fontsize="9pt", plot_width=800):
    # Setting up the nucleotide color code
    def get_colors(seqs):
    	text = [i for s in list(seqs) for i in s]
    	clrs = {'a': 'green', 't': 'blue', 'c': 'orange', 'g': 'red', '-': 'white'}
    	# Assign a default color for any unrecognized base
    	colors = [clrs.get(i, 'gray') for i in text]
    	return colors


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
    p = figure(title=None, width=plot_width, height=50, x_range=x_range, y_range=(0, S), tools=tools,
               min_border=0, toolbar_location='below')
    rects = Rect(x="x", y="recty", width=1, height=1, fill_color="colors", line_color=None, fill_alpha=0.6)
    p.add_glyph(source, rects)
    p.yaxis.visible = False
    p.grid.visible = False
    p1 = figure(title=None, width=plot_width, height=plot_height, x_range=view_range, y_range=ids,
                tools="xpan,reset", min_border=0, toolbar_location='below')
    glyph = Text(x="x", y="y", text="text", text_align='center', text_color="black", text_font="monospace",
                 text_font_size=fontsize)
    rects = Rect(x="x", y="recty", width=1, height=1, fill_color="colors", line_color=None, fill_alpha=0.4)
    p1.add_glyph(source, glyph)
    p1.add_glyph(source, rects)
    p1.grid.visible = False
    p1.xaxis.major_label_text_font_style = "bold"
    p1.yaxis.minor_tick_line_width = 0
    p1.yaxis.major_tick_line_width = 0
    p = gridplot([[p], [p1]], toolbar_location='below')
    return p


# Name of the MSA file (including the filetype)
MSAfile = 'aligned_trimmed.fasta'
MSAformat = 'fasta'

# Read the alignment from the cleaned and trimmed file
aln = AlignIO.read(MSAfile, MSAformat)

# Calculate the distance matrix
calculator = DistanceCalculator('identity')
dm = calculator.get_distance(aln)
print("Distance Matrix:")
print(dm)

# Use the cleaned and trimmed alignment in the Bokeh visualization
p = view_alignment(aln, plot_width=900)
pn.pane.Bokeh(p)

# Use the cleaned and trimmed alignment in the Bokeh visualization
p = view_alignment(aln, plot_width=900)

# Set the filename for the saved PNG file
png_filename = "alignment_plot.png"

# Save the plot as a PNG file
export_png(p, filename=png_filename)

# Display the saved PNG filename
print(f"Plot saved as {png_filename}")

