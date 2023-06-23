import os
import tkinter as tk
from tkinter import messagebox
import json


config_file_path = os.environ['HOME'] + "/.ctxt_search-config.json"

class ConfigApp:
    def __init__(self, master):
        self.master = master
        master.title("Configurações")

        with open(config_file_path, "r") as file:
            self.config = json.load(file)

        listen_frame = tk.Frame(master)
        listen_frame.pack(fill=tk.X, expand=True)
        self.listen_label = tk.Label(listen_frame, text="Listen Paths (separated by comma)")
        self.listen_label.pack()
        self.listen_entry = tk.Entry(listen_frame)
        self.listen_entry.pack(fill=tk.X, expand=True)
        self.listen_entry.insert(0, ', '.join(self.config.get('listen', [])))

        checkbox_frame = tk.Frame(master)
        checkbox_frame.pack(fill=tk.X, expand=True)

        self.recursive_listening_var = tk.BooleanVar(value=self.config.get('recursive_listening', False))
        self.recursive_listening_check = tk.Checkbutton(checkbox_frame, text="Recursive Listening", variable=self.recursive_listening_var)
        self.recursive_listening_check.pack(side=tk.LEFT)

        self.ignore_hidden_var = tk.BooleanVar(value=self.config.get('ignore_hidden', False))
        self.ignore_hidden_check = tk.Checkbutton(checkbox_frame, text="Ignore Hidden", variable=self.ignore_hidden_var)
        self.ignore_hidden_check.pack(side=tk.LEFT)

        self.use_localization_var = tk.BooleanVar(value=self.config.get('use_localization', False))
        self.use_localization_check = tk.Checkbutton(checkbox_frame, text="Use Localization", variable=self.use_localization_var)
        self.use_localization_check.pack(side=tk.LEFT)

        self.use_time_mock_var = tk.BooleanVar(value=self.config.get('use_time_mock', False))
        self.use_time_mock_check = tk.Checkbutton(checkbox_frame, text="Use Time Mock", variable=self.use_time_mock_var)
        self.use_time_mock_check.pack(side=tk.LEFT)

        localization_frame = tk.Frame(master)
        localization_frame.pack(fill=tk.X, expand=True)

        self.localization_plugin_wait_time_label = tk.Label(localization_frame, text="Localization Plugin Wait Time")
        self.localization_plugin_wait_time_label.pack(side=tk.LEFT)
        self.localization_plugin_wait_time_entry = tk.Entry(localization_frame)
        self.localization_plugin_wait_time_entry.pack(fill=tk.X, expand=True, side=tk.LEFT)
        self.localization_plugin_wait_time_entry.insert(0, str(self.config.get('localization_plugin_wait_time', 0)))

        self.localization_precision_label = tk.Label(localization_frame, text="Localization Precision")
        self.localization_precision_label.pack(side=tk.LEFT)
        self.localization_precision_entry = tk.Entry(localization_frame)
        self.localization_precision_entry.pack(fill=tk.X, expand=True, side=tk.LEFT)
        self.localization_precision_entry.insert(0, str(self.config.get('localization_precision', 0)))

        path_frame = tk.Frame(master)
        path_frame.pack(fill=tk.X, expand=True)

        self.database_label = tk.Label(path_frame, text="Database Path")
        self.database_label.pack(side=tk.LEFT)
        self.database_entry = tk.Entry(path_frame)
        self.database_entry.pack(fill=tk.X, expand=True, side=tk.LEFT)
        self.database_entry.insert(0, self.config.get('database', ''))

        self.mountpoint_label = tk.Label(path_frame, text="Mountpoint Path")
        self.mountpoint_label.pack(side=tk.LEFT)
        self.mountpoint_entry = tk.Entry(path_frame)
        self.mountpoint_entry.pack(fill=tk.X, expand=True, side=tk.LEFT)
        self.mountpoint_entry.insert(0, self.config.get('mountpoint', ''))

        bottom_frame = tk.Frame(master)
        bottom_frame.pack(fill=tk.X, expand=True)

        self.event_dates_in_utc_var = tk.BooleanVar(value=self.config.get('event_dates_in_utc', False))
        self.event_dates_in_utc_check = tk.Checkbutton(bottom_frame, text="Event Dates in UTC", variable=self.event_dates_in_utc_var)
        self.event_dates_in_utc_check.pack(side=tk.LEFT)

        self.max_results_label = tk.Label(bottom_frame, text="Max Results")
        self.max_results_label.pack(side=tk.LEFT)
        self.max_results_entry = tk.Entry(bottom_frame)
        self.max_results_entry.pack(fill=tk.X, expand=True, side=tk.LEFT)
        self.max_results_entry.insert(0, str(self.config.get('max_results', 0)))

        self.save_button = tk.Button(master, text="Salvar Configurações", command=self.save_config)
        self.save_button.pack()

        self.show_button = tk.Button(master, text="Mostrar Configurações do Arquivo", command=self.show_config)
        self.show_button.pack()

    def save_config(self):
        self.config['listen'] = [path.strip() for path in self.listen_entry.get().split(',')]
        self.config['recursive_listening'] = self.recursive_listening_var.get()
        self.config['ignore_hidden'] = self.ignore_hidden_var.get()
        self.config['use_localization'] = self.use_localization_var.get()
        self.config['use_time_mock'] = self.use_time_mock_var.get()
        self.config['localization_plugin_wait_time'] = float(self.localization_plugin_wait_time_entry.get())
        self.config['localization_precision'] = float(self.localization_precision_entry.get())
        self.config['database'] = self.database_entry.get()
        self.config['mountpoint'] = self.mountpoint_entry.get()
        self.config['event_dates_in_utc'] = self.event_dates_in_utc_var.get()
        self.config['max_results'] = int(self.max_results_entry.get())
        
        with open(config_file_path, "w") as file:
            json.dump(self.config, file, indent=4)

    def show_config(self):
        with open(config_file_path, "r") as file:
            config = json.load(file)
        messagebox.showinfo("Configurações do Arquivo", json.dumps(config, indent=4))

def main():
    root = tk.Tk()
    root.geometry("800x600")
    app = ConfigApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
