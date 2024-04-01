import argparse

def read_values_from_file(file_path):
    with open(file_path, 'r') as file:
        values = [float(line.strip()) for line in file]
    return values

def compare_values(actual_values, computed_values):
    if len(actual_values) != len(computed_values):
        raise ValueError("The number of actual and computed values must be the same.")

    correct_count = 0
    for actual_value, computed_value in zip(actual_values, computed_values):
        if round(actual_value, 2) == round(computed_value, 2):
            correct_count += 1

    accuracy = correct_count / len(actual_values)
    return accuracy

def evaluate_accuracy(actual_file, computed_file):
    actual_values = read_values_from_file(actual_file)
    computed_values = read_values_from_file(computed_file)
    accuracy = compare_values(actual_values, computed_values)
    return accuracy

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluate accuracy of mean values using exact match.')
    parser.add_argument('--actual_file', type=str, required=True, help='Path to the file containing actual mean values.')
    parser.add_argument('--computed_file', type=str, required=True, help='Path to the file containing computed mean values.')
    args = parser.parse_args()

    actual_file = args.actual_file
    computed_file = args.computed_file

    accuracy = evaluate_accuracy(actual_file, computed_file)
    print(f"Accuracy: {accuracy:.4f}")