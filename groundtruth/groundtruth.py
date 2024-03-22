import os
import csv
import argparse
import re

def extract_number(file_name):
    match = re.search(r'_(\d+)\.csv$', file_name)
    if match:
        return int(match.group(1))
    return 0

def calculate_ranges(folder_path, output_file):
    # Initialize an empty list to store the ranges
    ranges = []

    # Get a list of all CSV files in the folder
    csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]

    # Sort the CSV files based on the extracted numbers in the filenames
    sorted_files = sorted(csv_files, key=extract_number)

    # Iterate over each sorted file
    for filename in sorted_files:
        file_path = os.path.join(folder_path, filename)

        # Initialize variables to store the minimum and maximum values
        min_value = float("inf")
        max_value = float("-inf")

        # Read the CSV file and calculate the range of the "Y" column
        with open(file_path, "r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                y_value = float(row["Y"])
                min_value = min(min_value, y_value)
                max_value = max(max_value, y_value)

        # Append the range tuple to the list
        ranges.append((min_value, max_value))

    # Write the ranges to the output file
    with open(output_file, "w") as file:
        for range_tuple in ranges:
            file.write(f"{range_tuple}\n")

    print("Range calculation completed. Results saved in", output_file)

def calculate_means(folder_path, output_file):
    # Initialize an empty list to store the means
    means = []

    # Get a list of all CSV files in the folder
    csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]

    # Sort the CSV files based on the extracted numbers in the filenames
    sorted_files = sorted(csv_files, key=extract_number)

    # Iterate over each sorted file
    for filename in sorted_files:
        file_path = os.path.join(folder_path, filename)

        # Initialize variables to store the sum and count of "Y" values
        y_sum = 0
        y_count = 0

        # Read the CSV file and calculate the mean of the "Y" column
        with open(file_path, "r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                y_value = float(row["Y"])
                y_sum += y_value
                y_count += 1

        # Calculate the mean and append it to the list
        mean = y_sum / y_count if y_count > 0 else 0
        means.append(mean)

    # Write the means to the output file
    with open(output_file, "w") as file:
        for mean in means:
            file.write(f"{mean}\n")

    print("Mean calculation completed. Results saved in", output_file)

if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Calculate ranges or means of Y column in CSV files")
    parser.add_argument("input_folder", help="Path to the folder containing CSV files")
    parser.add_argument("output_file", help="Path to the output file")
    parser.add_argument("calculation_type", choices=["range", "mean"], help="Type of calculation to perform")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the appropriate function based on the calculation type
    if args.calculation_type == "range":
        calculate_ranges(args.input_folder, args.output_file)
    elif args.calculation_type == "mean":
        calculate_means(args.input_folder, args.output_file)