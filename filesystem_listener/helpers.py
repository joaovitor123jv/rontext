from io import StringIO
import yaml
import settings
import database
import datetime

def parse_yaml_string(string):
    fd = StringIO(string) # Cria um 'arquivo' em memória
    return yaml.load(fd) # Faz o parse do yaml

def point_inside_circle(point, circle, precision):
    a = (point["latitude"] - circle["latitude"]) * (point["latitude"] - circle["latitude"])
    b = (point["longitude"] - circle["longitude"]) * (point["longitude"] - circle["longitude"])
    return (a + b) < (precision * precision)

def get_actual_localization():
    localization = settings.runtime['localization']

    stored_localizations = database.get_localizations(main_tread=True)

    if stored_localizations != None:
        for stored_localization in stored_localizations:
            temp_localization = {
                'id': stored_localization[0],
                'latitude': stored_localization[1],
                'longitude': stored_localization[2]
            }

            if point_inside_circle(localization, temp_localization):
                return temp_location['id']

    return False

# TODO
def get_actual_event():
    actual_time = datetime.datetime.now()

    stored_events = database.get_events()



