from database.client import Client
from psycopg2 import sql

class Users(Client):
    def __init__(self):
        super().__init__()
        self.tb_name = "users"
        self.schema_file = 'database/schemas/users_schema.sql'
        with open(self.schema_file, 'r') as f:
            schema = f.read()
            # self.cursor.executescript(schema)
            self.cursor.execute(schema)
    
    def get_user_value(self, user_id, column):
        # self.cursor.execute(f"""
        #     SELECT {column} FROM {self.tb_name} WHERE user_id = ?
        # """, (user_id,))
        self.cursor.execute(
            sql.SQL("SELECT {field} FROM {table} WHERE {pkey} = %s").format(
                field=sql.Identifier(column),
                table=sql.Identifier(self.tb_name),
                pkey=sql.Identifier('id')
                ), (user_id,)
            )
        return self.cursor.fetchone()
    
    def insert_user_value(self, user_id, value, column):
        # self.cursor.execute(f"""
        #     INSERT INTO {self.tb_name} (user_id, {column})
        #     VALUES(?,?)
        # """,(user_id,value,))
        self.cursor.execute(
            sql.SQL("INSERT INTO {table} ({fields}) VALUES (%s, %s)").format(
                table=sql.Identifier(self.tb_name),
                fields=sql.SQL(', ').join(map(sql.Identifier,['id',column]))
            ),(user_id,value,)
        )
        # placeholders=sql.SQL(', ').join(sql.Placeholder()*2))
        self.commit_db()

    def update_user_value(self, user_id, value, column):
        # self.cursor.execute(f"""
        #     UPDATE {self.tb_name} SET {column} = ?
        #     WHERE user_id = ?
        # """,(value, user_id,))
        self.cursor.execute(
            sql.SQL("UPDATE {table} SET {field} = %s WHERE {pkey} = %s").format(
                table=sql.Identifier(self.tb_name),
                field=sql.Identifier(column),
                pkey=sql.Identifier('id'),
            ), (value,user_id,)
        )
        self.commit_db()

    def delete_user(self, user_id):
        # self.cursor.execute(f"""
        #     DELETE FROM {self.tb_name} WHERE user_id = ?
        # """, (user_id,))
        self.cursor.execute(
            sql.SQL("DELETE FROM {table} WHERE {pkey} = %s").format(
                table=sql.Identifier(self.tb_name),
                pkey=sql.Identifier('id'),
            ), (user_id,)
        )
        self.commit_db()