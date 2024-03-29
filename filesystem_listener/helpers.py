from io import StringIO
import json
import settings
import database
import datetime
import time


def point_inside_circle(point, circle):
    precision = float(settings.loaded["localization_precision"])
    a = (point["latitude"] - circle["latitude"]) * (point["latitude"] - circle["latitude"])
    b = (point["longitude"] - circle["longitude"]) * (point["longitude"] - circle["longitude"])
    return ((a + b) < (precision * precision))


def get_actual_localization(cursor):
    localization = settings.runtime['localization']

    stored_localizations = database.get_localizations(cursor)

    if stored_localizations != None:
        for stored_localization in stored_localizations:
            temp_localization = {
                'id': stored_localization[0],
                'latitude': stored_localization[1],
                'longitude': stored_localization[2]
            }

            if point_inside_circle(localization, temp_localization):
                return temp_localization['id']

    return False


def get_mock_time():
    with open(settings.loaded['mock_time_localization'], "r") as stream:
        try:
            data = json.load(stream)
            # return datetime.datetime.strptime(data['time'], '%Y-%m-%d %H:%M:%S')
            if data == None:
                print("ERRO!!!!: DATA ATUAL == NONE")

            else:
                settings.add_runtime('actual_time', data['time'])
            # return data['time'] # Já é datetime

        except json.JSONDecodeError as exc:
            print(exc)
            return None


def get_date_from_event(event_date, using_utc=False):
    if using_utc:
        now_timestamp = time.time()
        offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
        return (datetime.datetime.strptime(event_date, '%Y-%m-%d %H:%M:%S') + offset)
    else:
        return datetime.datetime.strptime(event_date, '%Y-%m-%d %H:%M:%S')


def get_actual_event(cursor):
    actual_time = None

    if settings.loaded['use_time_mock']:
        get_mock_time()
        actual_time = settings.runtime['actual_time']
    else:
        actual_time = datetime.datetime.now()

    # print("Actual Time == ", actual_time)

    stored_events = database.get_events(cursor)

    for stored_event in stored_events:
        if get_date_from_event(stored_event[2], settings.loaded['event_dates_in_utc']) <= actual_time: # if the start_event time was before
            if get_date_from_event(stored_event[0], settings.loaded['event_dates_in_utc']) >= actual_time: # if the end_event still not done
                # print("IN EVENT: ", stored_event[1]) # Show event summary
                return stored_event # returns the found event
