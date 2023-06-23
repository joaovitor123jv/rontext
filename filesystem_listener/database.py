import sqlite3
import settings
import datetime
import helpers
import queue
import time


def connect():
    print("Connecting")
    return sqlite3.connect(settings.loaded['database'], detect_types=sqlite3.PARSE_DECLTYPES)


def is_database_ready(cursor):
    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='files';
    """)

    return False if (cursor.fetchone() == None) else True


def get_relationship(cursor, file_id):
    event_summary = None
    event = None
    relationship = None

    if settings.loaded['use_agenda']:
        event = helpers.get_actual_event(cursor)

    event_summary = event[1] if event != None else "NULL"

    if settings.loaded['use_localization'] and settings.loaded['use_agenda']:
        relationship = {
            'file_id': file_id,
            'localization_id': helpers.get_actual_localization(cursor),
            'event_summary': event_summary
        }
    elif settings.loaded['use_localization']:
        relationship = {
            'file_id': file_id,
            'localization_id': helpers.get_actual_localization(cursor),
            'event_summary': None
        }

    elif settings.loaded['use_agenda']:
        relationship = {
            'file_id': file_id,
            'localization_id': None,
            'event_summary': event_summary
        }

    else:
        relationship = {
            'file_id': file_id,
            'localization_id': None,
            'event_summary': None
        }

    return relationship


def insert_path(cursor, path):
    cursor.execute("SELECT idfiles, path FROM files WHERE path=?", (path,))
    response = cursor.fetchone()

    try:
        if response == [] or response == None:
            cursor.execute("INSERT INTO files (path, hits) VALUES (?, ?)", (path, 1))
            cursor.execute("SELECT idfiles, path FROM files WHERE path=?", (path,))
            response = cursor.fetchone()
        else:
            cursor.execute("UPDATE files SET hits=hits+1 WHERE path=?;", (path,))

        relationship = get_relationship(cursor, response[0])
        store_relationship(cursor, relationship)
    except:
        time.sleep(1)
        insert_path(cursor, path)


def insert_queue_items(connection, cursor, path=None):
    if path != None:
        insert_path(cursor, path)
        while True:
            try:
                next_path = settings.runtime['insert_queue'].get_nowait()
                insert_path(cursor, next_path)
            except queue.Empty:
                return

        # if path == '/home/joaovitor/experimentos/dados/START':
        #     print("Starting time monitoring")
        #     settings.add_runtime('start_timestamp', time.time())
        # elif path == '/home/joaovitor/experimentos/dados/END':
        #     print("Time elapsed == ", time.time() - settings.runtime['start_timestamp'])


def file_insert_handler():
    connection = connect()
    cursor = connection.cursor()
    settings.add_runtime('insert_queue', queue.Queue())

    while True:
        print("Waiting input")
        time.sleep(1)
        try:
            path = settings.runtime['insert_queue'].get()
            # print("== Beginning transaction")
            cursor.execute('BEGIN');
            insert_queue_items(connection, cursor, path)
            # print("== Commiting alterations")
            connection.commit()
            end = time.time()
            # print("== DONE")
            if 'start_timestamp' in settings.runtime:
                print("=======================")
                print("Elapsed time: ", end-settings.runtime['start_timestamp'])
                print("=======================")
        except queue.Empty:
            pass


def setup_schema():
    connection = connect()
    cursor = connection.cursor()
    if is_database_ready(cursor):
        print("Table already created")
        connection.close()
        return True
    else:
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


def store_events(cursor, events):
    cursor.executemany("INSERT INTO events (summary, start_time, end_time) VALUES (?, ?, ?)", events)


def get_events(cursor):
    cursor.execute("SELECT start_time, end_time, summary FROM events")
    return cursor.fetchall()


# Cria um registro do arquivo na tabela de arquivos, se arquivo já não tiver sido armazenado anteriormente
def store_file(path): #, hits=1):
    settings.runtime['insert_queue'].put(path)


# Remove o registro do arquivo na tabela de arquivos, se arquivo tiver sido armazenado anteriormente
def delete_file_reference(cursor, path):
    cursor.execute("SELECT idfiles, path FROM files WHERE path=?", (path,))
    if cursor.fetchall() != None:
        cursor.execute("DELETE FROM files WHERE path=?", (path,))


def get_localizations(cursor):
    cursor.execute("SELECT idlocalizations, latitude, longitude FROM localizations")
    return cursor.fetchall()


def store_localization(cursor, localization):
    cursor.execute("INSERT INTO localizations (latitude, longitude) VALUES (?, ?)", (localization['latitude'], localization['longitude']))
    cursor.execute("UPDATE localizations SET name = idlocalizations WHERE name IS NULL AND latitude = ? AND longitude = ?", 
                   (localization['latitude'], localization['longitude']))


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


def update_relationship(relation_data, cursor):
    cursor.execute("UPDATE relations SET hits=hits+1, last_access=? WHERE idrelations=?", (datetime.datetime.now(), relation_data[0][0]))


def store_relationship(cursor, relationship):
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
            return False


    relation_data = cursor.fetchall()

    if relation_data != []:
        update_relationship(relation_data, cursor)
    else:
        insert_relationship(relationship, cursor)
