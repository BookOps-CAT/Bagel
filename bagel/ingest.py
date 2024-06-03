from collections import namedtuple
import csv


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


def lower_first_letter(string):
    try:
        string = string.strip()
        string = f"{string[0].lower()}{string[1:]}"
    except IndexError:
        string = string
    except AttributeError:
        string = str(string)
    return string


def has_alphanumeric_last(string=None):
    try:
        return string[-1].isalnum()
    except AttributeError:
        raise
    except TypeError:
        raise
    except IndexError:
        raise


def remove_left_white_space(string=None):
    try:
        return string.lstrip()
    except AttributeError:
        raise


def remove_white_space_and_trailing_punctuation(string):
    if string:
        string = remove_left_white_space(string)
        while has_alphanumeric_last(string) is False:
            if string[-1] not in (")", "!", "?"):
                string = string[:-1]
            else:
                break
    else:
        string = ""

    return string


def str2list(string):
    return [i.strip() for i in string.split(";") if i.strip() != ""]


def form_data_reader():
    """
    Parses descripions from a csv file created from google sheet
    linked to submission form
    args:
        fh: str, csv file path
    yields: namedTuple, row of data
    """

    with open("temp/metadata.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)

        # skip header
        next(reader)

        for n, row in enumerate(reader):
            # add regex validation?
            try:
                central_barcodes = str2list(row[7])
                crown_barcodes = str2list(row[8])
                bushwick_barcodes = str2list(row[9])
                mckinley_barcodes = str2list(row[10])
                newutrecht_barcodes = str2list(row[11])
                windsor_barcodes = str2list(row[12])
                adams_st_barcodes = str2list(row[25])
                isbns = str2list(row[17])
                upcs = str2list(row[18])
                title = remove_white_space_and_trailing_punctuation(
                    row[2]
                )  # run regex to remove trailing periods
                subtitle = remove_white_space_and_trailing_punctuation(row[15])
                title_other = str2list(row[14])
                desc = remove_white_space_and_trailing_punctuation(row[22])
                content = remove_white_space_and_trailing_punctuation(row[23])

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
                    pub_date=row[21].strip(),  # validation?
                    desc=desc,
                    content=content,
                    email=row[24],
                    adams_st_barcodes=adams_st_barcodes,
                )
            except Exception:
                print(f"Encountered a problem in row {n + 1}")
                raise
