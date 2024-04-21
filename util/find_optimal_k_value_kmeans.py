import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def find_optimal_clusters(data, max_k):
    """
    Function to compute K-means with varying k and plot the SSD (Elbow Method) to find the optimal k.
    
    Args:
    data (numpy.ndarray): The input data to cluster.
    max_k (int): The maximum number of clusters to test.
    
    Returns:
    None
    """
    ssds = []
    ks = range(1, max_k + 1)
    
    for k in ks:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(data)
        ssds.append(kmeans.inertia_)  # Sum of squared distances of samples to their closest cluster center

    plt.figure(figsize=(10, 6))
    plt.plot(ks, ssds, marker='o')
    plt.title('Elbow Method For Optimal k')
    plt.xlabel('Number of clusters k')
    plt.ylabel('Sum of squared distances')
    plt.grid(True)
    plt.show()

