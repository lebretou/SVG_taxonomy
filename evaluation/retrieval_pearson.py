import os
import re
import sys
import pandas as pd
from scipy.stats import pearsonr

def extract_number(file_name):
    match = re.search(r'_(\d+)\.csv$', file_name)
    return int(match.group(1)) if match else 0

def calculate_pearson(folder1, folder2, exclude_indices=[]):
    # List all CSV files in both folders
    files1 = sorted([f for f in os.listdir(folder1) if f.endswith('.csv')], key=extract_number)
    files2 = sorted([f for f in os.listdir(folder2) if f.endswith('.csv')], key=extract_number)
    
    if len(files1) != len(files2):
        raise ValueError("The number of files in both folders must be the same.")
    
    correlations = []
    for i, (file1, file2) in enumerate(zip(files1, files2)):
        # Skip files based on exclude_indices
        if i in exclude_indices:
            continue
        
        # Read the CSV files
        df1 = pd.read_csv(os.path.join(folder1, file1))
        df2 = pd.read_csv(os.path.join(folder2, file2))
        
        # Ensure both dataframes contain the required columns
        if 'Y' not in df1 or 'Y' not in df2:
            raise ValueError(f"Both CSV files must contain a 'Y' column. Check files: {file1}, {file2}")
        
        # Calculate Pearson correlation for the 'Y' column
        try:
            corr, _ = pearsonr(df1['Y'], df2['Y'])
            if corr < 0.9:
                print(f"File pair {i} ({file1}, {file2}) did not reach a correlation of 0.9. Correlation: {corr}")
            correlations.append(corr)
        except ValueError as e:
            print(f"Error calculating Pearson correlation for files {file1} and {file2}: {str(e)}")
            continue
    
    # Return the average Pearson correlation
    return sum(correlations) / len(correlations) if correlations else 0

if __name__ == "__main__":
    
    input_folder1 = '../dataset/bar/hard' 
    input_folder2 = '../results/bar/retrieval/hard_unlabeled'
    exclude_indices = []

    # Check for exclude_indices flag

    average_correlation = calculate_pearson(input_folder1, input_folder2, exclude_indices)
    print(f"Average Pearson Correlation: {average_correlation}")
