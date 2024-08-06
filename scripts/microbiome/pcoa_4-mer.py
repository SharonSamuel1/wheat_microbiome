import pandas as pd
from scipy.spatial.distance import pdist, squareform
from skbio.stats.ordination import pcoa
import matplotlib.pyplot as plt

def read_csv(file_path):
    """
    Reads a CSV file containing 4-mer occurrences.
    Assumes the first column is the sample IDs and the rest are 4-mer counts.
    """
    return pd.read_csv(file_path, index_col=0)

def calculate_bray_curtis(data):
    """
    Calculates the Bray-Curtis dissimilarity matrix.
    """
    dissimilarity_matrix = pdist(data.values, metric='braycurtis')
    return squareform(dissimilarity_matrix)

def perform_pcoa(dissimilarity_matrix):
    """
    Performs Principal Coordinates Analysis (PCoA) on the dissimilarity matrix.
    """
    return pcoa(dissimilarity_matrix)

def plot_pcoa(pcoa_results, sample_ids):
    """
    Plots the results of the PCoA.
    """
    plt.figure(figsize=(10, 8))
    plt.scatter(pcoa_results.samples['PC1'], pcoa_results.samples['PC2'], c='blue', marker='o')
    for i, sample_id in enumerate(sample_ids):
        plt.text(pcoa_results.samples['PC1'][i], pcoa_results.samples['PC2'][i], sample_id)

    plt.xlabel(f'PC1 ({pcoa_results.proportion_explained[0]*100:.2f}% variance)')
    plt.ylabel(f'PC2 ({pcoa_results.proportion_explained[1]*100:.2f}% variance)')
    plt.title('PCoA of 4-mer Occurrences Using Bray-Curtis Dissimilarity')
    plt.grid(True)
    plt.show()

def main(file_path):
    data = read_csv(file_path)
    sample_ids = data.index.tolist()
    bray_curtis_matrix = calculate_bray_curtis(data)
    pcoa_results = perform_pcoa(bray_curtis_matrix)
    plot_pcoa(pcoa_results, sample_ids)

# Example usage
file_path = 'your_4mer_occurrences.csv'
main(file_path)
