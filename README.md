# Articles Relationships SQL Project

This Python application models relationships between Authors, Articles, and Magazines using SQLite and raw SQL queries. It does not use an ORM like SQLAlchemy.

## Project Structure

```
articles-relationships-sql/
├── lib/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── article.py
│   │   ├── author.py
│   │   └── magazine.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── schema.sql
│   │   └── seed.py
│   ├── __init__.py
│   └── debug.py
├── scripts/
│   ├── __init__.py
│   ├── setup_db.py
│   └── run_queries.py
├── tests/
│   └── __init__.py
├── .gitignore
├── article.db
└── README.md
```

## Prerequisites

- Python 3.7+
- pip

## Setup and Installation

### Clone the Repository

```bash
git clone https://github.com/DedanKIarie/articles-relationships-sql
cd articles-relationships-sql
```

### Create and Activate a Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

### Install Dependencies

```bash
pip install pytest ipdb
```

- **pytest**: For running automated tests.
- **ipdb**: For interactive debugging (lib/debug.py).

### Set Up Database Schema

This creates tables in article.db based on lib/db/schema.sql. Existing tables will be dropped and recreated.

```bash
python scripts/setup_db.py
```

## Usage

### Seed Database

Populates the database with sample data. It ensures the schema is set up first.

```bash
python lib/db/seed.py
```

### Run Queries / Application Logic

scripts/run_queries.py seeds the database and can be used to execute and test your model methods.

```bash
python scripts/run_queries.py
```

### Interactive Debugging

Use lib/debug.py to interact directly with models and the database via ipdb.

```bash
python lib/debug.py
```

Inside ipdb:

```python
from lib.models.author import Author
# author_john = Author.find_by_name("John Doe")
# if author_john: print(author_john.articles())
```

## Running Tests

Execute tests using pytest from the project root directory:

```bash
pytest
```

Tests verify functionality. Ensure the database is set up and seeded, as tests may depend on the schema and initial data.
