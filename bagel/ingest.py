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
            central_barcodes = [b.strip() for b in row[7].split(';') if b.strip() != '']
            crown_barcodes = [b.strip() for b in row[8].split(';') if b.strip() != '']
            title_other = [t.strip() for t in row[10].split(';') if t.strip() != '']
            isbn = [i.strip() for i in row[13].split(';') if i.strip() != '']
            upc = [u.strip() for u in row[14].split(';') if u.strip() != '']
            title = row[2].strip()  # run regex to remove trailing periods

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
                desc=row[18].strip(),
                content=row[19].strip(),
                email=row[20])
