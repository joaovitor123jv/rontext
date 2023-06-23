import os


def init():
    global loaded
    loaded = {}

    global runtime
    runtime = {}

    global default
    default = {
        'listen': [
            os.environ['HOME'],
            os.environ['HOME'] + "/Documentos",
            os.environ['HOME'] + "/Música",
            os.environ['HOME'] + "/Vídeos",
            os.environ['HOME'] + "/Imagens",
            os.environ['HOME'] + "/Downloads"
        ],
        'recursive_listening': False,
        'ignore_occurrences': [
            # Ignore all specified directories or files which contains defined substrings
            # If empty, listen all.
            # 'node_modules'
            '/.git/'
        ],
        # 'recursive_listening': True,
        'ignore_hidden': True,
        'use_localization': True,
        'use_time_mock': False,
        'localization_plugin_wait_time': 1, # Time, in seconds
        'localization_precision': 0.01, # Worst precision than the Mock, reduce the amount of stored localizations
        # 'localization_bin': os.environ['HOME'] + "/Documentos/UFG-CDC/PFC/PFC2/Sistema/localization/main.py",
        'localization_bin': os.path.dirname(os.path.abspath(__file__)) + '/../localization/main.py',
        'ics_parser_bin': os.path.dirname(os.path.abspath(__file__)) + '/../ics_parser/main.rb',
        # 'ics_parser_bin': os.environ['HOME'] + "/Documentos/UFG-CDC/PFC/PFC2/Sistema/ics_parser/main.rb",
        'use_agenda': True,
        'database': os.environ['HOME'] + "/.ctxt_search-database.db",
        'mountpoint': os.environ['HOME'] + "/Rontext/",
        'event_dates_in_utc': False,
        'max_results': 20
    }


def add_runtime(name, data):
    global runtime
    runtime[name] = data


def set(name, data):
    add_runtime(name, data)
