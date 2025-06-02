from lib.db.connection import get_connection
from lib.models.article import Article
from lib.models.magazine import Magazine

class Author:
    def __init__(self, name, id=None):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Author name must be a non-empty string")
        self._name = name
        self.id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Author name must be a non-empty string")
        self._name = value

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self.id:
                cursor.execute("UPDATE authors SET name=? WHERE id=?", (self.name, self.id))
            else:
                cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
                self.id = cursor.lastrowid
            conn.commit()
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM authors WHERE id=?", (id,))
            row = cursor.fetchone()
            return cls(row['name'], row['id']) if row else None
        finally:
            conn.close()

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM authors WHERE name=?", (name,))
            row = cursor.fetchone()
            return cls(row['name'], row['id']) if row else None
        finally:
            conn.close()

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM articles WHERE author_id=?", (self.id,))
            rows = cursor.fetchall()
            return [Article(row['title'], row['author_id'], row['magazine_id'], row['id']) for row in rows]
        finally:
            conn.close()

    def magazines(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT DISTINCT magazines.* FROM magazines
                JOIN articles ON magazines.id = articles.magazine_id
                WHERE articles.author_id = ?
            """, (self.id,))
            rows = cursor.fetchall()
            return [Magazine(row['name'], row['category'], row['id']) for row in rows]
        finally:
            conn.close()

    def add_article(self, magazine, title):
        if not isinstance(magazine, Magazine):
            raise TypeError("magazine must be a Magazine instance")
        if not magazine.id:
            raise ValueError("Magazine must be saved before adding an article")
        
        article = Article(title=title, author_id=self.id, magazine_id=magazine.id)
        article.save()
        return article

    def topic_areas(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT DISTINCT magazines.category FROM magazines
                JOIN articles ON magazines.id = articles.magazine_id
                WHERE articles.author_id = ?
            """, (self.id,))
            rows = cursor.fetchall()
            return list(set([row['category'] for row in rows])) if rows else []
        finally:
            conn.close()
    
    @classmethod
    def top_author(cls):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT authors.id, authors.name, COUNT(articles.id) as article_count
                FROM authors
                JOIN articles ON authors.id = articles.author_id
                GROUP BY authors.id
                ORDER BY article_count DESC
                LIMIT 1
            """)
            row = cursor.fetchone()
            return cls(row['name'], row['id']) if row else None
        finally:
            conn.close()

    def __repr__(self):
        return f"<Author {self.name}>"

