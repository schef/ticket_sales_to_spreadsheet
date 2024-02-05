#!/usr/bin/env python3

import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from ticket_sales_to_spreadsheet.seat import Seat
from ticket_sales_to_spreadsheet.common import write_seats_json

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

def download_seats_from_url(url):
    driver = get_driver(headless=True)
    open_url(driver, url)
    seats = get_seats(driver)
    driver.close()
    return seats

def run():
    url = input("Url: ")
    show_name = input("Show name: ")
    download_path = input("Download path: ")
    seats = download_seats_from_url(url)
    write_seats_json(seats, show_name, download_path)
    #from IPython import embed; embed()

if __name__ == "__main__":
    run()
