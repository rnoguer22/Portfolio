import sqlite3
from config import SQLITE_FILE_PATH



class Sqlite3_Db:

    def __init__(self):
        self.sqlite_file_path = SQLITE_FILE_PATH

    def init_db(self):
        conn = sqlite3.connect(self.sqlite_file_path)
        # We need a cursor instance to execute queries 
        cursor = conn.cursor()
        # Execute the initial query
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS verified_users (
                cookie TEXT PRIMARY KEY,
                email TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def is_cookie_verified(self, cookie: str) -> bool:
        conn = sqlite3.connect(self.sqlite_file_path)
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM verified_users WHERE cookie = ?", (cookie,))
        result = cursor.fetchone()
        conn.close()
        # Return a bool to just to check if the cookie has been verified
        return result is not None 

    def save_verified_cookie(self, email: str, cookie: str):
        conn = sqlite3.connect(self.sqlite_file_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO verified_users (email, cookie) VALUES (?, ?)", (email, cookie))
        conn.commit()
        print(f"\nSaved email and cookies to the db... ({email}, {cookie})")
        conn.close()
