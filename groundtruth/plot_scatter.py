import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import re

def extract_number(file_name):
    match = re.search(r'_(\d+)\.csv$', file_name)
    if match:
        return int(match.group(1))
    return 0

def plot_csv_files(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get a list of CSV files in the input folder
    csv_files = sorted([file for file in os.listdir(input_folder) if file.endswith('.csv')], key=extract_number)

    for csv_file in csv_files:
        # Read the CSV file into a DataFrame
        file_path = os.path.join(input_folder, csv_file)
        df = pd.read_csv(file_path)

        # Get unique cluster labels and outlier label
        labels = df['Label'].unique()
        cluster_labels = [label for label in labels if label.startswith('cluster_')]
        outlier_label = 'outlier' if 'outlier' in labels else None

        # Create a figure and axis
        fig, ax = plt.subplots()

        # Plot data points for each cluster with different colors
        colors = plt.cm.get_cmap('tab10', len(cluster_labels))
        for i, cluster_label in enumerate(cluster_labels):
            cluster_data = df[df['Label'] == cluster_label]
            ax.scatter(cluster_data['X'], cluster_data['Y'], color=colors(i), label=cluster_label)

        # Plot outliers with a different color
        if outlier_label is not None:
            outlier_data = df[df['Label'] == outlier_label]
            ax.scatter(outlier_data['X'], outlier_data['Y'], color='red', label=outlier_label)

        # Set labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(f'Plot of {csv_file}')
        ax.legend()

        # Save the plot as an image file
        plot_file = csv_file.replace('.csv', '.png')
        plot_path = os.path.join(output_folder, plot_file)
        plt.savefig(plot_path)

        # Close the figure to free up memory
        plt.close(fig)

    print(f"Plots saved in {output_folder}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create plots from CSV files.')
    parser.add_argument('--input_folder', type=str, required=True, help='Path to the input folder containing CSV files.')
    parser.add_argument('--output_folder', type=str, required=True, help='Path to the output folder for saving plots.')
    args = parser.parse_args()

    input_folder = args.input_folder
    output_folder = args.output_folder

    plot_csv_files(input_folder, output_folder)