import csv
import datetime


def validate_headings(file: str) -> bool:
    """
    Read the headings of the csv and confirm they match the expected list of headings
    Args:
        file: path to csv file as a str
    Returns:
        whether or not the headings validate
    """
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
    with open(file, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        csv_header = next(reader)
        if csv_header == correct_headings:
            return True
        else:
            print("Spreadsheet headings do not match. Check csv and rerun script.")
            return False


def validate_timestamps(file: str) -> bool:
    """
    Test validity of csv by tring to convert str in first column to a timestamp
    Args:
        file: path to csv file as a str
    Returns:
        whether or not the timestamps validate
    """
    with open(file, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for n, row in enumerate(reader):
            try:
                datetime.datetime.strptime(row[0], "%m/%d/%Y %H:%M:%S")
                valid = True
            except ValueError:
                print(f"Invalid timestamp in row {n + 1}. Check csv and rerun script.")
                valid = False
    return valid


def validate_csv(file: str) -> bool:
    """
    Test validity of csv by validating headings and timestamps
    Args:
        file: path to csv file as a str
    Returns:
        whether or not the csv validates
    """
    headings = validate_headings(file)
    timestamps = validate_timestamps(file)
    print("Spreadsheet structure is valid.")
    if headings is True and timestamps is True:
        return True
    else:
        return False
