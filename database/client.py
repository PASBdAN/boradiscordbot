# import sqlite3
import psycopg2
import os
# from config.config import DATABASE_URL

class Client():
    def __init__(self):
        # self.conn = sqlite3.connect(db_name)
        self.conn = psycopg2.connect(os.environ['DATABASE_URL'])
        # self.conn = psycopg2.connect(DATABASE_URL)
        self.cursor = self.conn.cursor()

    def commit_db(self):
        if self.conn:
            self.conn.commit()
    
    def close_db(self):
        if self.conn:
            self.conn.close()
            print("Sessão finalizada")

        