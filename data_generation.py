import numpy as np
import pandas as pd
import os

def generate_scatter_dataset(n_points, correlation_factor, n_clusters, cluster_bias, file_name):
    """
    Generate a scatter plot dataset with a given number of points, correlation factor, number of clusters, and cluster bias.
    """
    cluster_points = n_points // n_clusters  # Ensure n_points is split evenly among the clusters
    cluster_separation = cluster_bias # Starting bias for cluster separation


    x = np.array([])
    y = np.array([])

    for _ in range(n_clusters):
        # Generate cluster data with increased separation for each cluster
        x_cluster = np.random.normal(loc=i * 10 + cluster_separation, scale=1.0, size=cluster_points)
        y_cluster = correlation_factor * x_cluster + np.random.normal(loc=0, scale=1.0, size=cluster_points)
        x = np.concatenate([x, x_cluster])
        y = np.concatenate([y, y_cluster])

        # Increase the separation for the next cluster
        cluster_separation += np.random.uniform(10, 20)  # Adjust this range as needed

    
    # Add an outlier
    x_outlier = np.random.uniform(np.min(x) - 10, np.max(x) + 10, size=1) 
    y_outlier = np.random.uniform(np.min(y) - 10, np.max(y) + 10, size=1) 
    x = np.append(x, x_outlier)
    y = np.append(y, y_outlier)

    # Create a DataFrame
    df = pd.DataFrame({'X': x, 'Y': y})

    # Check if the folder exists; if not, create it
    os.makedirs(folder_path, exist_ok=True)

    # Save to CSV in the specified folder
    full_path = os.path.join(folder_path, f'{file_name}.csv')
    df.to_csv(full_path, index=False)


folder_path = "./dataset/scatter"

# Example usage:
n_datasets = 10  
for i in range(n_datasets):
    n_points = np.random.randint(30, 51)  # Randomly choose between 30 to 50 points
    correlation_factor = np.random.uniform(-10, 10)
    n_clusters = np.random.randint(2, 4)  # Randomly choose the number of clusters (between 1 and 3)
    cluster_bias = np.random.uniform(0, 5)  # Random bias for the first cluster
    file_name = f"scatter_data_{i+1}"

    generate_scatter_dataset(n_points, correlation_factor, n_clusters, cluster_bias, file_name)

print(f"Generated {n_datasets} datasets for scatter plots with varying number of clusters and correlation factors.")
