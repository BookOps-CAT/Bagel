import pandas as pd

SHEET_ID = "1Z8kWlHZXbnzP7OQWK3nLy7DEdxedPv2pW2pYodh6_dY"
SHEET = "Form Responses 1"
SHEET_NAME = SHEET.replace(" ", "%20")
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"


def get_metadata():
    # download metadata from google sheet and save it as a csv
    df = pd.read_csv(
        URL,
        usecols=range(0, 25),
        converters={
            "Number of players": str,
            "Recommended age": str,
            "Date of publication": str,
            "Central Library Barcodes": str,
            "Crown Heights Barcodes": str,
            "Bushwick Barcodes": str,
            "McKinley Park Barcodes": str,
            "New Utrecht Barcodes": str,
            "Windsor Terrace Barcodes": str,
            "ISBN": str,
            "UPC": str,
            "Description/summary": lambda x: x.replace("\n", " "),
        },
    )
    df.to_csv("temp/metadata.csv", index=False)
