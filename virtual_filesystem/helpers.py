from io import StringIO
import yaml
import datetime
import time

def point_inside_circle(point, circle, settings):
    a = (point["latitude"] - circle["latitude"]) * (point["latitude"] - circle["latitude"])
    b = (point["longitude"] - circle["longitude"]) * (point["longitude"] - circle["longitude"])
    precision = float(settings.loaded["localization_precision"])
    return (a + b) < (precision * precision)

def parse_yaml_string(string):
    fd = StringIO(string) # Create an 'in-memory' file
    return yaml.load(fd, Loader=yaml.Loader) # Do the yaml parse

def get_date_from_event(event_date, settings=None):
    if (settings == None) or (not settings.loaded['event_dates_in_utc']):
        return datetime.datetime.strptime(event_date, '%Y-%m-%d %H:%M:%S')
    else:
        now_timestamp = time.time()
        offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
        return (datetime.datetime.strptime(event_date, '%Y-%m-%d %H:%M:%S') + offset)
