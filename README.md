# Articles Relationships Project

A simple Python app using SQLite to manage relationships between Authors, Articles, and Magazines—**without using SQLAlchemy**.

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/DedanKIarie/articles-relationships-sql
   cd articles-relationships-sql
2. **setup the database**
    ```bash
    python scripts/setup_db.py
3. **Run Tests**
    ```bash
    python -m tests.test_author
    python -m tests.test_article
    python -m tests.test_magazine

# Requirements
1. Python 3.x

2. SQLite (included with Python)