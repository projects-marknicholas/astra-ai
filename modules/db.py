import sqlite3
import time

class LocalStorageDB:
    def __init__(self, db_name="storage.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)  # ✅ Allow multi-threading
        self.cursor = self.conn.cursor()
        
        # ✅ Ensure the base table exists
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS storage (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                prompt TEXT, 
                image TEXT,
                file_path TEXT,
                response TEXT,
                intent TEXT,  
                timestamp INTEGER
            )
        """)
        self.conn.commit()

    def set_item(self, prompt, response="", image="", file_path="", intent="text"):
        """ Store a prompt-response pair with a timestamp. """
        timestamp = int(time.time())  # Current Unix timestamp
        self.cursor.execute(
            "INSERT INTO storage (prompt, response, image, file_path, intent, timestamp) VALUES (?, ?, ?, ?, ?, ?)", 
            (prompt, response, image, file_path, intent, timestamp)
        )
        self.conn.commit()

    def get_item(self, prompt):
        """ Retrieve a response for a given prompt. """
        # self.cleanup()
        self.cursor.execute("SELECT response, image, file_path, intent FROM storage WHERE prompt=?", (prompt,))
        result = self.cursor.fetchone()
        return {"response": result[0], "image": result[1], "file_path": result[2], "intent": result[3]} if result else None

    def get_all(self):
        """ Retrieve all stored items. """
        # self.cleanup()
        self.cursor.execute("SELECT id, prompt, response, image, file_path, intent, timestamp FROM storage ORDER BY timestamp DESC")
        return [
            {"id": row[0], "prompt": row[1], "response": row[2], "image": row[3], "file_path": row[4], "intent": row[5], "timestamp": row[6]} 
            for row in self.cursor.fetchall()
        ]

    def cleanup(self):
        self.cursor.execute("DELETE FROM storage")
        self.conn.commit()

    def close(self):
        """ Close database connection. """
        self.conn.close()
