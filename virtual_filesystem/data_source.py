import sqlite3
from settings import Settings
from helpers import get_date_from_event
import datetime
import time
import yaml

import threading

class DataSource:
    def __init__(self):
        self.settings = Settings()
        self.connection = sqlite3.connect(self.settings.loaded['database'], detect_types=sqlite3.PARSE_DECLTYPES)
        self.map = {}

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
        # parsed_path = str(data[0][(str(data[0]).rfind('/') + 1):])
        for full_path in full_paths:
            partial_path = str(full_path[0][(str(full_path[0]).rfind('/') + 1):])
            self.map[partial_path] = str(full_path[0])

    def get_localizations(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT idlocalizations, latitude, longitude FROM localizations")
        return_data = cursor.fetchall()
        # print(f"Found this localizations: {return_data}")
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
        cursor.execute("SELECT start_time, end_time, summary FROM events")
        return cursor.fetchall()

    def get_mock_time(self):
        with open(self.settings.loaded['mock_time_localization'], "r") as stream:
            try:
                data = yaml.load(stream, Loader=yaml.FullLoader)
                # return datetime.datetime.strptime(data['time'], '%Y-%m-%d %H:%M:%S')
                if data == None:
                    print("ERRO!!!!: DATA ATUAL == NONE")

                else:
                    self.settings.add_runtime('actual_time', data['time'])
                # return data['time'] # Já é datetime

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

        # print("Actual Time == ", actual_time)
        # print("Using UTC in calendar ?", self.settings.loaded['event_dates_in_utc'])
        stored_events = self.get_events()
        for stored_event in stored_events:
            # print("----")
            # print("Stored stert event time == ", get_date_from_event(stored_event[2], self.settings))
            # print("Stored stop event time == ", get_date_from_event(stored_event[0], self.settings))
            # print("Event summary == ", stored_event[1])
            # print("Actual time == ", actual_time)
            if get_date_from_event(stored_event[2], self.settings) <= actual_time: # if the start_event time was before
                # print("\tEvent already started")
                if get_date_from_event(stored_event[0], self.settings) >= actual_time: # if the end_event still not done
                    # print("\t------------------------ IN EVENT: ", stored_event[1]) # Show event summary
                    return stored_event # returns the found event
            # print("----")


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
        max_results = 10

        if localization != None and event_summary != None:
            cursor.execute("""
                    SELECT f.path 
                    FROM relations AS r 
                    INNER JOIN files AS f
                    WHERE localization_id=? 
                        AND event_summary=? 
                        AND f.idfiles=r.file_id
                    ORDER BY r.hits DESC 
                    LIMIT 0, ?;
                    """, (localization, event_summary, max_results))

        elif localization != None:
            # print(f"Localization = {localization}")
            # print(f"Max results = {max_results}")
            cursor.execute("""
                    SELECT f.path 
                    FROM relations AS r 
                    INNER JOIN files AS f
                    WHERE localization_id=? 
                        AND f.idfiles=r.file_id
                    ORDER BY r.hits DESC 
                    LIMIT 0, ?;
                    """, (localization, max_results))

        elif event_summary != None:
            cursor.execute("""
                    SELECT f.path
                    FROM relations AS r 
                    INNER JOIN files AS f
                    WHERE event_summary=? 
                        AND f.idfiles=r.file_id
                    ORDER BY r.hits DESC 
                    LIMIT 0, ?;
                    """, (event_summary, max_results))

        else:
            cursor.execute("""
                    SELECT f.path 
                    FROM relations AS r 
                    INNER JOIN files AS f
                    WHERE f.idfiles=r.file_id
                    ORDER BY r.hits DESC 
                    LIMIT 0, ?;
                    """, (max_results,))

        return cursor.fetchall()

        #
        # if localization != None:
        #
        # else:


    def close(self):
        if self.connection != None:
            self.connection.close()

