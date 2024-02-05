import json
import os
from ticket_sales_to_spreadsheet.common import read_seats_from_json, get_show_name_files

def diff_two_seats(seats1, seats2):
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

def diff_last_two_files(show_name_files):
    diff = []
    if len(show_name_files) >= 2:
        show_name_files.sort(reverse = True)
        seat2 = read_seats_from_json(show_name_files[0])
        seat1 = read_seats_from_json(show_name_files[1])
        diff = diff_two_seats(seat1, seat2)
    else:
        print("[DIFF]: Error, only one file")
    return diff

def get_diff_from_last_two_seats_by_show_name(show_name, download_path):
    show_name_files = get_show_name_files(show_name, download_path)
    return diff_last_two_files(show_name_files)

def run():
    show_name = input("Show name: ")
    directory_path = input("Directory path: ")
    get_diff_from_last_two_seats_by_show_name(show_name, directory_path)

if __name__ == "__main__":
    run()
