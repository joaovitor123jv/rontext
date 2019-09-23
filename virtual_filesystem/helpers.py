from io import StringIO
import yaml

def point_inside_circle(point, circle, settings):
    a = (point["latitude"] - circle["latitude"]) * (point["latitude"] - circle["latitude"])
    b = (point["longitude"] - circle["longitude"]) * (point["longitude"] - circle["longitude"])
    precision = float(settings.loaded["localization_precision"])
    return (a + b) < (precision * precision)

def parse_yaml_string(string):
    fd = StringIO(string) # Cria um 'arquivo' em memória
    return yaml.load(fd, Loader=yaml.Loader) # Faz o parse do yaml

