from lib.db.connection import get_connection

class Author:
    def __init__(self, name, id = None):
        self.name = name
        self.id = id
    def save(self):
        conn  = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute("UPDATE authors SET name=? WHERE id=?", (self.name, self.id))
        else:
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            self.id = cursor.lastrowid

        conn.commit()
        conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id=?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row['name'], row['id'])
        
        return None
    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id=?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        from lib.models.article import Article
        return [Article(row['title'], row['author_id'], row['magazine_id'], row['id']) for row in rows]
    
    def magazines(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
            """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        from lib.models.magazine import Magazine
        return [Magazine(row['name'], row['category'], row['id']) for row in rows]