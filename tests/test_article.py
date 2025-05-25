import sys
import os
from lib.db.connection import get_connection
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestArticle:
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
        cls.cursor.execute("INSERT INTO authors (name) VALUES ('Test Author')")
        cls.cursor.execute("INSERT INTO magazines (name, category) VALUES ('Test Mag', 'Testing')")
        cls.conn.commit()
    
    def test_article_save(self):
        try:
            article = Article("Test Article", 1, 1)
            article.save()
            assert article.id is not None
            print("✅ test_article_save passed")
        except Exception as e:
            print(f"❌ test_article_save failed: {str(e)}")
    
    def test_find_by_id(self):
        try:
            self.cursor.execute("""
                INSERT INTO articles (title, author_id, magazine_id)
                VALUES ('Find Me', 1, 1)
            """)
            article_id = self.cursor.lastrowid
            self.conn.commit()
            
            article = Article.find_by_id(article_id)
            assert article is not None
            assert article.title == "Find Me"
            print("✅ test_find_by_id passed")
        except Exception as e:
            print(f"❌ test_find_by_id failed: {str(e)}")
    
    def test_article_relationships(self):
        try:
            article = Article("Relationship Test", 1, 1)
            article.save()
            assert article.author_id == 1
            assert article.magazine_id == 1
            print("✅ test_article_relationships passed")
        except Exception as e:
            print(f"❌ test_article_relationships failed: {str(e)}")

if __name__ == "__main__":
    print("\nRunning Article Tests...")
    tester = TestArticle()
    tester.setup_class()
    
    tester.test_article_save()
    tester.test_find_by_id()
    tester.test_article_relationships()
    
    tester.teardown_class()
    print("\nArticle tests completed")

