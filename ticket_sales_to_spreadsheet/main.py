from ticket_sales_to_spreadsheet.download import download_seats_by_name
from ticket_sales_to_spreadsheet.compare import compare_last_two_seats_by_name
from ticket_sales_to_spreadsheet.online import update_field_by_name

def run():
    for name in ["bela", "botti"]:
        download_seats_by_name(name)
        diffs = compare_last_two_seats_by_name(name)
        for diff in diffs:
            update_field_by_name(name, diff.row, diff.column, "1")

if __name__ == "__main__":
    run()
