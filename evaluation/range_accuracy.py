import argparse
import re

def read_ranges_from_file(file_path):
    ranges = []
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r'\((-?\d+\.\d+), (-?\d+\.\d+)\)', line)
            if match:
                min_val = float(match.group(1))
                max_val = float(match.group(2))
                ranges.append((round(min_val, 2), round(max_val, 2)))
    return ranges

def read_llm_ranges_from_file(file_path):
    ranges = []
    with open(file_path, 'r') as file:
        for line in file:
            min_val, max_val = line.strip().split(', ')
            ranges.append((float(min_val), float(max_val)))
    return ranges

def compare_ranges(actual_ranges, llm_ranges):
    if len(actual_ranges) != len(llm_ranges):
        raise ValueError("The number of actual and LLM ranges must be the same.")

    correct_count = 0
    for actual_range, llm_range in zip(actual_ranges, llm_ranges):
        if actual_range == llm_range:
            correct_count += 1

    accuracy = correct_count / len(actual_ranges)
    return accuracy

def evaluate_accuracy(actual_file, llm_file):
    actual_ranges = read_ranges_from_file(actual_file)
    llm_ranges = read_llm_ranges_from_file(llm_file)
    accuracy = compare_ranges(actual_ranges, llm_ranges)
    return accuracy

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluate accuracy of "determine range" results using exact match.')
    parser.add_argument('--actual_file', type=str, required=True, help='Path to the file containing actual ranges.')
    parser.add_argument('--llm_file', type=str, required=True, help='Path to the file containing LLM ranges.')
    args = parser.parse_args()

    actual_file = args.actual_file
    llm_file = args.llm_file

    accuracy = evaluate_accuracy(actual_file, llm_file)
    print(f"Accuracy: {accuracy:.4f}")