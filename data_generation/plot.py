import os
import pandas as pd
import matplotlib.pyplot as plt
import re
import argparse
import seaborn as sns
import plotly.express as px
from adjustText import adjust_text

def extract_number(file_name):
    match = re.search(r'_(\d+)\.csv$', file_name)
    if match:
        return int(match.group(1))
    return 0

# Function to plot and save scatter plots from all CSV files in a folder
def plot_scatter(source_folder, target_folder, label):
    # Check if the target folder exists; if not, create it
    os.makedirs(target_folder, exist_ok=True)
    
    # List all CSV files in the source folder
    csv_files = sorted([f for f in os.listdir(source_folder) if f.endswith('.csv')], key=extract_number)
    
    for csv_file in csv_files:
        # Read the dataset
        df = pd.read_csv(os.path.join(source_folder, csv_file))
        
        # Create scatter plot
        plt.figure(figsize=(6, 4),facecolor='none')
        plt.scatter(df['X'], df['Y'], alpha=0.6)

        # if label:
        #     for i in range(len(df['X'])):
        #         plt.text(df['X'][i], df['Y'][i], f"({df['X'][i]:.2f}, {df['Y'][i]:.2f})", fontsize=8)
        if label:
            texts = []
            for i in range(len(df['X'])):
                texts.append(plt.text(df['X'][i], df['Y'][i], f"({df['X'][i]:.2f}, {df['Y'][i]:.2f})", fontsize=8))

            adjust_text(texts)
        
        # Omit titles, grid lines, and labels
        plt.title('')
        plt.grid(False)
        plt.xlabel('')
        plt.ylabel('')
        # plt.xticks([])
        # plt.yticks([])
        plt.legend([],[], frameon=False)
        
        # Save the plot to the target folder
        plot_filename = csv_file.replace('.csv', '.svg')
        plt.savefig(os.path.join(target_folder, plot_filename))
        
        # Close the figure to free memory
        plt.close()

def plot_line(source_folder, target_folder, label):
    # Check if the target folder exists; if not, create it
    os.makedirs(target_folder, exist_ok=True)
    
    # List all CSV files in the source folder
    csv_files = sorted([f for f in os.listdir(source_folder) if f.endswith('.csv')], key=extract_number)
    
    for csv_file in csv_files:
        # Read the dataset
        df = pd.read_csv(os.path.join(source_folder, csv_file))
        
        # Create line plot
        plt.figure(figsize=(6, 4), facecolor='none')
        plt.plot(df['X'], df['Y'], linewidth=1.5)
        
        # Add markers to the data points
        plt.scatter(df['X'], df['Y'], alpha=0.8)

        # if label:
        #     for i in range(len(df['X'])):
        #         plt.text(df['X'][i], df['Y'][i], f"({df['X'][i]:.2f}, {df['Y'][i]:.2f})", fontsize=8)
        if label:
            texts = []
            for i in range(len(df['X'])):
                texts.append(plt.text(df['X'][i], df['Y'][i], f"({df['X'][i]:.2f}, {df['Y'][i]:.2f})", fontsize=8))

            adjust_text(texts)
        
        # Omit titles, grid lines, and labels
        plt.title('')
        plt.grid(False)
        plt.xlabel('')
        plt.ylabel('')
        
        # Adjust the plot limits to remove excess white space
        # plt.xlim(df['X'].min(), df['X'].max())
        # plt.ylim(df['Y'].min(), df['Y'].max())
        
        # Remove the legend
        plt.legend([], [], frameon=False)
        
        # Save the plot to the target folder
        plot_filename = csv_file.replace('.csv', '.svg')
        plt.savefig(os.path.join(target_folder, plot_filename))
        
        # Close the figure to free memory
        plt.close()


def plot_bar(source_folder, target_folder, label):
    # Check if the target folder exists; if not, create it
    os.makedirs(target_folder, exist_ok=True)
    
    # List all CSV files in the source folder
    csv_files = sorted([f for f in os.listdir(source_folder) if f.endswith('.csv')], key=extract_number)
    
    for csv_file in csv_files:
        # Read the dataset
        df = pd.read_csv(os.path.join(source_folder, csv_file))
        
        # Create bar plot
        plt.figure(figsize=(6, 4), facecolor='none')
        plt.bar(df['X'], df['Y'], width=0.8)
        
        # Add data value labels if specified
        # if label:
        #     for i in range(len(df['X'])):
        #         plt.text(df['X'][i], df['Y'][i], f"({df['X'][i]},{df['Y'][i]:.2f})", ha='center', va='bottom', fontsize=8)
        
        if label:
            texts = []
            for i in range(len(df['X'])):
                texts.append(plt.text(df['X'][i], df['Y'][i], f"({df['X'][i]}, {df['Y'][i]:.2f})", fontsize=7))
            
            adjust_text(texts)

        # Omit titles, grid lines, and labels
        plt.title('')
        plt.grid(False)
        plt.xlabel('')
        plt.ylabel('')
        
        # Adjust the plot limits to remove excess white space
        plt.xlim(df['X'].min() - 0.5, df['X'].max() + 0.5)
        plt.ylim(0, df['Y'].max() * 1.1)
        
        # Remove the legend
        plt.legend([], [], frameon=False)
        
        # Save the plot to the target folder
        plot_filename = csv_file.replace('.csv', '.svg')
        plt.savefig(os.path.join(target_folder, plot_filename))
        
        # Close the figure to free memory
        plt.close()
    
# Seaborn plotting functions
def plot_scatter_seaborn(source_folder, target_folder, label):
    os.makedirs(target_folder, exist_ok=True)
    csv_files = sorted([f for f in os.listdir(source_folder) if f.endswith('.csv')], key=extract_number)
    for csv_file in csv_files:
        df = pd.read_csv(os.path.join(source_folder, csv_file))
        plt.figure(figsize=(6, 4), facecolor='none')
        sns.scatterplot(x='X', y='Y', data=df, alpha=0.6)
        if label:
            texts = []
            for i in range(len(df['X'])):
                texts.append(plt.text(df['X'][i], df['Y'][i], f"({df['X'][i]:.2f}, {df['Y'][i]:.2f})", fontsize=8))
            adjust_text(texts)
        plt.title('')
        plt.grid(False)
        plt.xlabel('')
        plt.ylabel('')
        plt.legend([],[], frameon=False)
        plot_filename = csv_file.replace('.csv', '.svg')
        plt.savefig(os.path.join(target_folder, plot_filename))
        plt.close()

def plot_line_seaborn(source_folder, target_folder, label):
    os.makedirs(target_folder, exist_ok=True)
    csv_files = sorted([f for f in os.listdir(source_folder) if f.endswith('.csv')], key=extract_number)
    for csv_file in csv_files:
        df = pd.read_csv(os.path.join(source_folder, csv_file))
        plt.figure(figsize=(6, 4), facecolor='none')
        sns.lineplot(x='X', y='Y', data=df, linewidth=1.5)
        sns.scatterplot(x='X', y='Y', data=df, alpha=0.8)
        if label:
            texts = []
            for i in range(len(df['X'])):
                texts.append(plt.text(df['X'][i], df['Y'][i], f"({df['X'][i]:.2f}, {df['Y'][i]:.2f})", fontsize=8))
            adjust_text(texts)
        plt.title('')
        plt.grid(False)
        plt.xlabel('')
        plt.ylabel('')
        plt.legend([], [], frameon=False)
        plot_filename = csv_file.replace('.csv', '.svg')
        plt.savefig(os.path.join(target_folder, plot_filename))
        plt.close()

def plot_bar_seaborn(source_folder, target_folder, label):
    os.makedirs(target_folder, exist_ok=True)
    csv_files = sorted([f for f in os.listdir(source_folder) if f.endswith('.csv')], key=extract_number)
    for csv_file in csv_files:
        df = pd.read_csv(os.path.join(source_folder, csv_file))
        plt.figure(figsize=(6, 4), facecolor='none')
        sns.barplot(x='X', y='Y', data=df)
        if label:
            texts = []
            for i in range(len(df['X'])):
                texts.append(plt.text(df['X'][i], df['Y'][i], f"({df['X'][i]}, {df['Y'][i]:.2f})", fontsize=7))
            adjust_text(texts)
        plt.title('')
        plt.grid(False)
        plt.xlabel('')
        plt.ylabel('')
        plt.xlim(df['X'].min() - 0.5, df['X'].max() + 0.5)
        plt.ylim(0, df['Y'].max() * 1.1)
        plt.legend([], [], frameon=False)
        plot_filename = csv_file.replace('.csv', '.svg')
        plt.savefig(os.path.join(target_folder, plot_filename))
        plt.close()

def plot_scatter_plotly(source_folder, target_folder, label):
    os.makedirs(target_folder, exist_ok=True)
    csv_files = sorted([f for f in os.listdir(source_folder) if f.endswith('.csv')], key=extract_number)
    for csv_file in csv_files:
        df = pd.read_csv(os.path.join(source_folder, csv_file))
        fig = px.scatter(df, x='X', y='Y', text='X' if label else None)
        fig.update_traces(textposition='top center')
        fig.update_layout(showlegend=False)
        plot_filename = csv_file.replace('.csv', '.svg')
        fig.write_image(os.path.join(target_folder, plot_filename))
        
def main():
    parser = argparse.ArgumentParser(description='Plot and save scatter, line, or bar plots from CSV files.')
    parser.add_argument('--data_type', type=str, required=True, choices=['scatter', 'line', 'bar'], help='Type of plot to generate (scatter, line, or bar)')
    parser.add_argument('--input_folder', type=str, required=True, help='Path to the folder containing CSV files')
    parser.add_argument('--output_folder', type=str, required=True, help='Path to the folder for saving the generated plots')
    parser.add_argument('--label', action='store_true', help='Add data value labels to the plot points')
    parser.add_argument('--library', type=str, required=True, choices=['matplotlib', 'seaborn', 'plotly'], help='Library to use for plotting (matplotlib or seaborn)')

    args = parser.parse_args()

    plot_type = args.data_type
    input_folder = args.input_folder
    output_folder = args.output_folder
    label = args.label
    library = args.library

    if library == 'matplotlib':
        if plot_type == 'scatter':
            plot_scatter(input_folder, output_folder, label)
        elif plot_type == 'line':
            plot_line(input_folder, output_folder, label)
        elif plot_type == 'bar':
            plot_bar(input_folder, output_folder, label)
    elif library == 'seaborn':
        if plot_type == 'scatter':
            plot_scatter_seaborn(input_folder, output_folder, label)
        elif plot_type == 'line':
            plot_line_seaborn(input_folder, output_folder, label)
        elif plot_type == 'bar':
            plot_bar_seaborn(input_folder, output_folder, label)
    elif library == 'plotly':
        if plot_type == 'scatter':
            plot_scatter_plotly(input_folder, output_folder, label)

if __name__ == '__main__':
    main()

