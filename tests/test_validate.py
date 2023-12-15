import csv
from datetime import datetime


def test_validate_headings():
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
    ]
    with open("temp/metadata.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        csv_header = next(reader)
        assert csv_header == correct_headings


def test_validate_timestamps():
    with open("temp/metadata.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            timestamp = datetime.strptime(row[0], "%m/%d/%Y %H:%M:%S")
            assert type(timestamp) is datetime
