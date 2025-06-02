import sys
import os

_current_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_current_script_dir)

if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.seed import seed_database

def run_example_queries():
    print("Running example queries...")
    pass

if __name__ == "__main__":
    print("Attempting to seed database...")
    try:
        seed_database() 
        print("Seeding complete.")
    except Exception as e:
        print(f"Error during seeding in run_queries: {e}")
        print("Please ensure your database schema is set up correctly (run scripts/setup_db.py).")
        print("And that the seed.py script can run without issues.")
    print("-" * 30)
    run_example_queries()
    print("-" * 30)
    print("Example queries execution finished (if any were added).")
