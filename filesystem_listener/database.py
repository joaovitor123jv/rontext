import sqlite3
import settings


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
                    longitude       INTEGER     NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE relations (
                    idrelations     INTEGER  NOT NULL        PRIMARY KEY     AUTOINCREMENT,
                    file_id         INTEGER  NOT NULL,
                    localization_id INTEGER,
                    event_id        INTEGER,
                    time            DATETIME NOT NULL,
                    FOREIGN KEY(file_id)     REFERENCES files(idfiles),
                    FOREIGN KEY(localization_id) REFERENCES localization(idlocalizations),
                    FOREIGN KEY(event_id)    REFERENCES events(idevents)
                )
            """)

            print("Table successfully created")

def execute(command):
    if is_connected():
        cursor = get_connection().cursor()
        cursor.execute(command)
        get_connection().commit()

        print("Data successfully inserted")

# In this case, data MUST be an array of paths (strings)
def insert_many(data):
    if is_connected():
        cursor = get_connection().cursor()
        cursor.executemany("""
            INSERT INTO arquivos (path) 
            VALUES(?)
        """, data)

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
def store_file(path):
    if is_connected():
        cursor = get_connection().cursor()

        cursor.execute("SELECT idfiles, path FROM files WHERE path=?", (path,))

        if cursor.fetchall() == []:
            cursor.execute("INSERT INTO files (path) VALUES (?)", (path,))
            get_connection().commit()
            print(f"Registro de arquivo '{path}' adicionado ao banco de dados")

# Remove o registro do arquivo na tabela de arquivos, se arquivo tiver sido armazenado anteriormente
def delete_file_reference(path):
    if is_connected():
        cursor = get_connection().cursor()

        cursor.execute("SELECT idfiles, path FROM files WHERE path=?", (path,))

        if cursor.fetchall() != None:
            cursor.execute("DELETE FROM files WHERE path=?", (path,))
            get_connection().commit()
            print(f"Registro de arquivo '{path}' removido do banco de dados")

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


def store_relationship(relationship):
    print("Relationship === ", relationship)






