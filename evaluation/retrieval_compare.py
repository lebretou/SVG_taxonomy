import os
import matplotlib.pyplot as plt
import csv
import re

def extract_number(file_name):
    match = re.search(r'_(\d+)\.csv$', file_name)
    if match:
        return int(match.group(1))
    return 0

def plot_csv_pairs(folder_a, folder_b, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get the list of CSV files in folder A
    csv_files_a = sorted([file for file in os.listdir(folder_a) if file.endswith('.csv')], key=extract_number)
    
    # Get the list of CSV files in folder B
    csv_files_b = sorted([file for file in os.listdir(folder_b) if file.endswith('.csv')], key=extract_number)

    # Iterate over the pairs of CSV files
    for i, (file_a, file_b) in enumerate(zip(csv_files_a, csv_files_b)):
        try:
            # Read data from CSV file in folder A
            with open(os.path.join(folder_a, file_a), 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip the header row
                data_a = list(reader)

            # Read data from CSV file in folder B
            with open(os.path.join(folder_b, file_b), 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip the header row
                data_b = list(reader)

            # Extract x and y values from data
            x_a = [float(row[0]) for row in data_a]
            y_a = [float(row[1]) for row in data_a]
            x_b = [float(row[0]) for row in data_b]
            y_b = [float(row[1]) for row in data_b]

            # Create a new figure for each pair of CSV files
            plt.figure()

            # Plot the data points from folder A
            plt.scatter(x_a, y_a, color='blue', label=file_a)

            # Plot the data points from folder B
            plt.scatter(x_b, y_b, color='red', label=file_b)

            # Add labels and legend
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.legend()

            # Save the plot as an image file
            output_filename = f"plot_{i}.png"
            output_path = os.path.join(output_folder, output_filename)
            plt.savefig(output_path)

            # Close the figure to free up memory
            plt.close()
        except Exception as e:
            print(f"Error processing files {file_a} and {file_b}: {str(e)}")
            continue

    print("All plots have been saved.")

# Example usage
folder_a = '../dataset/scatter/easy'
folder_b = '../results/scatter/retrieval/easy_labeled'
output_folder = '../results/scatter/retrieval/easy_labeled'

plot_csv_pairs(folder_a, folder_b, output_folder)