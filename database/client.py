# import sqlite3
import psycopg2

from manage import dict_config
DATABASE_URL = dict_config['DATABASE_URL']

class Client():
    def __init__(self):
        # self.conn = sqlite3.connect(db_name)
        self.conn = psycopg2.connect(DATABASE_URL)
        self.cursor = self.conn.cursor()

    def commit_db(self):
        if self.conn:
            self.conn.commit()
    
    def close_db(self):
        if self.conn:
            self.conn.close()
            print("Sessão finalizada")

        