import os
import pandas as pd
import matplotlib.pyplot as plt

# Function to plot and save scatter plots from all CSV files in a folder
def plot_and_save_all_csv(source_folder, target_folder):
    # Check if the target folder exists; if not, create it
    os.makedirs(target_folder, exist_ok=True)
    
    # List all CSV files in the source folder
    csv_files = [f for f in os.listdir(source_folder) if f.endswith('.csv')]
    
    for csv_file in csv_files:
        # Read the dataset
        df = pd.read_csv(os.path.join(source_folder, csv_file))
        
        # Create scatter plot
        plt.figure(figsize=(6, 4),facecolor='none')
        plt.scatter(df['X'], df['Y'], alpha=0.6)
        
        # Omit titles, grid lines, and labels
        plt.title('')
        plt.grid(False)
        plt.xlabel('')
        plt.ylabel('')
        plt.xticks([])
        plt.yticks([])
        plt.legend([],[], frameon=False)
        
        # Save the plot to the target folder
        plot_filename = csv_file.replace('.csv', '.svg')
        plt.savefig(os.path.join(target_folder, plot_filename))
        
        # Close the figure to free memory
        plt.close()

# Specify source and target folders
source_folder = "./dataset/scatter"  # Replace with your CSV files folder path
target_folder = "./images/scatter"  # Replace with your target folder path for saving plots

# Plot and save
plot_and_save_all_csv(source_folder, target_folder)

print(f"All CSV files from '{source_folder}' have been plotted and saved in '{target_folder}'.")
