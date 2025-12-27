"""Storage module for managing notes in JSON file."""

import json
from pathlib import Path
from typing import List, Dict

NOTES_FILE = Path("notes.json")


def _ensure_file_exists() -> None:
    """Create notes.json file if it doesn't exist."""
    if not NOTES_FILE.exists():
        with open(NOTES_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def load_notes() -> List[Dict[str, str]]:
    """Load all notes from notes.json file.
    
    Returns:
        List of note dictionaries with 'id' and 'content' keys.
    """
    _ensure_file_exists()
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_notes(notes: List[Dict[str, str]]) -> None:
    """Save notes to notes.json file.
    
    Args:
        notes: List of note dictionaries to save.
    """
    _ensure_file_exists()
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)


def add_note(content: str) -> None:
    """Add a new note to storage.
    
    Args:
        content: The note content to save.
    """
    notes = load_notes()
    note_id = str(len(notes) + 1)
    new_note = {"id": note_id, "content": content}
    notes.append(new_note)
    save_notes(notes)


def get_all_notes() -> List[Dict[str, str]]:
    """Get all notes from storage.
    
    Returns:
        List of all note dictionaries.
    """
    return load_notes()

