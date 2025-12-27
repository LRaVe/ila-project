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
    add_note(note)
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


if __name__ == "__main__":
    app()

