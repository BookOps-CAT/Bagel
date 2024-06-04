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
            "Number of players": lambda x: str(x),
            "Recommended age": lambda x: str(x),
            "Date of publication": lambda x: str(x),
            "Central Library Barcodes": lambda x: str(x),
            "Crown Heights Barcodes": lambda x: str(x),
            "Bushwick Barcodes": lambda x: str(x),
            "McKinley Park Barcodes": lambda x: str(x),
            "New Utrecht Barcodes": lambda x: str(x),
            "Windsor Terrace Barcodes": lambda x: str(x),
            "ISBN": lambda x: str(x),
            "UPC": lambda x: str(x),
            "Description/summary": lambda x: x.replace("\n", " "),
        },
    )
    df.to_csv(outfile, index=False)
    return outfile
