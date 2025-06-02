from lib.db.connection import get_connection

class Article:
    def __init__(self, title, author_id, magazine_id, content=None, id=None):
        if not isinstance(title, str) or len(title) == 0:
            raise ValueError("Article title must be a non-empty string")
        self._title = title
        self.content = content 
        self.author_id = author_id
        self.magazine_id = magazine_id
        self.id = id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Article title must be a non-empty string")
        self._title = value

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self.id:
                cursor.execute(
                    "UPDATE articles SET title=?, content=?, author_id=?, magazine_id=? WHERE id=?",
                    (self.title, self.content, self.author_id, self.magazine_id, self.id)
                )
            else:
                cursor.execute(
                    "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                    (self.title, self.content, self.author_id, self.magazine_id)
                )
                self.id = cursor.lastrowid
            conn.commit()
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM articles WHERE id=?", (id,))
            row = cursor.fetchone()
            return cls(row['title'], row['author_id'], row['magazine_id'], row['content'], row['id']) if row else None
        finally:
            conn.close()

    @classmethod
    def find_by_title(cls, title):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM articles WHERE title=?", (title,))
            # Title might not be unique, return first one or all?
            # For now, returning the first match.
            row = cursor.fetchone()
            return cls(row['title'], row['author_id'], row['magazine_id'], row['content'], row['id']) if row else None
        finally:
            conn.close()
            
    @classmethod
    def find_by_author(cls, author_id):
        conn = get_connection()
        cursor = conn.cursor()
        articles = []
        try:
            cursor.execute("SELECT * FROM articles WHERE author_id=?", (author_id,))
            rows = cursor.fetchall()
            for row in rows:
                articles.append(cls(row['title'], row['author_id'], row['magazine_id'], row['content'], row['id']))
            return articles
        finally:
            conn.close()

    @classmethod
    def find_by_magazine(cls, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        articles = []
        try:
            cursor.execute("SELECT * FROM articles WHERE magazine_id=?", (magazine_id,))
            rows = cursor.fetchall()
            for row in rows:
                articles.append(cls(row['title'], row['author_id'], row['magazine_id'], row['content'], row['id']))
            return articles
        finally:
            conn.close()

    # Properties to fetch related Author and Magazine objects
    @property
    def author(self):
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM authors WHERE id=?", (self.author_id,))
            row = cursor.fetchone()
            return Author(row['name'], row['id']) if row else None
        finally:
            conn.close()

    @property
    def magazine(self):
        from lib.models.magazine import Magazine
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM magazines WHERE id=?", (self.magazine_id,))
            row = cursor.fetchone()
            return Magazine(row['name'], row['category'], row['id']) if row else None
        finally:
            conn.close()

    def __repr__(self):
        return f"<Article {self.title}>"
