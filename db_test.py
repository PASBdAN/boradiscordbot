import psycopg2
from psycopg2 import Error
from time import sleep

try:
    # Connect to an existing database
    '''
    connection = psycopg2.connect(
        user="iahdcmqnelbrfy",
        password="6f9a9833e0922ea8b9729e5701a706664c6b1308df8207257e16ff502059da90",
        host="ec2-54-83-137-206.compute-1.amazonaws.com",
        port="5432",
        database="dbful1aoklvin4"
    )
    '''
    connection = psycopg2.connect("postgres://iahdcmqnelbrfy:6f9a9833e0922ea8b9729e5701a706664c6b1308df8207257e16ff502059da90@ec2-54-83-137-206.compute-1.amazonaws.com:5432/dbful1aoklvin4")
    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")
    # Executing a SQL query
    cursor.execute("SELECT version();")
    # Fetch result
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")
    # sleep(2)
    # cursor.execute(open("database/schemas/guilds_schema.sql","r").read())
    # connection.commit()
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")