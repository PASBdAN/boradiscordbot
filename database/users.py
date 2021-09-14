import sqlite3
from database.client import Client

class Users(Client):
    def __init__(self):
        super().__init__()
        self.tb_name = "users"
        self.schema_file = 'database/schemas/users_schema.sql'
        with open(self.schema_file, 'r') as f:
            schema = f.read()
            # self.cursor.executescript(schema)
            self.cursor.execute(schema)
    
    