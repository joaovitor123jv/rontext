import _thread
import time
import settings

def listener():
    while True:
        return_data = subprocess.run([settings.loaded['localization'], file], stdout=subprocess.PIPE)
        parsed_return = parse_yaml_string(return_data.stdout.decode('utf8'))

        settings.runtime['localization'] = parsed_return

        time.sleep(settings.loaded['localization']) # Waits 1 second till the next localization check

def start_plugin():
    print("Starting localization plugin")

    try:
        _thread.start_new_thread(listener)
    
    except:
        print("Failed to start localization plugin")