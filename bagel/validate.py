import csv
from datetime import datetime


def validate_headings():
    # read the headings of the csv and confirm they match the expected list of headings
    correct_headings = [
        "Timestamp",
        "Processing",
        "Title proper",
        "Name of part / expansion",
        "Number of players",
        "Game duration",
        "Recommended age",
        "Central Library Barcodes",
        "Crown Heights Barcodes",
        "Bushwick Barcodes",
        "McKinley Park Barcodes",
        "New Utrecht Barcodes",
        "Windsor Terrace Barcodes",
        "Price",
        "Other titles",
        "Subtitle",
        "Authors/designers",
        "ISBN",
        "UPC",
        "Place of publication",
        "Publisher",
        "Date of publication",
        "Description/summary",
        "List of components",
        "Email Address",
        "Adams St. Barcodes",
    ]
    with open("temp/metadata.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        csv_header = next(reader)
        try:
            assert csv_header == correct_headings
        except AssertionError:
            print("Spreadsheet headings do not match. Check csv and rerun script.")
            exit()


def validate_timestamps():
    # test validity of csv by tring to convert str in first column to a timestamp
    with open("temp/metadata.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for n, row in enumerate(reader):
            try:
                datetime.strptime(row[0], "%m/%d/%Y %H:%M:%S")
            except Exception:
                print(f"Invalid timestamp in row {n + 1}. Check csv and rerun script.")
                exit()


def validate_csv():
    validate_headings()
    validate_timestamps()
    print("Spreadsheet structure is valid.")
