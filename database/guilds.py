import sqlite3
from database.client import Client

class Guilds(Client):
    def __init__(self,db_name = "database/bot.db"):
        super().__init__(db_name)
        self.tb_name = "guilds"
        self.schema_file = 'database/schemas/guilds_schema.sql'
        with open(self.schema_file, 'r') as f:
            schema = f.read()
            self.cursor.executescript(schema)

    def get_guild_prefix(self, guild_id):
        self.cursor.execute(f"""
            SELECT prefix FROM {self.tb_name} WHERE guild_id = ?
        """, (guild_id,))
        return self.cursor.fetchone()
    
    def insert_guild_prefix(self, guild_id, prefix):
        self.cursor.execute(f"""
            INSERT INTO {self.tb_name} (guild_id, prefix)
            VALUES(?,?)
        """,(guild_id,prefix,))
        self.commit_db()

    def update_guild_prefix(self, guild_id, prefix):
        self.cursor.execute(f"""
            UPDATE {self.tb_name} SET prefix = ?
            WHERE guild_id = ?
        """,(prefix, guild_id,))
        self.commit_db()
    
    def delete_guild(self, guild_id):
        self.cursor.execute(f"""
            DELETE FROM {self.tb_name} WHERE guild_id = ?
        """, (guild_id,))
        self.commit_db()
    