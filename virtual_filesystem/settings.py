import os
import json


class Settings:
    def __init__(self):
        self.loaded = {}
        self.runtime = {}
        self.config_file_path = os.environ['HOME'] + "/.ctxt_search-config.json"

        if(os.path.isfile(self.config_file_path)):
            with open(self.config_file_path, "r") as stream:
                try:
                    self.loaded = json.load(stream)
                    self.runtime = {}

                except json.JSONDecodeError as exc:
                    print(exc)

        else:
            print("[VFS]: File {} doesn't exists aborting".format(self.config_file_path))
            exit(1)


    def add_runtime(self, name, data):
        self.runtime[name] = data

