"""File ingestion module for processing and storing file contents as notes."""

from pathlib import Path
from typing import List

from database import add_note
from ai_logic import text_to_vector, vector_to_bytes


def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    """Split text into chunks of roughly the specified size without cutting words.
    
    Args:
        text: The text to chunk.
        chunk_size: Target size for each chunk in characters (default: 500).
        
    Returns:
        List of text chunks.
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    words = text.split()
    current_chunk = []
    current_length = 0
    
    for word in words:
        word_length = len(word) + 1  # +1 for the space
        
        # If adding this word would exceed chunk_size, save current chunk and start new one
        if current_length + word_length > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += word_length
    
    # Add the last chunk if it has content
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks


def ingest_file(file_path: str) -> int:
    """Ingest a file by reading it, chunking it, and saving each chunk as a note.
    
    Args:
        file_path: Path to the file to ingest.
        
    Returns:
        Number of chunks created.
        
    Raises:
        FileNotFoundError: If the file doesn't exist.
        IOError: If there's an error reading the file.
    """
    path = Path(file_path)
    
    # Check if file exists
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    
    # Read the file content
    try:
        text = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        try:
            text = path.read_text(encoding='latin-1')
        except Exception as e:
            raise IOError(f"Error reading file: {e}")
    except Exception as e:
        raise IOError(f"Error reading file: {e}")
    
    # Get the file name for source_file column
    file_name = path.name
    
    # Split text into chunks
    chunks = chunk_text(text, chunk_size=500)
    
    # Process each chunk
    for chunk in chunks:
        # Generate embedding for the chunk
        embedding_vector = text_to_vector(chunk)
        embedding_bytes = vector_to_bytes(embedding_vector)
        
        # Save to database with source_file
        add_note(chunk, embedding_bytes, source_file=file_name)
    
    return len(chunks)

