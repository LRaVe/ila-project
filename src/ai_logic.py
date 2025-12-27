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
    embedding = model.encode(text, convert_to_numpy=True)
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
        Numpy array representing the embedding vector.
    """
    if data is None:
        return None
    # The model 'all-MiniLM-L6-v2' produces 384-dimensional vectors
    return np.frombuffer(data, dtype=np.float32)


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
    
    # Normalize vectors
    vec1_norm = vec1 / (np.linalg.norm(vec1) + 1e-8)
    vec2_norm = vec2 / (np.linalg.norm(vec2) + 1e-8)
    
    # Calculate cosine similarity
    return float(np.dot(vec1_norm, vec2_norm))

