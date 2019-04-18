import sqlite3
import settings

def init():
    global connection
    connection = None

def connect():
    global connection
    connection = sqlite3.connect(settings.loaded['database'], detect_types=sqlite3.PARSE_DECLTYPES)

def close():
    global connection
    if connection != None:
        return connection.close()

def is_connected():
    global connection
    return True if connection != None else False

def is_database_ready():
    global connection

    if connection != None:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT name FROM sqlite_master WHERE type='table' AND name='files';
        """)

        if cursor.fetchone() == None:
            return False
        else:
            return True


def setup_schema():
    global connection
    if connection != None:
        if is_database_ready():
            print("Table already created")
            return True
        else:
            cursor = connection.cursor()

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
                CREATE TABLE locations (
                    idlocations INTEGER     NOT NULL PRIMARY KEY AUTOINCREMENT,
                    latitude    INTEGER     NOT NULL,
                    longitude   INTEGER     NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE relations (
                    idrelations     INTEGER NOT NULL        PRIMARY KEY     AUTOINCREMENT,
                    file_id         INTEGER NOT NULL,
                    location_id     INTEGER NOT NULL,
                    event_id        INTEGER NOT NULL,
                    FOREIGN KEY(file_id)     REFERENCES files(idfiles),
                    FOREIGN KEY(location_id) REFERENCES location(idlocations),
                    FOREIGN KEY(event_id)    REFERENCES events(idevents)
                )
            """)

            print("Table successfully created")

def execute(command):
    global connection
    if connection != None:
        cursor = connection.cursor()
        cursor.execute(command)
        connection.commit()

        print("Data successfully inserted")

# In this case, data MUST be an array of paths (strings)
def insert_many(data):
    global connection
    if connection != None:
        cursor = connection.cursor()
        cursor.executemany("""
            INSERT INTO arquivos (path) 
            VALUES(?)
        """, data)