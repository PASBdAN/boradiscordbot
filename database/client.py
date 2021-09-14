# import sqlite3
import psycopg2
import os

class Client():
    def __init__(self):
        # self.conn = sqlite3.connect(db_name)
        self.conn = psycopg2.connect(os.environ['DATABASE_URL'])
        # self.conn = psycopg2.connect("postgres://iahdcmqnelbrfy:6f9a9833e0922ea8b9729e5701a706664c6b1308df8207257e16ff502059da90@ec2-54-83-137-206.compute-1.amazonaws.com:5432/dbful1aoklvin4")
        self.cursor = self.conn.cursor()

    def commit_db(self):
        if self.conn:
            self.conn.commit()
    
    def close_db(self):
        if self.conn:
            self.conn.close()
            print("Sessão finalizada")

        