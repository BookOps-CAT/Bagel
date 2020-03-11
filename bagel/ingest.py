from collections import namedtuple
import csv


Row = namedtuple('Row', [
    'processing',
    'title',
    'title_part',
    'players',
    'duration',
    'age',
    'central_barcodes',
    'crown_barcodes',
    'price',
    'title_other',
    'subtitle',
    'author',
    'isbn',
    'upc',
    'pub_place',
    'publisher',
    'pub_date',
    'desc',
    'content',
    'email'])


def lower_first_letter(string):
    try:
        string = string.strip()
        string = f'{string[0].lower()}{string[1:]}'
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
            string = string[:-1]
    else:
        string = ''

    return string


def str2list(string):
    return [i.strip() for i in string.split(';') if i.strip() != '']


def form_data_reader(fh):
    """
    Parses descripions from a csv file created from google sheet
    linked to submission form
    args:
        fh: str, csv file path
    yields: namedTuple, row of data
    """

    with open(fh, 'r') as csvfile:
        reader = csv.reader(csvfile)

        # skip header
        next(reader)

        for row in reader:
            # add regex validation?
            central_barcodes = str2list(row[7])
            crown_barcodes = str2list(row[8])
            title_other = str2list(row[10])
            isbn = str2list(row[13])
            upc = str2list(row[14])
            title = remove_white_space_and_trailing_punctuation(row[2])  # run regex to remove trailing periods
            title_other = lower_first_letter(row[10])
            desc = remove_white_space_and_trailing_punctuation(row[18])
            content = remove_white_space_and_trailing_punctuation(row[19])

            yield Row(
                processing=row[1],
                title=title,
                title_part=row[3].strip(),
                players=row[4].strip(),
                duration=row[5].strip(),
                age=row[6].strip(),
                central_barcodes=central_barcodes,
                crown_barcodes=crown_barcodes,
                price=f'{float(row[9].strip()):.2f}',
                title_other=title_other,
                subtitle=row[11].strip(),
                author=row[12].strip(),
                isbn=isbn,
                upc=upc,
                pub_place=row[15].strip(),
                publisher=row[16].strip(),
                pub_date=row[17].strip(),  # validation?
                desc=desc,
                content=row[19].strip(),
                email=row[20])
