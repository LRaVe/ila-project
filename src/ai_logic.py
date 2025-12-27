"""AI logic module for generating embeddings using sentence-transformers."""

import numpy as np
from sentence_transformers import SentenceTransformer
from typing import Union

# Load the model once at module level for efficiency
_model = None


def get_model() -> SentenceTransformer:
    """Get or initialize the sentence transformer model.
    
    Returns:
        SentenceTransformer model instance.
    """
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


def text_to_vector(text: str) -> np.ndarray:
    """Convert a string into a vector embedding.
    
    Args:
        text: The input text string to convert.
        
    Returns:
        Numpy array representing the embedding vector.
    """
    model = get_model()
    embedding = model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
    return embedding


def vector_to_bytes(vector: np.ndarray) -> bytes:
    """Convert a numpy array to bytes for database storage.
    
    Args:
        vector: The numpy array to convert.
        
    Returns:
        Bytes representation of the vector.
    """
    return vector.tobytes()


def bytes_to_vector(data: bytes) -> np.ndarray:
    """Convert bytes back to numpy array from database.
    
    Args:
        data: The bytes data from database.
        
    Returns:
        Numpy array representing the embedding vector (1D array).
    """
    if data is None:
        return None
    # The model 'all-MiniLM-L6-v2' produces 384-dimensional vectors
    vector = np.frombuffer(data, dtype=np.float32)
    # Ensure it's a 1D array
    return vector.flatten()


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Calculate cosine similarity between two vectors.
    
    Args:
        vec1: First embedding vector.
        vec2: Second embedding vector.
        
    Returns:
        Cosine similarity score between -1 and 1.
    """
    if vec1 is None or vec2 is None:
        return 0.0
    
    # Ensure vectors are 1D and have the same shape
    vec1 = vec1.flatten()
    vec2 = vec2.flatten()
    
    if vec1.shape != vec2.shape:
        return 0.0
    
    # Calculate dot product
    dot_product = np.dot(vec1, vec2)
    
    # Calculate norms
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    # Avoid division by zero
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    # Cosine similarity = dot product / (norm1 * norm2)
    similarity = dot_product / (norm1 * norm2)
    
    # Clamp to [-1, 1] to handle floating point errors
    return float(np.clip(similarity, -1.0, 1.0))


def cosine_similarity_batch(query_vec: np.ndarray, note_vectors: np.ndarray) -> np.ndarray:
    """Calculate cosine similarity between a query vector and multiple note vectors efficiently.
    
    This uses vectorized operations for much better performance than calculating one-by-one.
    
    Args:
        query_vec: Query embedding vector (1D array, shape: (384,)).
        note_vectors: Array of note embedding vectors (2D array, shape: (n_notes, 384)).
        
    Returns:
        Array of similarity scores (1D array, shape: (n_notes,)).
    """
    if query_vec is None or note_vectors is None or len(note_vectors) == 0:
        return np.array([])
    
    # Ensure query vector is 1D
    query_vec = query_vec.flatten()
    
    # Normalize query vector once
    query_norm = np.linalg.norm(query_vec)
    if query_norm == 0:
        return np.zeros(len(note_vectors))
    query_vec_norm = query_vec / query_norm
    
    # Normalize all note vectors at once (vectorized)
    note_norms = np.linalg.norm(note_vectors, axis=1, keepdims=True)
    # Avoid division by zero
    note_norms = np.where(note_norms == 0, 1, note_norms)
    note_vectors_norm = note_vectors / note_norms
    
    # Calculate dot products for all notes at once (vectorized)
    similarities = np.dot(note_vectors_norm, query_vec_norm)
    
    # Clamp to [-1, 1] to handle floating point errors
    return np.clip(similarities, -1.0, 1.0)

