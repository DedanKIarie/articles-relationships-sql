from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Magazine name must be a non-empty string")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Magazine category must be a non-empty string")
        self._name = name
        self._category = category
        self.id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Magazine name must be a non-empty string")
        self._name = value
    
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Magazine category must be a non-empty string")
        self._category = value

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self.id:
                cursor.execute("UPDATE magazines SET name=?, category=? WHERE id=?", (self.name, self.category, self.id))
            else:
                cursor.execute("INSERT INTO magazines (name, category) VALUES (?,?)", (self.name, self.category))
                self.id = cursor.lastrowid
            conn.commit()
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM magazines WHERE id=?", (id,))
            row = cursor.fetchone()
            return cls(row['name'], row['category'], row['id']) if row else None
        finally:
            conn.close()

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM magazines WHERE name=?", (name,))
            row = cursor.fetchone()
            return cls(row['name'], row['category'], row['id']) if row else None
        finally:
            conn.close()

    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM magazines WHERE category=?", (category,))
            rows = cursor.fetchall() # Category might not be unique
            return [cls(row['name'], row['category'], row['id']) for row in rows] if rows else []
        finally:
            conn.close()

    def articles(self):
        from lib.models.article import Article 
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM articles WHERE magazine_id=?", (self.id,))
            rows = cursor.fetchall()
            return [Article(row['title'], row['author_id'], row['magazine_id'], row['id']) for row in rows]
        finally:
            conn.close()

    def contributors(self):
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT DISTINCT authors.* FROM authors
                JOIN articles ON authors.id = articles.author_id
                WHERE articles.magazine_id = ?
            """, (self.id,))
            rows = cursor.fetchall()
            return [Author(row['name'], row['id']) for row in rows]
        finally:
            conn.close()

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT title FROM articles WHERE magazine_id=?", (self.id,))
            rows = cursor.fetchall()
            return [row['title'] for row in rows] if rows else []
        finally:
            conn.close()

    def contributing_authors(self):
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT authors.*, COUNT(articles.id) as article_count FROM authors
                JOIN articles ON authors.id = articles.author_id
                WHERE articles.magazine_id = ?
                GROUP BY authors.id
                HAVING article_count > 2
            """, (self.id,))
            rows = cursor.fetchall()
            return [Author(row['name'], row['id']) for row in rows] if rows else []
        finally:
            conn.close()
            
    @classmethod
    def with_multiple_authors(cls, min_authors=2):
        conn = get_connection()
        cursor = conn.cursor()
        magazines_data = []
        try:
            cursor.execute(f"""
                SELECT m.id, m.name, m.category, COUNT(DISTINCT a.author_id) as author_count
                FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                GROUP BY m.id
                HAVING author_count >= ?
            """, (min_authors,))
            rows = cursor.fetchall()
            for row in rows:
                magazines_data.append(cls(row['name'], row['category'], row['id']))
            return magazines_data
        finally:
            conn.close()

    @classmethod
    def article_counts(cls):
        conn = get_connection()
        cursor = conn.cursor()
        counts = {}
        try:
            cursor.execute("""
                SELECT m.name, COUNT(a.id) as num_articles
                FROM magazines m
                LEFT JOIN articles a ON m.id = a.magazine_id
                GROUP BY m.name
            """)
            rows = cursor.fetchall()
            for row in rows:
                counts[row['name']] = row['num_articles']
            return counts
        finally:
            conn.close()
            
    @classmethod
    def top_publisher(cls):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT m.id, m.name, m.category, COUNT(a.id) as article_count
                FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                GROUP BY m.id
                ORDER BY article_count DESC
                LIMIT 1
            """)
            row = cursor.fetchone()
            return cls(row['name'], row['category'], row['id']) if row else None
        finally:
            conn.close()


    def __repr__(self):
        return f"<Magazine {self.name} ({self.category})>"

