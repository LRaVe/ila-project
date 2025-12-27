"""Main CLI application for ILA (Intelligent Local Archive)."""

import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

# Add src directory to path for imports when running directly
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))

from database import add_note, get_all_notes, delete_note
from ai_logic import text_to_vector, vector_to_bytes, bytes_to_vector, cosine_similarity

app = typer.Typer()
console = Console()


@app.command()
def add(
    note: str = typer.Argument(..., help="The note content to save"),
) -> None:
    """Add a new note to the archive.
    
    Args:
        note: The note content to save.
    """
    # Generate embedding for the note
    embedding_vector = text_to_vector(note)
    embedding_bytes = vector_to_bytes(embedding_vector)
    
    add_note(note, embedding_bytes)
    console.print("[green]✓[/green] Note added successfully!")

@app.command()
def delete(
    noteID: str = typer.Argument(..., help="The ID of the note to delete"),
) -> None:
    """Delete the note with the input ID

    Args: 
        noteID : ID of the note we want to delete.
    """
    delete_note(noteID)
    console.print("[green]✓[/green] Note deleted successfully!")



@app.command()
def list_notes() -> None:
    """List all saved notes in a formatted table."""
    notes = get_all_notes()
    
    if not notes:
        console.print(
            "[yellow]No notes found. Use 'add' to create your first note.[/yellow]"
        )
        return
    
    table = Table(title="Saved Notes", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Content", style="white")
    table.add_column("Created At", style="dim", no_wrap=True)
    
    for note in notes:
        table.add_row(note["id"], note["content"], note["created_at"])
    
    console.print(table)


# Alias 'list' command to 'list_notes' since 'list' is a Python builtin
@app.command(name="list")
def list_command() -> None:
    """List all saved notes. Alias for list_notes."""
    list_notes()


@app.command()
def find(
    query: str = typer.Argument(..., help="The search query string"),
) -> None:
    """Find the top 3 most semantically similar notes to the query.
    
    Args:
        query: The search query string.
    """
    # Generate embedding for the query
    query_embedding = text_to_vector(query)
    
    # Get all notes from database
    notes = get_all_notes()
    
    if not notes:
        console.print("[yellow]No notes found. Use 'add' to create your first note.[/yellow]")
        return
    
    # Calculate cosine similarity for each note
    note_similarities = []
    for note in notes:
        if note["embedding"] is None:
            # Skip notes without embeddings (old notes)
            continue
        
        note_embedding = bytes_to_vector(note["embedding"])
        similarity = cosine_similarity(query_embedding, note_embedding)
        note_similarities.append({
            "note": note,
            "similarity": similarity
        })
    
    if not note_similarities:
        console.print("[yellow]No notes with embeddings found. Add some notes first.[/yellow]")
        return
    
    # Sort by similarity (descending) and get top 3
    note_similarities.sort(key=lambda x: x["similarity"], reverse=True)
    top_notes = note_similarities[:3]
    
    # Display results using rich
    table = Table(title=f"Top 3 Most Similar Notes for: '{query}'", show_header=True, header_style="bold magenta")
    table.add_column("Rank", style="cyan", no_wrap=True)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Content", style="white")
    table.add_column("Similarity", style="green", no_wrap=True)
    table.add_column("Created At", style="dim", no_wrap=True)
    
    for idx, item in enumerate(top_notes, 1):
        note = item["note"]
        similarity = item["similarity"]
        table.add_row(
            str(idx),
            note["id"],
            note["content"],
            f"{similarity:.4f}",
            note["created_at"]
        )
    
    console.print(table)


if __name__ == "__main__":
    app()

