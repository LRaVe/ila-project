"""File ingestion module for processing and storing file contents as notes."""

import mimetypes
import sqlite3
from pathlib import Path
from typing import List

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

from database import add_note
from ai_logic import text_to_vector, vector_to_bytes

console = Console()


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
        ValueError: If the path is not a file or file type is not supported.
        IOError: If there's an error reading the file.
        sqlite3.Error: If there's an error saving to the database.
    """
    path = Path(file_path)
    
    # Check if file exists
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    
    # Check file type using mimetypes
    mime_type, _ = mimetypes.guess_type(str(path))
    
    # Allowed text-based MIME types
    allowed_types = [
        'text/plain',
        'text/html',
        'text/css',
        'text/javascript',
        'text/xml',
        'application/javascript',
        'application/json',
        'application/xml',
        'application/x-sh',
        'application/x-python',
    ]
    
    # Check if file type is text-based
    if mime_type is None:
        # If mimetype can't be determined, check common text extensions
        text_extensions = {'.txt', '.md', '.py', '.js', '.html', '.css', '.json', 
                          '.xml', '.sh', '.bat', '.ps1', '.yml', '.yaml', '.csv'}
        if path.suffix.lower() not in text_extensions:
            console.print(f"[red]✗[/red] Error: Cannot determine file type for '{file_path}'. "
                         f"Please ensure it's a text-based file.")
            raise ValueError(f"Unsupported file type: {file_path}")
    elif mime_type not in allowed_types:
        console.print(f"[red]✗[/red] Error: File type '{mime_type}' is not supported. "
                     f"Only text-based files are allowed.")
        raise ValueError(f"Unsupported file type '{mime_type}' for file: {file_path}")
    
    # Read the file content with proper error handling
    try:
        text = path.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        # If UTF-8 fails, it might be a binary file with misleading extension
        console.print(f"[red]✗[/red] Error: Failed to decode file as UTF-8. "
                     f"This might be a binary file with a misleading extension.")
        raise IOError(f"Cannot decode file as text (possibly binary): {file_path}") from e
    except Exception as e:
        console.print(f"[red]✗[/red] Error reading file: {e}")
        raise IOError(f"Error reading file: {e}") from e
    
    # Get the file name for source_file column
    file_name = path.name
    
    # Split text into chunks
    chunks = chunk_text(text, chunk_size=500)
    
    if not chunks:
        console.print("[yellow]⚠[/yellow] Warning: File appears to be empty.")
        return 0
    
    # Process chunks with progress bar
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task = progress.add_task(
            f"[cyan]Processing {len(chunks)} chunk(s) from '{file_name}'...",
            total=len(chunks)
        )
        
        successful_chunks = 0
        for chunk in chunks:
            try:
                # Generate embedding for the chunk
                embedding_vector = text_to_vector(chunk)
                embedding_bytes = vector_to_bytes(embedding_vector)
                
                # Save to database with source_file
                try:
                    add_note(chunk, embedding_bytes, source_file=file_name)
                    successful_chunks += 1
                except sqlite3.Error as db_error:
                    console.print(f"\n[red]✗[/red] Database error while saving chunk: {db_error}")
                    raise
                except Exception as e:
                    console.print(f"\n[red]✗[/red] Unexpected error while saving chunk: {e}")
                    raise sqlite3.Error(f"Error saving to database: {e}") from e
                
                progress.update(task, advance=1)
                
            except Exception as e:
                console.print(f"\n[red]✗[/red] Error processing chunk: {e}")
                raise
    
    return successful_chunks

