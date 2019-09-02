import os

def init():
    global loaded
    loaded = {}

    global runtime
    runtime = {}

    global default
    default = {
        'listen': [
            os.environ['HOME'] + "/Documentos",
            os.environ['HOME'] + "/Música",
            os.environ['HOME'] + "/Vídeos",
            os.environ['HOME'] + "/Imagens",
            os.environ['HOME'] + "/Downloads",
            os.environ['HOME']
        ],
        'recursive_listening': False,
        'ignore_hidden': True,
        'use_localization': True,
        'use_time_mock': False,
        'localization_plugin_wait_time': 1, # Time, in seconds
        'localization_precision': 0.01, # Worst precision than the Mock, reduce the amount of stored localizations
        'localization_bin': "/home/joaovitor/Documentos/UFG-CDC/PFC/PFC2/Sistema/localization/main.py",
        'ics_parser_bin': "/home/joaovitor/Documentos/UFG-CDC/PFC/PFC2/Sistema/ics_parser/main.rb",
        'use_agenda': True,
        'database': "/home/joaovitor/ctxt_search-database.db",
        'mountpoint': "/home/joaovitor/Rontext/"
    }

def add_runtime(name, data):
    global runtime
    runtime[name] = data
