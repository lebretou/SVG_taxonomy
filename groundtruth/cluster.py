import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.covariance import EllipticEnvelope

# Create a folder to store the results
csv_folder = "../dataset/scatter"
output_folder = "../images/scatter/cluster_groundtruth"
os.makedirs(output_folder, exist_ok=True)

# Get a list of all CSV files in the current directory
csv_files = [file for file in os.listdir(csv_folder) if file.endswith(".csv")]

for file in csv_files:
    # Read the CSV file
    file_path = os.path.join(csv_folder, file)
    data = pd.read_csv(file_path)
    X = data["X"].values.reshape(-1, 1)
    Y = data["Y"].values.reshape(-1, 1)

    # Standardize the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    Y_scaled = scaler.fit_transform(Y)
    data_scaled = np.hstack((X_scaled, Y_scaled))

    # Perform clustering using DBSCAN
    dbscan = DBSCAN(eps=0.5, min_samples=5)  # Adjust eps and min_samples as needed
    labels = dbscan.fit_predict(data_scaled)

    # Detect outliers using Elliptic Envelope
    outlier_detector = EllipticEnvelope(contamination=0.05)  # Adjust contamination as needed
    outlier_labels = outlier_detector.fit_predict(data_scaled)
    outlier_mask = outlier_labels == -1

    # Create a color map for clusters and outliers
    unique_labels = np.unique(labels)
    colors = plt.cm.get_cmap("viridis", len(unique_labels))
    color_map = [colors(label) if label != -1 else "red" for label in labels]
    color_map = ["black" if mask else color for mask, color in zip(outlier_mask, color_map)]

    # Plot the data points with cluster colors and outliers
    plt.figure(figsize=(8, 6))
    plt.scatter(X, Y, c=color_map)
    # plt.xlabel("X")
    # plt.ylabel("Y")
    plt.title("")

    # Save the plot
    output_path = os.path.join(output_folder, f"{file[:-4]}_plot.png")
    plt.savefig(output_path)
    plt.close()

print("Clustering and outlier detection completed. Results saved in the 'clustering_results' folder.")