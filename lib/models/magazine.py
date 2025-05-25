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
        