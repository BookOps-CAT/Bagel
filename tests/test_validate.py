import csv
from bagel.validate import validate_headings, validate_timestamps, validate_csv


def test_validate_headings():
    valid_headings = validate_headings("temp/metadata.csv")
    assert valid_headings is True


def test_validate_headings_errors(tmpdir):
    with open(f"{tmpdir}/heading_errors.csv", "w") as csvfile:
        writer = csv.writer(
            csvfile,
            delimiter=",",
            lineterminator="\n",
        )
        writer.writerow(["Timestamp", "Processing", "Title proper"])
    valid_headings = validate_headings(f"{tmpdir}/heading_errors.csv")
    assert valid_headings is False


def test_validate_timestamps():
    valid_timestamps = validate_timestamps("temp/metadata.csv")
    assert valid_timestamps is True


def test_validate_timestamp_errors(tmpdir):
    with open(f"{tmpdir}/timestamp_errors.csv", "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=",", lineterminator="\n")
        writer.writerow(
            [
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
        )
        writer.writerow(
            [
                "Foo",
            ]
        )
    valid_timestamps = validate_timestamps(f"{tmpdir}/timestamp_errors.csv")
    assert valid_timestamps is False


def test_validate_csv():
    valid_csv = validate_csv("temp/metadata.csv")
    assert valid_csv is True


def test_validate_csv_errors(tmpdir):
    with open(f"{tmpdir}/invalid.csv", "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=",", lineterminator="\n")
        writer.writerow(
            [
                "Date of publication",
                "Description/summary",
                "List of components",
                "Email Address",
                "Adams St. Barcodes",
            ]
        )
        writer.writerow(
            [
                "Foo",
            ]
        )
    valid_csv = validate_csv(f"{tmpdir}/invalid.csv")
    assert valid_csv is False
