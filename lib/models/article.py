from lib.db.connection import get_connection

class Article:
    def __init__(self, title ,author_id, magazine_id, id=None):
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id
        self.id = id

    def save(self):
        conn  = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute("UPDATE articles SET title=?, author_id=?, magazine_id=? WHERE id=?", (self.title, self.author_id, self.magazine_id, self.id))
        else:
            cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", (self.title, self.author_id, self.magazine_id))
            self.id = cursor.lastrowid

        conn.commit()
        conn.close()
    
    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id=?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row['title'],row['author_id'],row['magazine_id'], row['id'])
        return None