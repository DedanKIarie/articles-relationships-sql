import sys
import os
from lib.db.connection import get_connection
from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.models.article import Article

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestMagazine:
    @classmethod
    def setup_class(cls):
        cls.conn = get_connection()
        cls.cursor = cls.conn.cursor()
        cls.setup_test_data()
    
    @classmethod
    def teardown_class(cls):
        cls.cursor.execute("DELETE FROM articles")
        cls.cursor.execute("DELETE FROM authors")
        cls.cursor.execute("DELETE FROM magazines")
        cls.conn.commit()
        cls.conn.close()
    
    @classmethod
    def setup_test_data(cls):
        cls.cursor.execute("DELETE FROM articles")
        cls.cursor.execute("DELETE FROM authors")
        cls.cursor.execute("DELETE FROM magazines")
        cls.conn.commit()
        
        cls.cursor.execute("INSERT INTO authors (name) VALUES ('Test Author 1')")
        cls.cursor.execute("INSERT INTO authors (name) VALUES ('Test Author 2')")
        cls.cursor.execute("""
            INSERT INTO magazines (id, name, category) 
            VALUES (1, 'Tech Magazine', 'Technology')
        """)
        cls.cursor.execute("""
            INSERT INTO articles (title, author_id, magazine_id)
            VALUES ('Tech Article 1', 1, 1)
        """)
        cls.cursor.execute("""
            INSERT INTO articles (title, author_id, magazine_id)
            VALUES ('Tech Article 2', 2, 1)
        """)
        cls.conn.commit()
    
    def test_magazine_save(self):
        try:
            magazine = Magazine("New Magazine", "General")
            magazine.save()
            assert magazine.id is not None
            print("✅ test_magazine_save passed")
        except Exception as e:
            print(f"❌ test_magazine_save failed: {str(e)}")
    
    def test_find_by_id(self):
        try:
            magazine = Magazine.find_by_id(1)
            assert magazine is not None
            assert magazine.name == "Tech Magazine"
            print("✅ test_find_by_id passed")
        except Exception as e:
            print(f"❌ test_find_by_id failed: {str(e)}")
    
    def test_magazine_articles(self):
        try:
            magazine = Magazine.find_by_id(1)
            articles = magazine.articles()
            assert len(articles) == 2
            print("✅ test_magazine_articles passed")
        except Exception as e:
            print(f"❌ test_magazine_articles failed: {str(e)}")
    
    def test_magazine_contributors(self):
        try:
            magazine = Magazine.find_by_id(1)
            contributors = magazine.contributors()
            assert len(contributors) == 2
            print("✅ test_magazine_contributors passed")
        except Exception as e:
            print(f"❌ test_magazine_contributors failed: {str(e)}")

if __name__ == "__main__":
    print("\nRunning Magazine Tests...")
    tester = TestMagazine()
    tester.setup_class()
    tester.test_magazine_save()
    tester.test_find_by_id()
    tester.test_magazine_articles()
    tester.test_magazine_contributors()
    tester.teardown_class()
    print("\nMagazine tests completed")
