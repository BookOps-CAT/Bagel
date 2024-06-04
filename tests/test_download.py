import csv
from bagel.download import get_metadata


def test_get_metadata(tmpdir):
    get_metadata(f"{tmpdir}/test.csv")
    reader = csv.reader(open(f"{tmpdir}/test.csv", "r"))
    header = next(reader)
    assert sorted(header) == sorted(
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
