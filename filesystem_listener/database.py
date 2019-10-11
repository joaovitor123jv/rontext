import sqlite3
import settings
import datetime
import time


import threading

connection = {}

def init():
    global connection
    connection = {}

def connect():
    global connection
    connection[str(threading.get_ident())] = sqlite3.connect(settings.loaded['database'], detect_types=sqlite3.PARSE_DECLTYPES)

def close():
    global connection
    if connection != None:
        for one_connection in connection:
            print("ONE_CONNECTION == ", one_connection)
            one_connection.close()

def is_connected():
    global connection
    if str(threading.get_ident()) in connection:
        return True if connection[str(threading.get_ident())] != None else False
    else:
        return False

def get_connection():
    global connection
    return connection[str(threading.get_ident())]

def is_database_ready():
    if is_connected():
        cursor = get_connection().cursor()

        cursor.execute("""
            SELECT name FROM sqlite_master WHERE type='table' AND name='files';
        """)

        if cursor.fetchone() == None:
            return False
        else:
            return True


def setup_schema():
    if is_connected():
        if is_database_ready():
            print("Table already created")
            return True
        else:
            cursor = get_connection().cursor()

            cursor.execute("""
                CREATE TABLE files (
                    idfiles     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    hits        INTEGER NOT NULL,
                    path        TEXT    NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE events (
                    idevents    INTEGER     NOT NULL PRIMARY KEY AUTOINCREMENT,
                    summary     TEXT        NOT NULL,
                    start_time  DATETIME    NOT NULL,
                    end_time    DATETIME    NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE localizations (
                    idlocalizations INTEGER     NOT NULL PRIMARY KEY AUTOINCREMENT,
                    latitude        INTEGER     NOT NULL,
                    longitude       INTEGER     NOT NULL,
                    name            TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE relations (
                    idrelations     INTEGER  NOT NULL        PRIMARY KEY     AUTOINCREMENT,
                    file_id         INTEGER  NOT NULL,
                    localization_id INTEGER,
                    event_summary   TEXT,
                    last_access     DATETIME NOT NULL,
                    hits            INTEGER NOT NULL,
                    FOREIGN KEY(file_id)     REFERENCES files(idfiles),
                    FOREIGN KEY(localization_id) REFERENCES localization(idlocalizations)
                )
            """)

            get_connection().commit()

            print("Table successfully created")

def execute(command):
    if is_connected():
        cursor = get_connection().cursor()
        cursor.execute(command)
        get_connection().commit()

        # print("Data successfully inserted")

# In this case, data MUST be an array of paths (strings)
def insert_many(data):
    if is_connected():
        cursor = get_connection().cursor()
        cursor.executemany("""
            INSERT INTO arquivos (path) 
            VALUES(?)
        """, data)
        get_connection().commit()

def store_events(events):
    if is_connected():
        cursor = get_connection().cursor()
        cursor.executemany("INSERT INTO events (summary, start_time, end_time) VALUES (?, ?, ?)", events)
        get_connection().commit()

def get_events():
    if is_connected():
        cursor = get_connection().cursor()
        cursor.execute("SELECT start_time, end_time, summary FROM events")
        return cursor.fetchall()

# Cria um registro do arquivo na tabela de arquivos, se arquivo já não tiver sido armazenado anteriormente
def store_file(path, hits=1):
    if is_connected():
        cursor = get_connection().cursor()

        cursor.execute("SELECT idfiles, path FROM files WHERE path=?", (path,))

        response = cursor.fetchone()

        if response == [] or response == None:
            cursor.execute("INSERT INTO files (path, hits) VALUES (?, ?)", (path, hits))
            get_connection().commit()
            cursor.execute("SELECT idfiles, path FROM files WHERE path=?", (path,))
            response = cursor.fetchone()
            if path == '/home/joaovitor/experimentos/dados/START':
                settings.add_runtime('start_timestamp', time.time())
            elif path == '/home/joaovitor/experimentos/dados/END':
                print("Time elapsed == ", time.time() - settings.runtime['start_timestamp'])
                exit(0)
            print(f"Arquivo '{path}' no banco")

        return response[0]

def increase_file_hits(path):
    if is_connected():
        cursor = get_connection().cursor()
        cursor.execute("UPDATE files SET hits=hits+1 WHERE path=?;", (path,))
        get_connection().commit()
        # print(f"Hits do arquivo '{path}' atualizado no banco de dados")


# Remove o registro do arquivo na tabela de arquivos, se arquivo tiver sido armazenado anteriormente
def delete_file_reference(path):
    if is_connected():
        cursor = get_connection().cursor()

        cursor.execute("SELECT idfiles, path FROM files WHERE path=?", (path,))

        if cursor.fetchall() != None:
            cursor.execute("DELETE FROM files WHERE path=?", (path,))
            get_connection().commit()
            # print(f"Registro de arquivo '{path}' removido do banco de dados")

def get_localizations():
    if is_connected():
        cursor = get_connection().cursor()
        cursor.execute("SELECT idlocalizations, latitude, longitude FROM localizations")
        return_data = cursor.fetchall()

        return return_data

    else:
        connect()
        return get_localizations()

def store_localization(localization):
    if is_connected():
        cursor = get_connection().cursor()
        cursor.execute("INSERT INTO localizations (latitude, longitude) VALUES (?, ?)", (localization['latitude'], localization['longitude']))
        get_connection().commit()


def insert_relationship(relationship, cursor):
    if settings.loaded['use_agenda']:
        if settings.loaded['use_localization']:
            cursor.execute("INSERT INTO relations (file_id, localization_id, event_summary, last_access, hits) VALUES (?, ?, ?, ?, 1)", (
                relationship['file_id'], relationship['localization_id'], relationship['event_summary'], datetime.datetime.now()
            ))
        else:
            cursor.execute("INSERT INTO relations (file_id, event_summary, last_access, hits) VALUES (?, ?, ?, 1)", (
                relationship['file_id'], relationship['event_summary'], datetime.datetime.now()
            ))
    else:
        if settings.loaded['use_localization']:
            cursor.execute("INSERT INTO relations (file_id, localization_id, last_access, hits) VALUES (?, ?, ?, 1)", (
                relationship['file_id'], relationship['localization_id'], datetime.datetime.now()
            ))
        else:
            return False
    get_connection().commit()

def update_relationship(relation_data, cursor):
    cursor.execute("UPDATE relations SET hits=hits+1, last_access=? WHERE idrelations=?", (datetime.datetime.now(), relation_data[0][0]))
    get_connection().commit()

# TODO: Armazenar as relações
def store_relationship(relationship):
    # print("Relationship === ", relationship)
    if is_connected():
        cursor = get_connection().cursor()

        relation_data = None
        query = None

        if settings.loaded['use_agenda']:
            if settings.loaded['use_localization']:
                cursor.execute("""
                    SELECT idrelations
                    FROM relations
                    WHERE file_id = ?  AND localization_id = ?  AND event_summary = ?
                """, (relationship['file_id'], relationship['localization_id'], relationship['event_summary']))
            else:
                cursor.execute("""
                    SELECT idrelations
                    FROM relations
                    WHERE file_id = ?  AND event_summary = ?
                """, (relationship['file_id'], relationship['event_summary']))
        else:
            if settings.loaded['use_localization']:
                cursor.execute("""
                    SELECT idrelations
                    FROM relations
                    WHERE file_id = ?  AND localization_id = ?
                """, (relationship['file_id'], relationship['localization_id']))

            else:
                # print("No context data supplied, no relations can be found")
                return False


        relation_data = cursor.fetchall()

        # print(" RELATION_DATA === ", relation_data)

        if relation_data != []:
            # print("Found relationship in database, updating values")
            update_relationship(relation_data, cursor)

        else:
            # print("Can't found this relationship in database, inserting a new one")
            insert_relationship(relationship, cursor)



