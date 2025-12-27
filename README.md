# 🧠 ILA - Intelligent Local Archive

<div align="center">

**A powerful, AI-powered note-taking and semantic search system that helps you find information by meaning, not just keywords.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## ✨ Features

### 🎯 **Semantic Search**
- Find notes by **meaning**, not just keywords
- Uses state-of-the-art sentence transformers (`all-MiniLM-L6-v2`) for intelligent search
- Cosine similarity-based ranking for accurate results
- Returns top 3 most semantically similar notes

### 📝 **Note Management**
- Add, delete, and list notes with a beautiful CLI interface
- Automatic embedding generation for every note
- Rich, formatted output using the `rich` library

### 📄 **File Ingestion**
- Ingest entire files and automatically chunk them
- Smart text chunking (~500 characters) that preserves word boundaries
- Track source files for each note chunk

### 🔒 **Local & Private**
- Everything runs locally on your machine
- No data sent to external servers
- SQLite database for reliable, portable storage

### 🚀 **Fast & Efficient**
- Optimized embedding generation with model caching
- Efficient vector storage and retrieval
- Fast semantic search across thousands of notes

---

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ila-project.git
cd ila-project
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** The first time you run ILA, it will automatically download the `all-MiniLM-L6-v2` model (~80MB). This is a one-time download.

---

## 📖 Usage

### Basic Commands

#### Add a Note

```bash
python src/main.py add "Your note content here"
```

**Example:**
```bash
python src/main.py add "Python is a versatile programming language used for web development, data science, and automation."
```

#### List All Notes

```bash
python src/main.py list
# or
python src/main.py list_notes
```

#### Delete a Note

```bash
python src/main.py delete <note_id>
```

**Example:**
```bash
python src/main.py delete 5
```

### 🔍 Semantic Search

The `find` command uses AI-powered semantic search to find notes by meaning:

```bash
python src/main.py find "your search query"
```

**Example:**
```bash
python src/main.py find "programming languages"
```

This will find notes about programming languages even if they don't contain those exact words! The search uses cosine similarity to rank results by semantic similarity.

### 📄 File Ingestion

Ingest entire files into your archive:

```bash
python src/main.py ingest <file_path>
```

**Example:**
```bash
python src/main.py ingest document.txt
```

The file will be automatically:
- Read and split into chunks of ~500 characters
- Each chunk will be saved as a separate note with embeddings
- Source file information will be tracked

---

## 🏗️ Architecture

### Project Structure

```
ila-project/
├── src/
│   ├── main.py          # CLI application with Typer
│   ├── database.py      # SQLite database operations
│   ├── ai_logic.py      # Embedding generation and similarity
│   ├── ingestor.py      # File ingestion and chunking
│   └── storage.py       # Legacy JSON storage (optional)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Key Components

#### `database.py`
- Manages SQLite database connections
- Handles note CRUD operations
- Stores embeddings as BLOB data
- Tracks source files for ingested documents

#### `ai_logic.py`
- Uses `sentence-transformers` library
- Model: `all-MiniLM-L6-v2` (384-dimensional embeddings)
- Converts text to vectors with normalization
- Calculates cosine similarity between vectors

#### `ingestor.py`
- Reads files using `pathlib`
- Smart chunking algorithm (preserves word boundaries)
- Generates embeddings for each chunk
- Saves chunks to database with source tracking

#### `main.py`
- CLI interface using `typer`
- Beautiful output formatting with `rich`
- Commands: `add`, `delete`, `list`, `find`, `ingest`

---

## 🔬 How It Works

### Semantic Search Process

1. **Query Processing**: Your search query is converted into a 384-dimensional embedding vector
2. **Vector Retrieval**: All note embeddings are loaded from the database
3. **Similarity Calculation**: Cosine similarity is calculated between the query vector and each note vector
4. **Ranking**: Notes are sorted by similarity score (highest first)
5. **Results**: Top 3 most similar notes are displayed

### Embedding Generation

- Uses the `all-MiniLM-L6-v2` model from sentence-transformers
- Produces 384-dimensional normalized vectors
- Stored as binary BLOB in SQLite for efficiency
- Automatically generated when notes are added or files are ingested

### Cosine Similarity

The similarity between two vectors is calculated as:

```
similarity = (A · B) / (||A|| × ||B||)
```

Where:
- `A · B` is the dot product
- `||A||` and `||B||` are the vector norms

This gives a score between -1 (opposite) and 1 (identical), with higher scores indicating more semantic similarity.

---

## 🛡️ Security

- **SQL Injection Protection**: All database queries use parameterized statements
- **Local Processing**: All AI processing happens locally - no data leaves your machine
- **No External APIs**: No API keys or external services required

---

## 📦 Dependencies

- **typer** - Modern CLI framework
- **rich** - Beautiful terminal output
- **sentence-transformers** - AI embedding generation
- **numpy** - Numerical operations for vector math

---

## 🚧 Future Enhancements

Potential features for future versions:

- [ ] Batch note import
- [ ] Export notes to various formats
- [ ] Advanced filtering options
- [ ] Web interface
- [ ] Multi-database support
- [ ] Custom embedding models
- [ ] Note tagging and categorization

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- [sentence-transformers](https://www.sbert.net/) for the embedding model
- [Typer](https://typer.tiangolo.com/) for the CLI framework
- [Rich](https://rich.readthedocs.io/) for beautiful terminal output

---

## 📧 Contact

For questions, issues, or suggestions, please open an issue on GitHub.

---

<div align="center">

**Made with ❤️ for intelligent note-taking**

⭐ Star this repo if you find it useful!

</div>

