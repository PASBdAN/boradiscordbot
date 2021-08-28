import sqlite3
from database.client import Client

class UsersDB(Client):
    def __init__(self,db_name = "bot.db"):
        super().__init__(db_name)
        self.tb_name = "users"
        self.schema_file = 'database/schemas/users_schema.sql'
        with open(self.schema_file, 'r') as f:
            schema = f.read()
            self.cursor.executescript(schema)
    
    