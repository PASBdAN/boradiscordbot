# import sqlite3
from database.client import Client
from psycopg2 import sql

class Guilds(Client):
    def __init__(self):
        super().__init__()
        self.tb_name = "guilds"
        self.schema_file = 'database/schemas/guilds_schema.sql'
        with open(self.schema_file, 'r') as f:
            schema = f.read()
            # self.cursor.executescript(schema)
            self.cursor.execute(schema)
    
    def get_guild_value(self, guild_id, column):
        # self.cursor.execute(f"""
        #     SELECT {column} FROM {self.tb_name} WHERE guild_id = ?
        # """, (guild_id,))
        self.cursor.execute(
            sql.SQL("SELECT {field} FROM {table} WHERE {pkey} = %s").format(
                field=sql.Identifier(column),
                table=sql.Identifier(self.tb_name),
                pkey=sql.Identifier('guild_id')
                ), (guild_id,)
            )
        return self.cursor.fetchone()
    
    def insert_guild_value(self, guild_id, value, column):
        # self.cursor.execute(f"""
        #     INSERT INTO {self.tb_name} (guild_id, {column})
        #     VALUES(?,?)
        # """,(guild_id,value,))
        self.cursor.execute(
            sql.SQL("INSERT INTO {table} ({fields}) VALUES (%s, %s)").format(
                table=sql.Identifier(self.tb_name),
                fields=sql.SQL(', ').join(map(sql.Identifier,['guild_id',column]))
            ),(guild_id,column,)
        )
        # placeholders=sql.SQL(', ').join(sql.Placeholder()*2))
        self.commit_db()

    def update_guild_value(self, guild_id, value, column):
        # self.cursor.execute(f"""
        #     UPDATE {self.tb_name} SET {column} = ?
        #     WHERE guild_id = ?
        # """,(value, guild_id,))
        self.cursor.execute(
            sql.SQL("UPDATE {table} SET {field} = %s WHERE {pkey} = %s").format(
                table=sql.Identifier(self.tb_name),
                field=sql.Identifier(column),
                pkay=sql.Identifier('guild_id'),
            ), (value,guild_id,)
        )
        self.commit_db()

    def delete_guild(self, guild_id):
        # self.cursor.execute(f"""
        #     DELETE FROM {self.tb_name} WHERE guild_id = ?
        # """, (guild_id,))
        self.cursor.execute(
            sql.SQL("DELETE FROM {table} WHERE {pkey} = %s").format(
                table=sql.Identifier(self.tb_name),
                pkey=sql.Identifier('guild_id'),
            ), (guild_id,)
        )
        self.commit_db()
    