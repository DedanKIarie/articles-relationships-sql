import sys
import os

_current_script_dir = os.path.dirname(os.path.abspath(__file__))

_project_root = os.path.dirname(_current_script_dir)


if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from lib.db.connection import get_connection

def setup_database():
    conn = get_connection()
    try:
        schema_sql_path = os.path.join(_project_root, "lib", "db", "schema.sql")
        
        with open(schema_sql_path) as f:
            conn.executescript(f.read())
        conn.commit()
    except Exception as e:
        print(f"Error setting up database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    setup_database()
    print("Database setup completed.")
