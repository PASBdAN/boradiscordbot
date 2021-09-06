# import sqlite3
import psycopg2
import urllib.parse as urlparse
import os

class Client():
    def __init__(self, db_name):
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port
        # self.conn = sqlite3.connect(db_name)
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.conn.cursor()

    def commit_db(self):
        if self.conn:
            self.conn.commit()
    
    def close_db(self):
        if self.conn:
            self.conn.close()
            print("Sessão finalizada")

        