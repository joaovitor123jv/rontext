import time
import threading
import subprocess
import settings
import database
import helpers

def point_inside_circle(point, circle):
    a = (point["latitude"] - circle["latitude"]) * (point["latitude"] - circle["latitude"])
    b = (point["longitude"] - circle["longitude"]) * (point["longitude"] - circle["longitude"])
    precision = float(settings.loaded["localization_precision"])
    return (a + b) < (precision * precision)

def already_in_database(connection, localization):
    stored_localizations = database.get_localizations(connection)

    if stored_localizations != None:
        for stored_localization in stored_localizations:
            temp_localization = {
                'latitude': stored_localization[1],
                'longitude': stored_localization[2]
            }

            if point_inside_circle(localization, temp_localization):
                return True

    return False

def listener():
    # print("**** SIDE_THREAD ID == ", threading.get_ident())
    time.sleep(1)
    connection = database.connect()
    while True:
        return_data = subprocess.run([settings.loaded['localization_bin']], stdout=subprocess.PIPE)
        parsed_return = helpers.parse_yaml_string(return_data.stdout.decode('utf8'))

        settings.add_runtime('localization', parsed_return)

        if already_in_database(connection, settings.runtime['localization']):
            # print("Localization already in database, skipping")
            pass

        else:
            # print("Localization is not in database, inserting")
            with connection:
                database.store_localization(connection, settings.runtime['localization'])


        time.sleep(settings.loaded['localization_plugin_wait_time']) # Waits 1 second till the next localization check

def start_plugin():
    try:
        thread = threading.Thread(target=listener)
        thread.start()

    except:
        print("Failed to start localization plugin")
