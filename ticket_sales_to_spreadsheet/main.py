from ticket_sales_to_spreadsheet.common import write_seats_json
from ticket_sales_to_spreadsheet.download_seats import download_seats_from_url
from ticket_sales_to_spreadsheet.diff_seats import get_diff_from_last_two_seats_by_show_name
from ticket_sales_to_spreadsheet.spreadsheet_seats import update_field_by_name, get_count
from ticket_sales_to_spreadsheet.credentials import show_names, download_path
from ticket_sales_to_spreadsheet.whatsapp import send
import time

def run():
    for show_name, url in show_names.items():
        seats = download_seats_from_url(url)
        write_seats_json(seats, show_name, download_path)
        diffs = get_diff_from_last_two_seats_by_show_name(show_name, download_path)
        for e,diff in enumerate(diffs):
            update_field_by_name(show_name, diff.row, diff.column, "1")
            if e % 10 == 9:
                print("sleep 60s for google api")
                time.sleep(60)
        if len(diffs) > 0:
            number = get_count(show_name)
            details = []
            for diff in diffs:
                details.append(f" - {int(diff.row):02d}:{int(diff.column):02d}")
            details_text = "\n".join(details)
            send(f"[BOT]: {show_name} = {number} (novih: {len(diffs)})\n{details_text}")

if __name__ == "__main__":
    run()
