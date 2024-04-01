import os
import csv
import argparse
import re

def extract_number(file_name):
    match = re.search(r'_(\d+)\.csv$', file_name)
    if match:
        return int(match.group(1))
    return 0

def read_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            x = float(row[0])
            y = float(row[1])
            data.append((x, y))
    return data

def compare_data(actual_data, retrieved_data):
    actual_data = set((round(x, 2), round(y, 2)) for x, y in actual_data)
    retrieved_data = set(retrieved_data)

    correct_count = len(actual_data.intersection(retrieved_data))
    total_count = len(actual_data)

    accuracy = correct_count / total_count
    return accuracy

def evaluate_accuracy(actual_folder, retrieved_folder):
    actual_files = sorted([file for file in os.listdir(actual_folder) if file.endswith('.csv')])
    retrieved_files = sorted([file for file in os.listdir(retrieved_folder) if file.endswith('.csv')])

    if len(actual_files) != len(retrieved_files):
        raise ValueError("The number of files in the actual and retrieved folders must be the same.")

    total_accuracy = 0
    for actual_file, retrieved_file in zip(actual_files, retrieved_files):
        actual_data = read_csv(os.path.join(actual_folder, actual_file))
        retrieved_data = read_csv(os.path.join(retrieved_folder, retrieved_file))
        accuracy = compare_data(actual_data, retrieved_data)
        total_accuracy += accuracy

    overall_accuracy = total_accuracy / len(actual_files)
    return overall_accuracy

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluate accuracy using exact match.')
    parser.add_argument('--actual_folder', type=str, required=True, help='Path to the folder containing actual data CSV files.')
    parser.add_argument('--retrieved_folder', type=str, required=True, help='Path to the folder containing retrieved data CSV files.')
    args = parser.parse_args()

    actual_folder = args.actual_folder
    retrieved_folder = args.retrieved_folder

    overall_accuracy = evaluate_accuracy(actual_folder, retrieved_folder)
    print(f"Overall accuracy: {overall_accuracy:.4f}")