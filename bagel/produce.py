from datetime import date, datetime

from pymarc import Field, Record


def generate_control_no(start, end):
    pass


def check_article(title):
    # article check
    ind2 = '0'
    if title[:4].lower() == 'the ':
        ind2 = '4'
    elif title[:3].lower() == 'an ':
        ind2 = '3'
    elif title[:2].lower() == 'a ':
        ind2 = '2'

    return ind2


def save2marc(record, fh_out):
    """Appends MARC21 record to a file"""
    with open(fh_out, 'ab') as out:
        out.write(record.as_marc())


def game_record(data, control_number):
    """
    Creates a record object from data namedtuple
    args:
        data: namedtuple
    returns:
        record: pymarc.Record object
    """

    record = Record()
    record.leader = '00000crm a2200000M  4500'

    tags = []

    # 001 - control field
    tags.append(
        Field(
            tag='001',
            data=control_number))

    # 005
    tags.append(
        Field(
            tag='005',
            data=datetime.strftime(datetime.now(), '%y%m%d%H%M%S.%f')))

    # 008
    date_created = date.strftime(date.today(), '%y%m%d')
    if data.pub_date:
        t008 = f'{date_created}s{data.pub_date}    xxu               vneng d'
    else:
        t008 = f'{date_created}n        xxu               vneng d'
    tags.append(
        Field(
            tag='008',
            data=t008))

    # 020
    for isbn in data.isbn:
        tags.append(
            Field(
                tag='020',
                indicators=[' ', ' '],
                subfields=['a', isbn]))

    # 024
    for upc in data.upc:
        tags.append(
            Field(
                tag='024',
                indicators=['1', ' '],
                subfields=['a', upc]))

    # 040
    tags.append(
        Field(
            tag='040',
            indicators=[' ', ' '],
            subfields=['a', 'BKL', 'b', 'eng', 'e', 'rda', 'c', 'BKL']))

    # 099
    tags.append(
        Field(
            tag='099',
            indicators=[' ', ' '],
            subfields=['a', 'BOARD GAME']))

    # 245 (no final puctuation neeeded per new PCC ISBD policy)
    subfields = []
    if not data.title:
        raise ValueError('Missing title data')
    else:
        subfields.extend(['a', data.title])

    if data.subtitle:
        subfields[-1] = f'{subfields[-1]} : '
        subfields.extend('b', data.subtitle)

    if data.title_part:
        subfields[-1] = f'{subfields[-1]}. '
        subfields.extend(['p', data.title_part])

        # add 246 tag
        ind2 = check_article(data.title_part)
        tags.append(
            Field(
                tag='246',
                indicators=['1', ind2],
                subfields=['a', data.title_part[int(ind2):]]))

    if data.author:
        subfields[-1] = f'{subfields[-1]} / '
        subfields.extend(['c', data.author])

    ind2 = check_article(data.title)

    tags.append(
        Field(
            tag='245',
            indicators=['0', ind2],
            subfields=subfields))

    # 246 - other title
    for title in data.title_other:
        tags.append(
            Field(
                tag='246',
                indicators=['1', '3'],
                subfields=['a', data.title_other]))

    # 264 publication tags
    subfields = []
    if data.pub_place:
        subfields.extend(['a', f'{data.pub_place}:'])
    else:
        subfields.extend(['a', '[Place of publication not identified]:'])
    if data.publisher:
        subfields.extend(['b', f'{data.publisher},'])
    else:
        subfields.extend(['b', '[publisher not identified],'])
    if data.pub_date:
        subfields.extend(['c', data.pub_date])
    else:
        subfields.extend(['c', '[date of publication not identified]'])

    tags.append(
        Field(
            tag='264',
            indicators=[' ', '1'],
            subfields=subfields))

    # 300 tag
    tags.append(
        Field(
            tag='300',
            indicators=[' ', ' '],
            subfields=['a', '1 board game']))

    # RDA 3xx tags
    tags.append(
        Field(
            tag='336',
            indicators=[' ', ' '],
            subfields=[
                'a', 'three-dimansional form', 'b', 'tdf', '2', 'rdacontent']))
    tags.append(
        Field(
            tag='337',
            indicators=[' ', ' '],
            subfields=['a', 'unmediated', 'b', 'n', '2', 'rdamedia']))
    tags.append(
        Field(
            tag='338',
            indicators=[' ', ' '],
            subfields=['a', 'object', 'b', 'nr', '2', 'rdacarrier']))

    # 500 notes
    tags.append(
        Field(
            tag='500',
            indicators=[' ', ' '],
            subfields=['a', f'Number of players: {data.players}']))

    tags.append(
        Field(
            tag='500',
            indicators=[' ', ' '],
            subfields=['a', f'Game duration: {data.duration}']))

    # 520 summary
    if data.desc:
        tags.append(
            Field(
                tag='520',
                indicators=[' ', ' '],
                subfields=['a', data.desc]))

    # 521 note
    tags.append(
        Field(
            tag='521',
            indicators=[' ', ' '],
            subfields=['a', data.age]))

    # 655 genre
    tags.append(
        Field(
            tag='655',
            indicators=[' ', '7'],
            subfields=['a', 'Board games.', '2', 'lcgft']))

    # 856 fields (link to project)
    tags.append(
        Field(
            tag='856',
            indicators=['4', ' '],
            subfields=[
                'u', 'https://www.bklynlibrary.org/boardgamelibrary',
                'z', 'Board Game Library website']))

    # 960 item field
    for barcode in data.central_barcodes:
        subfields = [
            'i', barcode,
            'l', '02abg',
            'p', data.price,
            'q', '11',
            't', '53',
            'r', 'i',
            's', 'g'
        ]
        if data.item_msg:
            subfields.extend(['m', data.item_msg])

        tags.append(
            Field(
                tag='960',
                indicators=[' ', ' '],
                subfields=subfields))

    print(len(data.crown_barcodes), f'"{data.crown_barcodes}"')
    for barcode in data.crown_barcodes:
        subfields = [
            'i', barcode,
            'l', '30abg',
            'p', data.price,
            'q', '11',
            't', '53',
            'r', 'i',
            's', 'g'
        ]
        if data.item_msg:
            subfields.extend(['m', data.item_msg])

        tags.append(
            Field(
                tag='960',
                indicators=[' ', ' '],
                subfields=subfields))

    # 949 command line
    tags.append(
        Field(
            tag='949',
            indicators=[' ', ' '],
            subfields=['a', '*b2=o']))

    for tag in tags:
        record.add_ordered_field(tag)

    return record
