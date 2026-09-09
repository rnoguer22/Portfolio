import sqlite3
import os 
from config import DB_PATH, SQLITE_FILE_PATH



class Sqlite3_Db:

    def __init__(self):
        os.makedirs(DB_PATH, exist_ok=True)
        self.sqlite_file_path = SQLITE_FILE_PATH
        self.users_table = "users"
        self.devices_table = "devices"
        self.messages_table = "messages"

    def init_db(self):
        conn = sqlite3.connect(self.sqlite_file_path)
        # We need a cursor instance to execute queries 
        cursor = conn.cursor()
        # Execute the initial query
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.users_table} (
                email TEXT PRIMARY KEY,
                requests_left INTEGER DEFAULT 10
            )
        """)
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.devices_table} (
                cookie TEXT PRIMARY KEY,
                email TEXT NOT NULL,
                FOREIGN KEY (email) REFERENCES {self.users_table}(email) ON DELETE CASCADE
            )
        """)
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.messages_table} (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               email TEXT NOT NULL, 
               sender TEXT,
               text TEXT,
               file_name TEXT,
               timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
               FOREIGN KEY (email) REFERENCES {self.users_table}(email) ON DELETE CASCADE 
            )
        """)
        conn.commit()
        conn.close()


    # Get the email based on the cookie 
    def get_email(self, cookie: str) -> str:
        conn = sqlite3.connect(self.sqlite_file_path)
        cursor = conn.cursor()
        cursor.execute(f"""SELECT email FROM {self.devices_table} WHERE cookie = ?""", (cookie,))
        result = cursor.fetchone()
        conn.close()
        # fetchone returns a tuple if the value is found, or None if not, so we need to check that
        if result is None:
            return None
        return result[0]

    def is_cookie_verified(self, cookie: str) -> bool:
        # Return a bool to just to check if the cookie has been verified
        return self.get_email(cookie) is not None

    def save_verified_cookie(self, email: str, cookie: str):
        conn = sqlite3.connect(self.sqlite_file_path)
        cursor = conn.cursor()
        # We make sure the user exists
        cursor.execute(f"INSERT INTO {self.users_table} (email, requests_left) VALUES (?, 10) ON CONFLICT(email) DO NOTHING", (email,))
        # Linkthat specific cookie to the email, allowing multiple devices 
        cursor.execute(f"INSERT OR REPLACE INTO {self.devices_table} (cookie, email) VALUES (?, ?)", (cookie, email))
        conn.commit()
        print(f"\nSaved email and cookies to the db... ({email}, {cookie})")
        conn.close()

    # Add the user prompt or the agent response to the messages table 
    def add_message(self, cookie: str, sender: str, text: str, file_name: str = None):
        email = self.get_email(cookie)
        if not email:
            return 

        conn = sqlite3.connect(self.sqlite_file_path)
        cursor = conn.cursor()
        cursor.execute(f"""
           INSERT INTO {self.messages_table} (email, sender, text, file_name)
           VALUES (?, ?, ?, ?)
        """, (email, sender, text, file_name))
        conn.commit()
        conn.close()
    
    # Mehotd to get all the messages from a user
    def get_messages(self, cookie: str):
        email = self.get_email(cookie)
        if not email:
            return 

        conn = sqlite3.connect(self.sqlite_file_path)
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT sender, text, file_name, timestamp 
            FROM {self.messages_table}
            WHERE email = ?
            ORDER BY timestamp ASC
        """, (email,))
        rows = cursor.fetchall()
        conn.close()

        # Return the results in the expected frontend format 
        return [
            {"sender": row[0], "text": row[1], "file_name": row[2], "timestamp": row[3]}
            for row in rows
        ]

    # Method to get the number of queries the user can make to the tool
    def get_requests_left(self, cookie: str) -> int:
        email = self.get_email(cookie)
        if not email:
            return 

        conn = sqlite3.connect(self.sqlite_file_path)
        cursor = conn.cursor()
        cursor.execute(f"""SELECT requests_left FROM {self.users_table} WHERE email = ?""", (email,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[0]
        else: 
            return 0

    # Method to decrements the available prompts the user can make to the tool 
    def decrement_requests(self, cookie: str) -> bool:
        email = self.get_email(cookie)
        if not email:
            return 

        conn = sqlite3.connect(self.sqlite_file_path)
        cursor = conn.cursor()
        cursor.execute(f"""
            UPDATE {self.users_table}
            SET requests_left = requests_left - 1
            WHERE email = ? AND requests_left > 0
        """, (email,))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
