import numpy as np
import csv
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import zscore

data = []
genes = []

first = True
max_columns = 0  # Track the maximum number of columns in any row

with open("/home/farah/Pipeline/ge/GSE223073_nor.csv") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter="\t")  # Assuming your CSV is tab-separated
    
    for row in csv_reader:
        if not row:  # Skip empty lines
            continue

        print(row)  # Print each row to check the content

        if first:
            sample_names = row[1:]
            first = False
        else:
            genes.append(row[0])
            # Append only the numeric values after the first element
            numeric_values = [float(value) if value.replace('.', '').isdigit() else 0.0 for value in row[1:]]
            data.append(numeric_values)
            max_columns = max(max_columns, len(numeric_values))

# Ensure all rows have the same number of columns
data = [row + [0.0] * (max_columns - len(row)) for row in data]

data = np.array(data).astype(float)  # Use float instead of int to handle potential non-numeric values

# Calculate Z-score for each column (gene) in the data
zscore_data = np.nan_to_num(zscore(data, axis=1, nan_policy='omit'))

# Set the size of the figure to accommodate more space for x-axis labels
plt.figure(figsize=(10, 8))

# Create a clustermap with adjusted parameters for column clustering
sns_plot = sns.clustermap(zscore_data.T, xticklabels=sample_names, col_cluster=False, col_linkage=None, cmap='coolwarm')

plt.title('Z-Score Heatmap')
plt.xlabel('Samples')
plt.ylabel('Genes')

# Save the heatmap as a PDF file
sns_plot.savefig("/home/farah/Pipeline/ge/zscore_heatmap.pdf")

plt.show()

