import psycopg2

from psycopg2 import OperationalError
from pl_format import *

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
        print("Create db query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Execute... {} ...executed successfully\n".format(query))
    except OperationalError as e:
        print(f"The error '{e}' occurred")

def execute_db_check(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        list_database = cursor.fetchall()
        print(list_database)
        db_name = 'playlists'
        if (db_name,) in list_database:
            print("'{}' Database already exists".format("playlists"))
            return True
        else:
            print("'{}' Database does not exist.".format("playlists"))
            return False
    except OperationalError as e:
        print(f"The error '{e}' occurred")

def default_connection():
    connection = create_connection(
    "postgres", "postgres", "iguana90", "127.0.0.1", "5432"
    )
    db_check_query = ("SELECT datname FROM pg_database;")
    dbcheckbool = execute_db_check(connection, db_check_query)
    print(dbcheckbool)
    db_name = 'playlists'

    if dbcheckbool == False:
        create_database_query = "CREATE DATABASE {}".format(db_name)
        create_database(connection, create_database_query)
    else:
        print('database {} already exists. skipping creation...'.format(db_name))
  
def cleanup_tables():
    # cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('playlist',))
    # cur.fetchone()[0]
    delete_tables = """
    DROP TABLE IF EXISTS tracks, playlist_names
    """
    execute_query(connection_playlist(), delete_tables)

def connection_playlist():
    connection = create_connection("playlists", "postgres", "iguana90", "127.0.0.1", "5432")
    return connection

def create_table_playlist_names():
    create_playlist_table = """
    CREATE TABLE Playlist_Names (
    id SMALLSERIAL PRIMARY KEY,
    name character (90)
    )
    """
    execute_query(connection_playlist(), create_playlist_table)


def create_table_tracks():
    create_playlist_table = """
    CREATE TABLE IF NOT EXISTS Tracks (
    track_id SMALLSERIAL PRIMARY KEY,
    Folder character (90),
    Artist character (90), 
    Album character (90),
    Title character (90),
    playlist_id integer REFERENCES playlist_names (id)
    )
    """
    execute_query(connection_playlist(), create_playlist_table)