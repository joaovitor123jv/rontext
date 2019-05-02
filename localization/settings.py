import os

def init():
    global loaded
    loaded = {}

    global runtime
    runtime = {}

    global default
    default = {
        'use_mock': True,
        'mock': {
            'actual_localization': {
                'latitude': 50.21, # RANGE: -90 ~ 90
                'longitude': -51.11 # RANGE: -180 ~ 180
            },
            'precision': 0.001 # In decimal degrees (see table below). Precision relative to neighborhood, street
        }
    }

#       REFERENCE: Decimal degrees -> precision at equator -> precision at 23N/S (mexico, cuba...)
#       1.0                             111.32km                        102.47km
#       0.1                             11.132km                        10.247km
#       0.01                            1.1132km                        1.0247km
#       0.001                           111.32m                         102.47m