from oauth2client.service_account import ServiceAccountCredentials
import gspread
from ticket_sales_to_spreadsheet.credentials import spreahsheet_key_json_filename, spreahsheet_url

start_cell = None
ignore_cell = None

def get_spreadsheet_by_url(url):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(spreahsheet_key_json_filename, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_url(url)
    return spreadsheet

def get_sheet_by_name(spreadsheet, name):
    for worksheet in spreadsheet.worksheets():
        name_parts = name.split("_")
        if name_parts[0] in worksheet.title.lower():
            return worksheet
    return None

def get_cell(sheet, row, column):
    global start_cell, ignore_cell
    if start_cell is None:
        start_cell = sheet.acell('AP3')
    if ignore_cell is None:
        ignore_cell = sheet.acell('AP18')
    new_row = start_cell.row - 1 + row
    new_column = start_cell.col + 1 - column
    if new_row >= ignore_cell.row:
        new_row += 1
    return sheet.cell(new_row, new_column)

def format_cell(sheet, cell, clear = False):
    format = {}
    format["textFormat"] = {}
    format["textFormat"]["foregroundColor"] = {}
    if clear is not True:
        format["textFormat"]["foregroundColor"]["red"] = 255/255
        format["textFormat"]["foregroundColor"]["green"] = 0/255
        format["textFormat"]["foregroundColor"]["blue"] = 255/255
    else:
        format["textFormat"]["foregroundColor"]["red"] = 0/255
        format["textFormat"]["foregroundColor"]["green"] = 0/255
        format["textFormat"]["foregroundColor"]["blue"] = 0/255
    sheet.format(cell.address, format)

def update_cell(sheet, cell, text):
    sheet.update_cell(cell.row, cell.col, value=text)

def update_field_by_name(sheet_name, row, column, text, check_diff=False):
    print(f"[UPDATE]: {sheet_name}, {row}:{column} = {text}")
    row = int(row)
    column = int(column)
    spreadsheet = get_spreadsheet_by_url(spreahsheet_url)
    sheet = get_sheet_by_name(spreadsheet, sheet_name)
    cell = get_cell(sheet, row, column)
    if check_diff:
        if cell.value != text:
            print(f"[UPDATE]: check_diff {sheet_name}, {row}:{column} = {text}")
            if len(text) == 0:
                update_cell(sheet, cell, "")
                format_cell(sheet, cell, clear=True)
            else:
                update_cell(sheet, cell, "1")
                format_cell(sheet, cell)
    else:
        if len(text) == 0:
            update_cell(sheet, cell, "")
            format_cell(sheet, cell, clear=True)
        else:
            update_cell(sheet, cell, "1")
            format_cell(sheet, cell)

def get_count(sheet_name):
    spreadsheet = get_spreadsheet_by_url(spreahsheet_url)
    sheet = get_sheet_by_name(spreadsheet, sheet_name)
    return sheet.acell('AQ22').value

def run():
    row = int(input("Insert row: "))
    column = int(input("Insert col: "))
    text = input("Insert text: ")
    update_field_by_name("test", row, column, text)
    #from IPython import embed; embed()


if __name__ == "__main__":
    run()
