import sqlite3
from database.helper import Client

class UsersDB(Client):
    def __init__(self,db_name):
        super().__init__(db_name)
        self.tb_name = "guilds"
        self.schema_file = 'database/schemas/guilds_schema.sql'
        with open(schema_file, 'r') as f:
            schema = f.read()
            self.db.cursor.executescript(schema)
    
    