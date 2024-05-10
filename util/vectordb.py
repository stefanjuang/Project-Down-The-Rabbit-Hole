
# package version faiss-cpu==1.8.0
import numpy as np
import faiss
import os

def create_index(vectors, save_path="vector.index"):
    """
    Creates a FAISS index from a given set of vectors and saves the index to disk.

    Args:
    vectors (numpy.ndarray): A numpy array of shape (nb, d) where 'nb' is the number of base vectors and 'd' is the dimension.
    save_path (str): Path where the index will be saved.

    Returns:
    faiss.IndexIVFPQ: The created FAISS index.
    """
    d = vectors.shape[1]  # dimension of the vectors
    nb = vectors.shape[0]  # number of vectors in the base

    # Use a HNSW index as the quantizer
    quantizer = faiss.IndexHNSWFlat(d, 32)
    nlist = min(100, nb)  # number of Voronoi cells (clusters)
    m = 64  # number of bytes per vector; adjusted to be a factor of 1024

    # Create an IVFPQ index
    index = faiss.IndexIVFPQ(quantizer, d, nlist, m, 8)
    index.train(vectors)
    index.add(vectors)

    # Save the index
    faiss.write_index(index, save_path)

    return index
