import psycopg2

from psycopg2 import OperationalError


# SQL Implementation
def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occured")
    return connection

# Create new db in postgresql db server
def create_database(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

def execute_db_check(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        list_database = cursor.fetchall()
        print(list_database)
        if 'playlists' in list_database:
            print("'{}' Database already exists".format("playlists"))
            return True
        else:
            print("'{}' Database does not exist.".format("playlists"))
            return False
            

    except OperationalError as e:
        print(f"The error '{e}' occurred")


# Connect to default database
connection = create_connection(
    "postgres", "postgres", "PLACEHOLDER", "127.0.0.1", "5432"
)
db_check_query = ("SELECT datname FROM pg_database;")
execute_db_check(connection, db_check_query)

if execute_db_check is True:
    create_database_query = "CREATE DATABASE playlists"
    create_database(connection, create_database_query)
else:

#if db_check_query is True:

    print('Done')


# Connect to playlist database based on create_database_query above
connection = create_connection("playlists", "postgres", "PLACEHOLDER", "127.0.0.1", "5432")

create_playlist_table = """
CREATE TABLE IF NOT EXISTS Tracks (
  Folder character (90),
  Artist character (90), 
  Album character (90),
  Title character (90)
)
"""
execute_query(connection, create_playlist_table)

for trackdict in playlist:
    columns = ', '.join(str(x).replace('/','_').replace('\'','') for x in trackdict.keys())
    values = ', '.join("'" + str(x).replace('/', '_').replace('\'','') + "'" for x in trackdict.values())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ('Tracks', columns, values)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(sql)
