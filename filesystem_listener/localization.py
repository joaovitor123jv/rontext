from io import StringIO
import time
import yaml
import threading
import subprocess
import settings

def parse_yaml_string(string):
    fd = StringIO(string) # Cria um 'arquivo' em memória
    return yaml.load(fd) # Faz o parse do yaml

def listener():
    while True:
        return_data = subprocess.run([settings.loaded['localization_bin']], stdout=subprocess.PIPE)
        parsed_return = parse_yaml_string(return_data.stdout.decode('utf8'))

        settings.add_runtime('localization', parsed_return)

        print("LOCALIZATION == ", settings.runtime['localization'])

        time.sleep(settings.loaded['localization_plugin_wait_time']) # Waits 1 second till the next localization check

def start_plugin():
    try:
        thread = threading.Thread(target=listener)
        thread.start()

    except:
        print("Failed to start localization plugin")