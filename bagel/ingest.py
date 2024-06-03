import csv
from typing import Generator
from collections import namedtuple

Row = namedtuple(
    "Row",
    [
        "processing",
        "title",
        "title_part",
        "players",
        "duration",
        "age",
        "central_barcodes",
        "crown_barcodes",
        "bushwick_barcodes",
        "mckinley_barcodes",
        "newutrecht_barcodes",
        "windsor_barcodes",
        "price",
        "title_other",
        "subtitle",
        "author",
        "isbn",
        "upc",
        "pub_place",
        "publisher",
        "pub_date",
        "desc",
        "content",
        "email",
        "adams_st_barcodes",
    ],
)


def trim_string(string: str) -> str:
    """trim whitespace and remove trailing punctuation"""
    if string:
        string = string.strip()
        if string.endswith(")") | string.endswith("!") | string.endswith("?"):
            return string
        elif string.endswith(".") | string.endswith(",") | string.endswith(";"):
            return string[:-1].strip()
        else:
            return string
    else:
        return ""


def str2list(string: str) -> list:
    return [i.strip() for i in string.split(";") if i.strip() != ""]


def form_data_reader(file: str) -> Generator:
    """
    Parses descripions from a csv file created from google sheet
    linked to submission form
    args:
        file: str, csv file path

    yields:
        namedTuple, row of data
    """

    with open(file, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)

        # skip header
        next(reader)

        for row in reader:
            central_barcodes = str2list(row[7])
            crown_barcodes = str2list(row[8])
            bushwick_barcodes = str2list(row[9])
            mckinley_barcodes = str2list(row[10])
            newutrecht_barcodes = str2list(row[11])
            windsor_barcodes = str2list(row[12])
            adams_st_barcodes = str2list(row[25])
            isbns = str2list(row[17])
            upcs = str2list(row[18])
            title = trim_string(row[2])
            subtitle = trim_string(row[15])
            title_other = str2list(row[14])
            desc = trim_string(row[22])
            content = trim_string(row[23])

            yield Row(
                processing=row[1],
                title=title,
                title_part=row[3].strip(),
                players=row[4].strip(),
                duration=row[5].strip(),
                age=row[6].strip(),
                central_barcodes=central_barcodes,
                crown_barcodes=crown_barcodes,
                bushwick_barcodes=bushwick_barcodes,
                mckinley_barcodes=mckinley_barcodes,
                newutrecht_barcodes=newutrecht_barcodes,
                windsor_barcodes=windsor_barcodes,
                price=f"{float(row[13].strip()):.2f}",
                title_other=title_other,
                subtitle=subtitle,
                author=row[16].strip(),
                isbn=isbns,
                upc=upcs,
                pub_place=row[19].strip(),
                publisher=row[20].strip(),
                pub_date=row[21].strip(),
                desc=desc,
                content=content,
                email=row[24],
                adams_st_barcodes=adams_st_barcodes,
            )
