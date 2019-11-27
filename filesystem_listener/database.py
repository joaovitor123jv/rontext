import sqlite3
import settings
import datetime
import time

import threading

def connect():
    print("Connecting")
    return sqlite3.connect(settings.loaded['database'], detect_types=sqlite3.PARSE_DECLTYPES)

def is_database_ready(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='files';
    """)

    return False if (cursor.fetchone() == None) else True

    # if cursor.fetchone() == None:
    #     return False
    # else:
    #     return True

def notify_database_update(connection, cursor):
    print("Starting notification")
    if ('waiting_commit' in settings.runtime
        and settings.runtime['waiting_commit'] == True):
        print("First IF PASS")
        if (time.time() - settings.runtime['time_notified']) > 1:
            print("Elapsed time since last notification == ", time.time() - settings.runtime['time_notified'])
            print("Time now: ", time.time())
            print("Last Time notified: ", settings.runtime['time_notified'])
            print("Starting commit!")
            inicio = time.time()
            connection.commit()
            tempo = time.time() - inicio
            print("ELAPSED COMMIT TIME = ", tempo)
            print("FINISHED COMMIT")

        settings.add_runtime('time_notified', time.time())
    else:
        print("Beginning transaction")
        cursor.execute('BEGIN');
        settings.add_runtime('waiting_commit', True)
        settings.add_runtime('time_notified', time.time())

def setup_schema():
    connection = connect()
    if is_database_ready(connection):
        print("Table already created")
        connection.close()
        return True
    else:
        cursor = connection.cursor()

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

        connection.commit()
        connection.close()
        print("Table successfully created")

def store_events(connection, events):
    cursor = connection.cursor()
    notify_database_update(connection, cursor)
    cursor.executemany("INSERT INTO events (summary, start_time, end_time) VALUES (?, ?, ?)", events)
    # connection.commit()

def get_events(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT start_time, end_time, summary FROM events")
    return cursor.fetchall()

# Cria um registro do arquivo na tabela de arquivos, se arquivo já não tiver sido armazenado anteriormente
def store_file(connection, path, hits=1):
    print("Inserindo arquivo com nome: ", path)
    cursor = connection.cursor()
    notify_database_update(connection, cursor)
    cursor.execute("SELECT idfiles, path FROM files WHERE path=?", (path,))
    response = cursor.fetchone()

    if response == [] or response == None:
        cursor.execute("INSERT INTO files (path, hits) VALUES (?, ?)", (path, hits))
        # connection.commit()
        cursor.execute("SELECT idfiles, path FROM files WHERE path=?", (path,))
        response = cursor.fetchone()
        if path == '/home/joaovitor/experimentos/dados/START':
            print("Starting time monitoring")
            settings.add_runtime('start_timestamp', time.time())
        elif path == '/home/joaovitor/experimentos/dados/END':
            print("Time elapsed == ", time.time() - settings.runtime['start_timestamp'])
            # exit(0)
        # print(f"Arquivo '{path}' no banco")

    return response[0]

def increase_file_hits(connection, path):
    cursor = connection.cursor()
    notify_database_update(connection, cursor)
    cursor.execute("UPDATE files SET hits=hits+1 WHERE path=?;", (path,))
    # connection.commit()
    # print(f"Hits do arquivo '{path}' atualizado no banco de dados")


# Remove o registro do arquivo na tabela de arquivos, se arquivo tiver sido armazenado anteriormente
def delete_file_reference(connection, path):
    cursor = connection.cursor()
    notify_database_update(connection, cursor)
    cursor.execute("SELECT idfiles, path FROM files WHERE path=?", (path,))

    if cursor.fetchall() != None:
        cursor.execute("DELETE FROM files WHERE path=?", (path,))
        # connection.commit()
        # print(f"Registro de arquivo '{path}' removido do banco de dados")

def get_localizations(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT idlocalizations, latitude, longitude FROM localizations")
    return cursor.fetchall()

def store_localization(connection, localization):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO localizations (latitude, longitude) VALUES (?, ?)", (localization['latitude'], localization['longitude']))
    # connection.commit()

def insert_relationship(connection, relationship, cursor):
    notify_database_update(connection, cursor)
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
    # connection.commit()

def update_relationship(connection, relation_data, cursor):
    notify_database_update(connection, cursor)
    cursor.execute("UPDATE relations SET hits=hits+1, last_access=? WHERE idrelations=?", (datetime.datetime.now(), relation_data[0][0]))
    # connection.commit()

def store_relationship(connection, relationship):
    # print("Relationship === ", relationship)
    cursor = connection.cursor()
    notify_database_update(connection, cursor)

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
        update_relationship(connection, relation_data, cursor)

    else:
        # print("Can't found this relationship in database, inserting a new one")
        insert_relationship(connection, relationship, cursor)



