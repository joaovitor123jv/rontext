#!/usr/bin/python3
import config_file_handler
import random
import math
import yaml
import settings

def _main():
    loaded_settings = config_file_handler.parseConfigFile()
    point = generatePoint()
    print(yaml.dump(point))

def generatePoint():
    if settings.loaded['use_mock']:
        raw_point = {
            'latitude': settings.loaded['mock']['actual_localization']['latitude'],
            'longitude': settings.loaded['mock']['actual_localization']['longitude']
        }

        radius = settings.loaded['mock']['precision']
        angle = 2 * math.pi * random.random()
        random_radius = radius * math.sqrt(random.random())

        return {
            'latitude': random_radius * math.cos(angle) + raw_point['latitude'],
            'longitude': random_radius * math.sin(angle) + raw_point['longitude']
        }

if __name__ == "__main__":
    _main()