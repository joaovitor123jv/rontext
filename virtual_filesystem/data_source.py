import sqlite3
from settings import Settings
from helpers import get_date_from_event, has_duplicates, get_duplicates
import datetime
import time
import yaml

import threading

class DataSource:
    def __init__(self):
        self.settings = Settings()
        self.connection = sqlite3.connect(self.settings.loaded['database'], detect_types=sqlite3.PARSE_DECLTYPES)
        self.map = {}
        self.file_by_localization_map = {}
        self.file_by_event_map = {}
        self.localization_map = {}
        self.event_map = {}

    def is_database_ready(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='files';")
        return False if cursor.fetchone() == None else True

    def point_inside_circle(self, point, circle):
        precision = float(self.settings.loaded["localization_precision"])
        a = (point["latitude"] - circle["latitude"]) * (point["latitude"] - circle["latitude"])
        b = (point["longitude"] - circle["longitude"]) * (point["longitude"] - circle["longitude"])
        return ((a + b) < (precision * precision))

    def update_file_map(self, full_paths):
        self.map = {}
        duplicates = None
        if has_duplicates(full_paths):
            duplicates = get_duplicates(full_paths)

        for full_path in full_paths:
            full_path_str = str(full_path[0])
            if duplicates != None:
                if full_path_str in duplicates:
                    self.map[full_path_str.replace('/', '|')] = full_path_str
                else:
                    keys = full_path_str.split("/")
                    last_key = keys[len(keys) - 1] # Separate file name "/home/user/Documents/test" -> "test"
                    self.map[last_key] = full_path_str # Stores an 'object' with the filename as key and full_path as value
            else:
                keys = full_path_str.split("/")
                last_key = keys[len(keys) - 1] # Separate file name "/home/user/Documents/test" -> "test"
                self.map[last_key] = full_path_str # Stores an 'object' with the filename as key and full_path as value

    def update_localization_map(self, full_localizations):
        self.localization_map = {}
        for localization in full_localizations:
            pretty_name = None
            if localization[3] != None:
                pretty_name = str(localization[3]) # Localization name
            else:
                pretty_name = str(localization[0]) # Localization ID

            self.localization_map[pretty_name] = str(localization[0]) # Stores a Localization ID (content) related to pretty_name (key)

    def update_event_map(self, full_events):
        self.event_map = {}
        for event in full_events:
            pretty_name = str(event[1]) # event ID

            self.event_map[pretty_name] = pretty_name # Stores a Localization ID (content) related to pretty_name (key)

    def update_file_by_localization_map(self, localization_key, full_paths):
        self.file_by_localization_map[localization_key] = {}
        for full_path in full_paths:
            keys = str(full_path[0]).split("/")
            last_key = keys[len(keys) - 1] # Separate file name "/home/user/Documents/test" -> "test"
            self.file_by_localization_map[localization_key][last_key] = str(full_path[0]) # Stores an 'object' with the filename as key and full_path as value

    def update_file_by_event_map(self, event_key, full_paths):
        self.file_by_event_map[event_key] = {}
        for full_path in full_paths:
            keys = str(full_path[0]).split("/")
            last_key = keys[len(keys) - 1] # Separate file name "/home/user/Documents/test" -> "test"
            self.file_by_event_map[event_key][last_key] = str(full_path[0]) # Stores an 'object' with the filename as key and full_path as value

    def get_localizations(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT idlocalizations, latitude, longitude, name FROM localizations")
        return_data = cursor.fetchall()
        return return_data

    def get_actual_localization(self):
        if "localization" in self.settings.runtime:
            localization = self.settings.runtime['localization']
            stored_localizations = self.get_localizations()
            if stored_localizations != None:
                for stored_localization in stored_localizations:
                    temp_localization = {
                        'id': stored_localization[0],
                        'latitude': stored_localization[1],
                        'longitude': stored_localization[2]
                    }
                    if self.point_inside_circle(localization, temp_localization):
                        return temp_localization['id']
        return None

    def get_events(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT start_time, end_time, summary FROM events ORDER BY idevents DESC")
        return cursor.fetchall()

    def get_mock_time(self):
        with open(self.settings.loaded['mock_time_localization'], "r") as stream:
            try:
                data = yaml.load(stream, Loader=yaml.FullLoader)
                # return datetime.datetime.strptime(data['time'], '%Y-%m-%d %H:%M:%S')
                if data == None:
                    print("ERROR: actual date == None")

                else:
                    self.settings.add_runtime('actual_time', data['time'])
                # return data['time'] # Already a datetime

            except yaml.YAMLError as exc:
                # print(exc)
                return None

    def get_time(self):
        if self.settings.loaded['use_time_mock']:
            self.get_mock_time()
            return self.settings.runtime['actual_time']
        else:
            return datetime.datetime.now()

    def get_actual_event(self):
        actual_time = self.get_time()
        stored_events = self.get_events()
        for stored_event in stored_events:
            if get_date_from_event(stored_event[2], self.settings) <= actual_time: # if the start_event time was before
                if get_date_from_event(stored_event[0], self.settings) >= actual_time: # if the end_event still not done
                    return stored_event # returns the found event


    def get_files(self):
        event = None
        event_summary = None
        localization = None

        if self.settings.loaded['use_agenda']:
            event = self.get_actual_event()

        if self.settings.loaded['use_localization']:
            localization = self.get_actual_localization()

        if event != None:
            event_summary = event[1]

        # print("----------- GET FILES --------------")
        # print(f"Localization == {localization}")
        # print(f"Event summary == {event_summary}")

        cursor = self.connection.cursor()
        max_results = 20

        if localization != None and event_summary != None:
            cursor.execute("""
                    SELECT f.path
                    FROM relations AS r
                    INNER JOIN files AS f
                    WHERE localization_id=?
                        AND event_summary=?
                        AND f.idfiles=r.file_id
                    ORDER BY r.hits DESC,
                        f.idfiles DESC
                    LIMIT 0, ?;
                    """, (localization, event_summary, max_results))

        elif localization != None:
            cursor.execute("""
                    SELECT f.path
                    FROM relations AS r
                    INNER JOIN files AS f
                    WHERE localization_id=?
                        AND f.idfiles=r.file_id
                        AND event_summary='NULL'
                    ORDER BY r.hits DESC,
                        f.idfiles DESC
                    LIMIT 0, ?;
                    """, (localization, max_results))

        elif event_summary != None:
            cursor.execute("""
                    SELECT f.path
                    FROM relations AS r
                    INNER JOIN files AS f
                    WHERE event_summary=?
                        AND f.idfiles=r.file_id
                    ORDER BY r.hits DESC,
                        f.idfiles DESC
                    LIMIT 0, ?;
                    """, (event_summary, max_results))

        else:
            cursor.execute("""
                    SELECT f.path
                    FROM relations AS r
                    INNER JOIN files AS f
                    WHERE f.idfiles=r.file_id
                        AND event_summary='NULL'
                    ORDER BY r.hits DESC,
                        f.idfiles DESC
                    LIMIT 0, ?;
                    """, (max_results,))

        return cursor.fetchall()

    def get_files_by(self, type_key, item_key):
        cursor = self.connection.cursor()
        max_results = 20

        if type_key == 'localization':
            if self.localization_map == {}:
                self.update_localization_map( self.get_localizations() )

            localization = self.localization_map[item_key]
            cursor.execute("""
                    SELECT f.path
                    FROM relations AS r
                    INNER JOIN files AS f
                    WHERE localization_id=?
                        AND f.idfiles=r.file_id
                    ORDER BY r.hits DESC,
                        f.idfiles DESC
                    LIMIT 0, ?;
                    """, (localization, max_results))
            return cursor.fetchall()

        elif type_key == 'event':
            if self.event_map == {}:
                self.update_event_map( self.get_events() )

            event = self.event_map[item_key]
            cursor.execute("""
                    SELECT f.path
                    FROM relations AS r
                    INNER JOIN files AS f
                    WHERE event_summary=?
                        AND f.idfiles=r.file_id
                    ORDER BY r.hits DESC,
                        f.idfiles DESC
                    LIMIT 0, ?;
                    """, (item_key, max_results))
            return cursor.fetchall()

        else:
            print("Yet not implemented")

        return None

    def close(self):
        if self.connection != None:
            self.connection.close()
