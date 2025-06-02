import sys
import os

# Get the absolute path of the directory containing this script (articles-relationships-sql/lib/db)
_current_script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the absolute path of the project root (articles-relationships-sql)
# This goes up two levels: db -> lib -> project_root
_project_root = os.path.dirname(os.path.dirname(_current_script_dir))


# Add the project root to sys.path if it's not already there
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# Now, imports from 'lib' and 'scripts' should work
from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
# This import will work because _project_root (which contains the 'scripts' directory) is in sys.path
from scripts.setup_db import setup_database

def seed_database():
    # Ensure tables are created by calling setup_database
    # setup_database is now imported from scripts.setup_db
    print("Running setup_database from seed_database...")
    setup_database() 

    conn = None # Initialize conn to None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Clear existing data
        cursor.execute("DELETE FROM articles")
        cursor.execute("DELETE FROM authors")
        cursor.execute("DELETE FROM magazines")
        conn.commit()

        # Authors
        author1 = Author(name="John Doe")
        author1.save()
        author2 = Author(name="Jane Smith")
        author2.save()
        author3 = Author(name="Alice Brown")
        author3.save()

        # Magazines
        magazine1 = Magazine(name="Tech Today", category="Technology")
        magazine1.save()
        magazine2 = Magazine(name="Health Weekly", category="Health")
        magazine2.save()
        magazine3 = Magazine(name="Science Journal", category="Science")
        magazine3.save()
        magazine4 = Magazine(name="Gourmet Guide", category="Food")
        magazine4.save()


        # Articles
        Article(title="The Future of AI", author_id=author1.id, magazine_id=magazine1.id, content="Content about AI...").save()
        Article(title="Understanding Quantum Computing", author_id=author1.id, magazine_id=magazine1.id, content="Content about Quantum...").save()
        Article(title="Healthy Eating Habits", author_id=author2.id, magazine_id=magazine2.id, content="Content about Healthy Eating...").save()
        Article(title="The Benefits of Yoga", author_id=author2.id, magazine_id=magazine2.id, content="Content about Yoga...").save()
        Article(title="Breakthroughs in Cancer Research", author_id=author3.id, magazine_id=magazine3.id, content="Content about Cancer Research...").save()
        Article(title="Exploring the Cosmos", author_id=author1.id, magazine_id=magazine3.id, content="Content about Cosmos...").save()
        Article(title="Another Tech Article by John", author_id=author1.id, magazine_id=magazine1.id, content="More tech content...").save()
        Article(title="Jane on Tech", author_id=author2.id, magazine_id=magazine1.id, content="Jane's tech perspective...").save()

        print("Database seeded successfully.")

    except Exception as e:
        print(f"An error occurred during seeding: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    seed_database()
