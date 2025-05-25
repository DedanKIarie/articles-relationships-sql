from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name, category , id= None):
        self.name = name
        self.category = category
        self.id = id

    def save(self):
        conn  = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute("UPDATE magazines SET name=? WHERE id=?", (self.name, self.id))
        else:
            cursor.execute("INSERT INTO magazines (name, category) VALUES (?,?)", (self.name, self.category))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id=?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row['name'],row['category'], row['id'])
        return None
        
    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id=?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        from lib.models.article import Article
        return [Article(row['title'], row['author_id'], row['magazine_id'], row['id']) for row in rows]

    def contributoes(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        from lib.models.author import Author
        return [Author(row['name'], row['id']) for row in rows]