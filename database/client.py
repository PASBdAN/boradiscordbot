import psycopg2
from psycopg2 import sql

from manage import dict_config
DATABASE_URL = dict_config['DATABASE_URL']

class Client():
    def __init__(self, tb_name):
        self.conn = psycopg2.connect(DATABASE_URL)
        self.cursor = self.conn.cursor()
        self.schema_file = 'database/schemas/tables_schemas.sql'
        with open(self.schema_file, 'r') as f:
            schema = f.read()
            self.cursor.execute(schema)
        self.tb_name = tb_name


    def select(self, *columns, **filters):
        if columns:
            query = sql.SQL("SELECT {fields} FROM {table}").format(
                fields=sql.SQL(',').join([
                    sql.Identifier(x) for x in [str(x) for x in columns]
                ]),
                table=sql.Identifier(self.tb_name)
            )
        else:
            query = sql.SQL('SELECT * FROM {table}').format(
                table = sql.Identifier(self.tb_name)
            )
        if not filters:
            self.cursor.execute(
                query, tuple([x[1] for x in filters.items()])
            )
            return self.cursor.fetchall()
        query += sql.SQL(' WHERE ')
        for item in filters.items():
            query += sql.SQL('{field} = %s').format(
                field = sql.Identifier(str(item[0]))
            )
            if item != list(filters.items())[-1]:
                query += sql.SQL(' AND ')
        self.cursor.execute(
            query, tuple([x[1] for x in filters.items()])
        )
        return self.cursor.fetchall()


    def insert(self, **values):
        query = sql.SQL('INSERT INTO {table} ({fields}) VALUES (').format(
                table=sql.Identifier(self.tb_name),
                fields=sql.SQL(',').join([
                    sql.Identifier(x) for x in [x[0] for x in values.items()]
                ])
            )
        for i in list(range(0,len(values.items())-1)):
            query += sql.SQL('%s, ')
        query += sql.SQL('%s)')

        self.cursor.execute(    
            query, tuple([x[1] for x in values.items()])
        )
        return self.commit_db()


    def delete(self, **filters):
        query = sql.SQL("DELETE FROM {table}").format(
            table=sql.Identifier(self.tb_name)
        )
        if not filters:
            return query
        query += sql.SQL(' WHERE ')
        for item in filters.items():
            query += sql.SQL('{field} = %s').format(
                field = sql.Identifier(str(item[0]))
            )
            if item != list(filters.items())[-1]:
                query += sql.SQL(' AND ')
        self.cursor.execute(
            query, tuple([x[1] for x in filters.items()])
        )
        return self.commit_db()


    def update_by_id(self, **values):
        query = sql.SQL("UPDATE {table} SET ").format(
            table=sql.Identifier(self.tb_name)
        )

        for item in list(values.items())[1:]:
            query += sql.SQL('{field} = %s').format(
                field = sql.Identifier(str(item[0]))
            )
            if item != list(values.items())[-1]:
                query += sql.SQL(', ')

        query += sql.SQL(' WHERE {pkey} = %s').format(
            pkey=sql.Identifier('id')
        )
        lista = [x[1] for x in list(values.items())[1:]]
        lista.append(list(values.items())[0][1])
        self.cursor.execute(
            query, tuple(lista)
        )
        return self.commit_db()


    def commit_db(self):
        if self.conn:
            self.conn.commit()
    

    def close_db(self):
        if self.conn:
            self.conn.close()
            print("Sessão finalizada")

        