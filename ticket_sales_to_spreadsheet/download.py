#!/usr/bin/env python3

import os
import json
import datetime
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from ticket_sales_to_spreadsheet.seat import Seat

DOWNLOADS_PATH = "./downloads"
BELA_FLECK_URL = "https://ulaznice.czk-cakovec.hr/Dvorana.php?i=9200&W=&b=T&statusID=0"
CHRIS_BOTTI_URL = "https://ulaznice.czk-cakovec.hr/Dvorana.php?i=9157&W=&b=T&statusID=0"

def get_driver(headless=False):
    print("get_driver")
    options = Options()
    os.environ['CLASS'] = 'selenium'
    if headless == True:
        os.environ['MOZ_HEADLESS'] = '1'
    driver = webdriver.Firefox(options=options)
    return driver

def open_url(driver, url):
    print(f"open_url start {url}")
    driver.get(url)
    print(f"open_url end {url}")

def get_seats(driver):
    print("get_seats start")
    seats = []
    elements = driver.find_elements(By.XPATH, "//div[@align='center']/*")
    for e in elements:
        id_text = e.get_attribute("id")
        if id_text.isdigit():
            id = int(id_text)
            if id >= 1 and id <= 558:
                occupied = "Z" in e.get_attribute("class")
                column = int(e.text)
                row = -1
                seats.append(Seat(id, row, column, occupied))
    seats = sorted(seats, key=lambda s: s.id)
    row = 1
    last_column = 0
    for seat in seats:
        if seat.column < last_column:
            row += 1
        last_column = seat.column
        seat.row = row
    print("get_seats end")
    return seats

def save_to_json(filename, data):
    print(f"save_to_json start {filename}")
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"save_to_json end")

def get_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

selection_url = {
    "1": BELA_FLECK_URL,
    "2": CHRIS_BOTTI_URL,
    "bela": BELA_FLECK_URL,
    "fleck": BELA_FLECK_URL,
    "chris": CHRIS_BOTTI_URL,
    "botti": CHRIS_BOTTI_URL,
    }

def get_url_by_name(name):
    try:
        url = selection_url[name]
    except:
        print("Selection not valid")
        sys.exit(1)
    return url

def download_seats_by_name(name):
    url = get_url_by_name(name)
    driver = get_driver(headless=True)
    open_url(driver, url)
    seats = get_seats(driver)
    if url == BELA_FLECK_URL:
        filename = "bela_fleck"
    elif url == CHRIS_BOTTI_URL:
        filename = "chris_botti"
    else:
        sys.exit(2)
    save_to_json(f"{DOWNLOADS_PATH}/{filename}_{get_timestamp()}.json", [s.dict() for s in seats])
    #from IPython import embed; embed()
    driver.close()

def run():
    if len(sys.argv) > 1:
        selection = sys.argv[1]
    else:
        print("[1] Bela Fleck")
        print("[2] Chris Botti")
        selection = input("Select index: ")
    download_seats_by_name(selection)

if __name__ == "__main__":
    run()
