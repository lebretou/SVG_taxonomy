import numpy as np
import pandas as pd
import os
import argparse

def generate_scatter_dataset(n_points, correlation_factor, n_clusters, cluster_bias, num_outliers, file_name, output_folder):
    """
    Generate a scatter plot dataset with a given number of points, correlation factor, number of clusters, and cluster bias.
    """
    cluster_points = n_points // n_clusters  # Ensure n_points is split evenly among the clusters
    cluster_separation = cluster_bias # Starting bias for cluster separation


    x = np.array([])
    y = np.array([])

    for i in range(n_clusters):
        # Generate cluster data with increased separation for each cluster
        x_cluster = np.random.normal(loc=i * 10 + cluster_separation, scale=1.0, size=cluster_points)
        y_cluster = correlation_factor * x_cluster + np.random.normal(loc=0, scale=1.0, size=cluster_points)
        x = np.concatenate([x, x_cluster])
        y = np.concatenate([y, y_cluster])

        # Increase the separation for the next cluster
        cluster_separation += np.random.uniform(8, 10)  # Adjust this range as needed

    
    # Add an outlier
    for _ in range(num_outliers):
        x_outlier = np.random.uniform(np.min(x) - 5, np.max(x) + 5, size=1) 
        y_outlier = np.random.uniform(np.min(y) - 5, np.max(y) + 5, size=1) 
        x_outlier = x_outlier * 1.05
        y_outlier = y_outlier * 1.05
        x = np.append(x, x_outlier)
        y = np.append(y, y_outlier)

    # Create a DataFrame
    df = pd.DataFrame({'X': x, 'Y': y})

    # Check if the folder exists; if not, create it
    os.makedirs(output_folder, exist_ok=True)

    # Save to CSV in the specified folder
    full_path = os.path.join(output_folder, f'{file_name}.csv')
    df.to_csv(full_path, index=False)

def generate_line_dataset(n_points, correlation_factor, num_spikes, num_drops, file_name, output_folder):
    """
    Generate a line plot dataset with a given number of points, correlation factor,
    number of unusual spikes, and number of unusual drops.
    """
    x = np.arange(n_points)
    y = correlation_factor * x + np.random.normal(loc=0, scale=1.5, size=n_points)
    
    # Add unusual spikes
    spike_indices = np.random.choice(range(1, n_points - 1), size=num_spikes, replace=False)
    for idx in spike_indices:
        y[idx] += np.random.uniform(10, 12)  
    
    # Add unusual drops
    drop_indices = np.random.choice(range(1, n_points - 1), size=num_drops, replace=False)
    for idx in drop_indices:
        y[idx] -= np.random.uniform(10, 12)  
    
    # Create a DataFrame
    df = pd.DataFrame({'X': x, 'Y': y})
    
    # Check if the folder exists; if not, create it
    os.makedirs(output_folder, exist_ok=True)
    
    # Save to CSV in the specified folder
    full_path = os.path.join(output_folder, f'{file_name}.csv')
    df.to_csv(full_path, index=False)


def generate_bar_dataset(n_points, num_spikes, num_drops, file_name, output_folder):
    """
    Generate a bar plot dataset with a given number of points,
    number of unusual spikes, and number of unusual drops.
    """
    x = np.arange(n_points)
    y = np.random.uniform(low=5, high=10, size=n_points)
    
    # Add unusual spikes
    spike_indices = np.random.choice(range(1, n_points - 1), size=num_spikes, replace=False)
    for idx in spike_indices:
        y[idx] += np.random.uniform(13, 15)
    
    # Add unusual drops (ensure non-negative values)
    drop_indices = np.random.choice(range(1, n_points - 1), size=num_drops, replace=False)
    for idx in drop_indices:
        drop_value = np.random.uniform(5, 8)
        y[idx] = max(0.5, y[idx] - drop_value)
    
    # Create a DataFrame
    df = pd.DataFrame({'X': x, 'Y': y})
    
    # Check if the folder exists; if not, create it
    os.makedirs(output_folder, exist_ok=True)
    
    # Save to CSV in the specified folder
    full_path = os.path.join(output_folder, f'{file_name}.csv')
    df.to_csv(full_path, index=False)


def main():
    parser = argparse.ArgumentParser(description='Generate dataset for scatter or line plots.')
    parser.add_argument('--data_type', type=str, required=True, choices=['scatter', 'line', 'bar'], help='Type of dataset to generate (scatter or line)')
    parser.add_argument('--n_points', type=int, required=True, help='Number of data points to generate')
    parser.add_argument('--n_datasets', type=int, default=1, help='Number of datasets to generate (default: 1)')
    parser.add_argument('--output_folder', type=str, default='./dataset', help='Output folder path (default: ./dataset)')

    args = parser.parse_args()

    data_type = args.data_type
    n_points = args.n_points
    n_datasets = args.n_datasets
    output_folder = args.output_folder

    for i in range(n_datasets):
        if data_type == 'scatter':
            correlation_factor = np.random.uniform(-1, 1)
            n_outliers = 1

            if n_points <= 20: 
                n_clusters = 2
            else:
                n_clusters = 3
        
            # n_clusters = np.random.randint(2, 5)
            cluster_bias = np.random.uniform(50, 60)
            file_name = f"scatter_data_{i}"
            generate_scatter_dataset(n_points, correlation_factor, n_clusters, cluster_bias, n_outliers , file_name, output_folder)
        elif data_type == 'line':
            correlation_factor = np.random.uniform(-0.6, 0.6)
            num_spikes = np.random.randint(1, 2)
            num_drops = np.random.randint(1, 2)
            file_name = f"line_data_{i}"
            generate_line_dataset(n_points, correlation_factor, num_spikes, num_drops, file_name, output_folder)
        elif data_type == 'bar':
            num_spikes = np.random.randint(1, 2)
            num_drops = np.random.randint(1, 2)
            file_name = f"bar_data_{i}"
            generate_bar_dataset(n_points, num_spikes, num_drops, file_name, output_folder)

    print(f"Generated {n_datasets} datasets for {data_type} plots.")

if __name__ == '__main__':
    main()