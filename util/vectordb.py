
# package version faiss-cpu==1.8.0

import numpy as np
import faiss

def search_vectors(vectors, query_vector, top_k=1000):
    """
    Searches for the top K nearest neighbors of a given query vector within a database of vectors using FAISS.
    
    Args:
    vectors (numpy.ndarray): A numpy array of shape (nb, d) where 'nb' is the number of base vectors and 'd' is the dimension.
    query_vector (numpy.ndarray): A numpy array of shape (nq, d) where 'nq' is the number of query vectors (usually 1).
    top_k (int): The number of nearest neighbors to retrieve.

    Returns:
    tuple: A tuple of two arrays, distances (numpy.ndarray) and indices (numpy.ndarray), representing the nearest neighbors.
    """
    d = 1024  # dimension of the vectors
    nb = vectors.shape[0]  # number of vectors in the base
    
    # Use a HNSW index as the quantizer
    quantizer = faiss.IndexHNSWFlat(d, 32)

    # number of Voronoi cells (clusters)
    nlist = min(100, nb)  # use a smaller number of clusters if there aren't many vectors
    m = 64  # number of bytes per vector; adjusted to be a factor of 1024

    # Create an IVFPQ index
    index = faiss.IndexIVFPQ(quantizer, d, nlist, m, 8)
    index.train(vectors)
    index.add(vectors)

    # Search the index for the top K nearest neighbors
    distances, indices = index.search(query_vector, top_k)

    return distances, indices

# Example usage of the function:
# vectors = np.random.random((10000, 1024)).astype('float32')  # Random base vectors
# query_vector = np.random.random((1, 1024)).astype('float32')  # Random query vector
# distances, indices = search_vectors(vectors, query_vector, top_k=1000)
# print("Indices of Nearest Neighbors:", indices)
# print("Distances of Nearest Neighbors:", distances)
