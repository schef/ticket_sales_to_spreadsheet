import os
from pathlib import Path
import json
import datetime

def get_full_path(path):
    return os.path.realpath(os.path.expanduser(path))

def get_path_of_current_file(f):
    return str(Path(f).resolve().parent)

def write_json(filename, data):
    print(f"write_json start {filename}")
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"write_json end")

def get_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def write_seats_json(seats, show_name, download_path = "."):
    filename = f"{download_path}/{show_name}_{get_timestamp()}.json"
    fullpath = get_full_path(filename)
    write_json(fullpath, [s.dict() for s in seats])
