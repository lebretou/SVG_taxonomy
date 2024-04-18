import numpy as np
import pandas as pd
import os
import argparse

def generate_scatter_dataset(n_points, correlation_factor, n_clusters, cluster_bias, num_outliers, file_name, output_folder):
    """
    Generate a scatter plot dataset with similar ranges across different datasets,
    including labels for clusters and outliers.
    """
    total_range_start, total_range_end = 0, 20  # Define total range for clusters
    outlier_range_start, outlier_range_end = -10, 30  # Define range for outliers
    
    cluster_points = n_points // n_clusters
    labels = []
    x = np.array([])
    y = np.array([])
    
    # Evenly spaced cluster centers
    cluster_centers = np.linspace(total_range_start, total_range_end, n_clusters, endpoint=False)
    
    for i, center in enumerate(cluster_centers):
        # Generate cluster data
        x_cluster = np.random.normal(loc=center, scale=1.0, size=cluster_points)
        y_cluster = correlation_factor * x_cluster + np.random.normal(loc=0, scale=1.0, size=cluster_points)
        x = np.concatenate([x, x_cluster])
        y = np.concatenate([y, y_cluster])
        labels += [f'cluster_{i}'] * cluster_points  # Assign cluster label
    
    # Add outliers with controlled placement
    for _ in range(num_outliers):
        while True:
            x_outlier = np.random.uniform(outlier_range_start, outlier_range_end)
            y_outlier = np.random.uniform(outlier_range_start, outlier_range_end)
            
            # Check if the outlier is far away from all clusters
            is_far_away = True
            for i in range(n_clusters):
                cluster_x = x[labels == f'cluster_{i}']
                cluster_y = y[labels == f'cluster_{i}']
                
                if len(cluster_x) > 0:  # Check if the cluster has points
                    distances = np.sqrt((cluster_x - x_outlier)**2 + (cluster_y - y_outlier)**2)
                    if np.min(distances) < 5:  # Adjust the distance threshold as needed
                        is_far_away = False
                        break
            
            if is_far_away:
                x = np.append(x, x_outlier)
                y = np.append(y, y_outlier)
                labels.append('outlier')
                break
    
    # Create DataFrame
    df = pd.DataFrame({'X': x, 'Y': y, 'Label': labels})
    
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Save the dataset
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
        y[idx] += np.random.uniform(18, 20)  
    
    # Add unusual drops
    drop_indices = np.random.choice(range(1, n_points - 1), size=num_drops, replace=False)
    for idx in drop_indices:
        y[idx] -= np.random.uniform(18, 20)  
    
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
        y[idx] += np.random.uniform(18, 20)
    
    # # Add unusual drops (ensure non-negative values)
    drop_indices = np.random.choice(range(1, n_points - 1), size=num_drops, replace=False)
    for idx in drop_indices:
        drop_value = np.random.uniform(10, 15)
        y[idx] = max(0.5, y[idx] - drop_value)
    
    # Create a DataFrame
    df = pd.DataFrame({'X': x, 'Y': y})
    
    # Check if the folder exists; if not, create it
    os.makedirs(output_folder, exist_ok=True)
    
    # Save to CSV in the specified folder
    full_path = os.path.join(output_folder, f'{file_name}.csv')
    df.to_csv(full_path, index=False)

def generate_distribution_dataset(n_points, distribution_type, file_name, output_folder):
    """
    Generate a dataset with a given number of points following a specified distribution type.
    """
    if distribution_type == 'normal':
        x = np.random.normal(loc=0, scale=1, size=n_points)
        y = np.random.normal(loc=0, scale=1, size=n_points)
    elif distribution_type == 'binomial':
        x = np.random.binomial(n=10, p=0.5, size=n_points)
        y = np.random.binomial(n=10, p=0.5, size=n_points)
    elif distribution_type == 'uniform':
        x = np.random.uniform(low=0, high=1, size=n_points)
        y = np.random.uniform(low=0, high=1, size=n_points)
    else:
        raise ValueError(f"Invalid distribution type: {distribution_type}")
    
    # Create a DataFrame
    df = pd.DataFrame({'X': x, 'Y': y})
    
    # Check if the folder exists; if not, create it
    os.makedirs(output_folder, exist_ok=True)
    
    # Save to CSV in the specified folder
    full_path = os.path.join(output_folder, f'{file_name}.csv')
    df.to_csv(full_path, index=False)
    
    print(f"Generated dataset with {distribution_type} distribution: {file_name}.csv")

def generate_distribution_bar_dataset(n_points, distribution_type, file_name, output_folder):
    """
    Generate a dataset for a bar plot with a given number of points following a specified distribution type.
    """
    x = np.arange(1, n_points + 1)
    
    if distribution_type == 'normal':
        y = np.abs(np.random.normal(loc=0, scale=1, size=n_points))
    elif distribution_type == 'binomial':
        y = np.random.binomial(n=10, p=0.5, size=n_points)
    elif distribution_type == 'uniform':
        y = np.random.uniform(low=0, high=1, size=n_points)
    else:
        raise ValueError(f"Invalid distribution type: {distribution_type}")
    
    # Create a DataFrame
    df = pd.DataFrame({'X': x, 'Y': y})
    
    # Check if the folder exists; if not, create it
    os.makedirs(output_folder, exist_ok=True)
    
    # Save to CSV in the specified folder
    full_path = os.path.join(output_folder, f'{file_name}.csv')
    df.to_csv(full_path, index=False)
    
    print(f"Generated distribution bar dataset with {distribution_type} distribution: {file_name}.csv")

def main():
    parser = argparse.ArgumentParser(description='Generate dataset for scatter or line plots.')
    parser.add_argument('--data_type', type=str, required=True, choices=['scatter', 'line', 'bar', 'distribution', 'distribution_bar'], help='Type of dataset to generate (scatter or line)')
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
            correlation_factor = np.random.uniform(-0.5, 0.5)
            n_outliers = 1

            if n_points <= 20: 
                n_clusters = 2
            else:
                n_clusters = 3
                n_outliers = 2
        
            # n_clusters = np.random.randint(2, 5)
            cluster_bias = np.random.uniform(50, 60)
            file_name = f"scatter_data_{i}"
            generate_scatter_dataset(n_points, correlation_factor, n_clusters, cluster_bias, n_outliers , file_name, output_folder)
        elif data_type == 'line':
            correlation_factor = np.random.uniform(-0.6, 0.6)
            num_spikes = np.random.randint(1, 2)
            # num_drops = np.random.randint(1, 2)
            num_drops = 0
            file_name = f"line_data_{i}"
            generate_line_dataset(n_points, correlation_factor, num_spikes, num_drops, file_name, output_folder)
        elif data_type == 'bar':
            num_spikes = 1
            num_drops = 1
            file_name = f"bar_data_{i}"
            generate_bar_dataset(n_points, num_spikes, num_drops, file_name, output_folder)
        elif data_type == 'distribution':
            distribution_types = ['normal', 'binomial', 'uniform']
            distribution_type = np.random.choice(distribution_types)
            file_name = f"data_{i}"
            generate_distribution_dataset(n_points, distribution_type, file_name, output_folder)
        elif data_type == 'distribution_bar':
            distribution_types = ['normal', 'binomial', 'uniform']
            distribution_type = np.random.choice(distribution_types)
            file_name = f"data_{i}"
            generate_distribution_bar_dataset(n_points, distribution_type, file_name, output_folder)

    print(f"Generated {n_datasets} datasets for {data_type} plots.")

if __name__ == '__main__':
    main()