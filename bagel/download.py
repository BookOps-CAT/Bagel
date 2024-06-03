import pandas as pd


SHEET = "https://docs.google.com/spreadsheets/d/"
SHEET_ID = "1Z8kWlHZXbnzP7OQWK3nLy7DEdxedPv2pW2pYodh6_dY"
SHEET_NAME = "Form Responses 1".replace(" ", "%20")
URL = f"{SHEET}{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"


def get_metadata(outfile: str) -> str:
    """
    Download metadata from google sheet and save it as a csv
    Args:
        outfile: name of csv file to save google sheet data to

    Returns:
        name of outfile as a str
    """
    df = pd.read_csv(
        URL,
        usecols=range(0, 26),
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
            "Description/summary": lambda x: str(x.replace("\n", " ")),
        },
    )
    df.to_csv(outfile, index=False)
    return outfile
