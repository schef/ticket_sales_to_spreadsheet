import json
import glob, os
from ticket_sales_to_spreadsheet.seat import Seat
import sys

DOWNLOAD_PATH = "./downloads"
BELA_FLECK = "bela_fleck"
CHRIS_BOTTI = "chris_botti"

def get_seats_from_filename(filename):
    seats = []
    with open(filename) as user_file:
        content = user_file.read()
        json_obj = json.loads(content)
        for seat in json_obj:
            seats.append(Seat(**seat))
        return seats

def get_downladed_files(key):
    files = []
    oldpwd = os.getcwd()
    os.chdir(DOWNLOAD_PATH)
    for file in glob.glob("*.json"):
        if key in file:
            files.append(f"./{DOWNLOAD_PATH}/{file}")
    os.chdir(oldpwd)
    return files

def compare_two_seats(seats1, seats2):
    diff1 = []
    diff2 = []
    for i in range(len(seats1)):
        seat1 = seats1[i]
        seat2 = seats2[i]
        if seat1 != seat2:
            diff1.append(seat1)
            diff2.append(seat2)
    if len(diff1) > 0:
        for i in range(len(diff1)):
            seat1 = diff1[i]
            seat2 = diff2[i]
            print(f"[DIFF] {seat2}")
    return diff2

def compare_last_two_files(downloads):
    diff = []
    if len(downloads) >= 2:
        downloads.sort(reverse = True)
        seat2 = get_seats_from_filename(downloads[0])
        seat1 = get_seats_from_filename(downloads[1])
        diff = compare_two_seats(seat1, seat2)
    else:
        print("[DIFF]: Error, only one file")
    return diff

selection_name = {
    "1": BELA_FLECK,
    "2": CHRIS_BOTTI,
    "bela": BELA_FLECK,
    "fleck": BELA_FLECK,
    "chris": CHRIS_BOTTI,
    "botti": CHRIS_BOTTI,
    }

def compare_last_two_seats_by_name(name):
    try:
        name = selection_name[name]
    except:
        print("Selection not valid")
        sys.exit(1)

    downloads = get_downladed_files(name)
    return compare_last_two_files(downloads)

def run():
    if len(sys.argv) > 1:
        selection = sys.argv[1]
    else:
        print("[1] Bela Fleck")
        print("[2] Chris Botti")
        selection = input("Select index: ")

    compare_last_two_seats_by_name(selection)


if __name__ == "__main__":
    run()


