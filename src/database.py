"""Database module for managing notes in SQLite database."""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

DB_FILE = Path("ila.db")


def get_connection() -> sqlite3.Connection:
    """Create and return a database connection.
    
    Returns:
        SQLite database connection.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn


def initialize_database() -> None:
    """Initialize the database and create notes table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create notes table with parameterized query (though DDL is safe)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()


def add_note(content: str) -> None:
    """Add a new note to the database.
    
    Args:
        content: The note content to save.
    """
    initialize_database()
    conn = get_connection()
    cursor = conn.cursor()
    
    # Use parameterized query to prevent SQL injection
    cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))
    
    conn.commit()
    conn.close()


def get_all_notes() -> List[Dict[str, str]]:
    """Get all notes from the database.
    
    Returns:
        List of note dictionaries with 'id', 'content', and 'created_at' keys.
    """
    initialize_database()
    conn = get_connection()
    cursor = conn.cursor()
    
    # Use parameterized query (though SELECT without user input is safe)
    cursor.execute("SELECT id, content, created_at FROM notes ORDER BY id ASC")
    
    rows = cursor.fetchall()
    notes = [
        {
            "id": str(row["id"]),
            "content": row["content"],
            "created_at": row["created_at"]
        }
        for row in rows
    ]
    
    conn.close()
    return notes


def get_note_by_id(note_id: int) -> Optional[Dict[str, str]]:
    """Get a note by its ID.
    
    Args:
        note_id: The ID of the note to retrieve.
        
    Returns:
        Note dictionary if found, None otherwise.
    """
    initialize_database()
    conn = get_connection()
    cursor = conn.cursor()
    
    # Use parameterized query to prevent SQL injection
    cursor.execute("SELECT id, content, created_at FROM notes WHERE id = ?", (note_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "id": str(row["id"]),
            "content": row["content"],
            "created_at": row["created_at"]
        }
    return None

