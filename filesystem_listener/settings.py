import os

def init():
    global loaded
    loaded = {
        'listen': [
            os.environ['HOME']
        ],
        'recursive_listening': False,
        'ignore_hidden': True,
        'use_location': True,
        'ics_parser_bin': "",
        'use_agenda': True
    }

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
        'use_location': True,
        'location_bin': "/home/joaovitor/Documentos/UFG-CDC/PFC/PFC2/Sistema/localization/main.py",
        'ics_parser_bin': "/home/joaovitor/Documentos/UFG-CDC/PFC/PFC2/Sistema/ics_parser/main.rb",
        'use_agenda': True,
        'database': "/home/joaovitor/ctxt_search-database.db"
    }