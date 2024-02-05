import os
from pathlib import Path
import json
import datetime
from ticket_sales_to_spreadsheet.seat import Seat

def get_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def get_full_path(path):
    return os.path.realpath(os.path.expanduser(path))

def get_path_of_current_file(f):
    return str(Path(f).resolve().parent)

def write_json(filename, data):
    print(f"write_json start {filename}")
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"write_json end")

def write_seats_json(seats, show_name, download_path = "."):
    print(f"write_seats_json start {show_name}, {download_path}")
    filename = f"{show_name}_{get_timestamp()}.json"
    path = f"{download_path}/{filename}"
    write_json(path, [s.dict() for s in seats])
    print(f"write_seats_json end")

def read_seats_from_json(filename):
    print(f"read_seats_from_json {filename}")
    seats = []
    with open(filename) as user_file:
        content = user_file.read()
        json_obj = json.loads(content)
        for seat in json_obj:
            seats.append(Seat(**seat))
        return seats

def get_show_name_files(show_name, download_path):
    print(f"get_show_name_files {show_name}, {download_path}")
    files = []
    for file in os.listdir(download_path):
        if file.startswith(show_name) and file.endswith(".json"):
            files.append(os.path.join(download_path, file))
    return files

if __name__ == "__main__":
    import credentials
    print(get_path_of_current_file(__file__))



