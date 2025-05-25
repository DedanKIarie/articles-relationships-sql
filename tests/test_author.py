import sys
import os
from lib.db.connection import get_connection
from lib.models.author import Author

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestAuthor:
    @classmethod
    def setup_class(cls):
        cls.conn = get_connection()
        cls.cursor = cls.conn.cursor()
        cls.setup_test_data()
    
    @classmethod
    def teardown_class(cls):
        cls.cursor.execute("DELETE FROM articles")
        cls.cursor.execute("DELETE FROM authors")
        cls.conn.commit()
        cls.conn.close()
    
    @classmethod
    def setup_test_data(cls):
        cls.cursor.execute("DELETE FROM articles")
        cls.cursor.execute("DELETE FROM authors")
        cls.cursor.execute("INSERT INTO authors (name) VALUES ('Test Author 1')")
        cls.cursor.execute("INSERT INTO authors (name) VALUES ('Test Author 2')")
        cls.conn.commit()
    
    def test_author_save(self):
        try:
            author = Author("New Test Author")
            author.save()
            assert author.id is not None
            print("✅ test_author_save passed")
        except Exception as e:
            print(f"❌ test_author_save failed: {str(e)}")
    
    def test_find_by_id(self):
        try:
            self.cursor.execute("INSERT INTO authors (name) VALUES ('Find Me')")
            self.conn.commit()
            last_id = self.cursor.lastrowid
            
            author = Author.find_by_id(last_id)
            assert author is not None
            assert author.name == "Find Me"
            print("✅ test_find_by_id passed")
        except Exception as e:
            print(f"❌ test_find_by_id failed: {str(e)}")
    
    def test_author_articles(self):
        try:
            self.cursor.execute("INSERT INTO magazines (name, category) VALUES ('Test Mag', 'Testing')")
            self.cursor.execute("""
                INSERT INTO articles (title, author_id, magazine_id)
                VALUES ('Test Article', 1, 1)
            """)
            self.conn.commit()
            
            author = Author.find_by_id(1)
            articles = author.articles()
            assert len(articles) > 0
            assert articles[0].title == "Test Article"
            print("✅ test_author_articles passed")
        except Exception as e:
            print(f"❌ test_author_articles failed: {str(e)}")

if __name__ == "__main__":
    print("\nRunning Author Tests...")
    tester = TestAuthor()
    tester.setup_class()
    
    tester.test_author_save()
    tester.test_find_by_id()
    tester.test_author_articles()
    
    tester.teardown_class()
    print("\nAuthor tests completed")
