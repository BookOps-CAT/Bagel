import datetime

from pymarc import Field, Record, Subfield


def create_item_field(shelfcode, barcode, price, status_code):
    """
    Creates item MARC tag subfields
    """
    return Field(
        tag="960",
        indicators=[" ", " "],
        subfields=[
            Subfield(code="i", value=barcode),
            Subfield(code="l", value=shelfcode),
            Subfield(code="p", value=price),
            Subfield(code="q", value="11"),
            Subfield(code="t", value="53"),
            Subfield(code="r", value="i"),
            Subfield(code="s", value=status_code),
        ],
    )


def generate_controlNo(sequence_no):
    sequence_no = str(sequence_no).zfill(7)
    return f"bkl-bgm-{sequence_no}"


def check_article(title):
    # article check
    ind2 = "0"
    if title[:4].lower() == "the ":
        ind2 = "4"
    elif title[:3].lower() == "an ":
        ind2 = "3"
    elif title[:2].lower() == "a ":
        ind2 = "2"

    return ind2


def save2marc(record, fh_out):
    """Appends MARC21 record to a file"""
    with open(fh_out, "ab") as out:
        out.write(record.as_marc())


def game_record(data, control_number, suppressed=True, status_code="-"):
    """
    Creates a record object from data namedtuple
    args:
        data: namedtuple
    returns:
        record: pymarc.Record object
    """
    today = datetime.datetime.now(tz=datetime.timezone.utc)

    record = Record()
    record.leader = "00000crm a2200000M  4500"

    # 001 - control field
    record.add_ordered_field(Field(tag="001", data=control_number))

    # 005
    record.add_ordered_field(
        Field(
            tag="005",
            data=datetime.datetime.strftime(today, "%Y%m%d%H%M%S.%f"),
        )
    )

    # 008
    date_created = datetime.date.strftime(today, "%y%m%d")
    if data.pub_date:
        t008 = f"{date_created}s{data.pub_date}    xxu               vneng d"
    else:
        t008 = f"{date_created}n        xxu               vneng d"
    record.add_ordered_field(Field(tag="008", data=t008))

    # 020
    for isbn in data.isbn:
        record.add_ordered_field(
            Field(
                tag="020",
                indicators=[" ", " "],
                subfields=[Subfield(code="a", value=isbn)],
            )
        )

    # 024
    for upc in data.upc:
        record.add_ordered_field(
            Field(
                tag="024",
                indicators=["1", " "],
                subfields=[Subfield(code="a", value=upc)],
            )
        )

    # 040
    record.add_ordered_field(
        Field(
            tag="040",
            indicators=[" ", " "],
            subfields=[
                Subfield(code="a", value="BKL"),
                Subfield(code="b", value="eng"),
                Subfield(code="e", value="rda"),
                Subfield(code="c", value="BKL"),
            ],
        )
    )

    # 099
    record.add_ordered_field(
        Field(
            tag="099",
            indicators=[" ", " "],
            subfields=[Subfield(code="a", value="BOARD GAME")],
        )
    )

    # 245 (no final puctuation neeeded per new PCC ISBD policy)
    if not data.title:
        raise ValueError("Missing title data")
    title = {"a": data.title, "b": data.subtitle, "c": data.author}
    if data.subtitle:
        title["a"] = f"{title['a']}:"
    if data.subtitle and data.author:
        title["b"] = f"{title['b']}/"
    if data.author and not data.subtitle:
        title["a"] = f"{title['a']}/"
    title_ind2 = check_article(data.title)
    title_subfields = [Subfield(code=k, value=v) for k, v in title.items() if v]
    record.add_ordered_field(
        Field(tag="245", indicators=["0", title_ind2], subfields=title_subfields)
    )

    # 246 - other title
    for title in data.title_other:
        record.add_ordered_field(
            Field(
                tag="246",
                indicators=["1", "3"],
                subfields=[Subfield(code="a", value=title)],
            )
        )

    # 264 publication tags
    pub_place = (
        data.pub_place if data.pub_place else "[Place of publication not identified]"
    )
    publisher = data.publisher if data.publisher else "[publisher not identified]"
    date = data.pub_date if data.pub_date else "[date of publication not identified]"
    pub_data = {"a": f"{pub_place}:", "b": f"{publisher},", "c": f"{date}"}
    record.add_ordered_field(
        Field(
            tag="264",
            indicators=[" ", "1"],
            subfields=[Subfield(code=k, value=v) for k, v in pub_data.items()],
        )
    )
    # 300 tag
    record.add_ordered_field(
        Field(
            tag="300",
            indicators=[" ", " "],
            subfields=[Subfield(code="a", value="1 board game")],
        )
    )

    # RDA 3xx tags
    record.add_ordered_field(
        Field(
            tag="336",
            indicators=[" ", " "],
            subfields=[
                Subfield(code="a", value="three-dimensional form"),
                Subfield(code="b", value="tdf"),
                Subfield(code="2", value="rdacontent"),
            ],
        )
    )
    record.add_ordered_field(
        Field(
            tag="337",
            indicators=[" ", " "],
            subfields=[
                Subfield(code="a", value="unmediated"),
                Subfield(code="b", value="n"),
                Subfield(code="2", value="rdamedia"),
            ],
        )
    )
    record.add_ordered_field(
        Field(
            tag="338",
            indicators=[" ", " "],
            subfields=[
                Subfield(code="a", value="object"),
                Subfield(code="b", value="nr"),
                Subfield(code="2", value="rdacarrier"),
            ],
        )
    )

    # 500 notes
    record.add_ordered_field(
        Field(
            tag="500",
            indicators=[" ", " "],
            subfields=[Subfield(code="a", value=f"Number of players: {data.players}")],
        )
    )

    record.add_ordered_field(
        Field(
            tag="500",
            indicators=[" ", " "],
            subfields=[Subfield(code="a", value=f"Game duration: {data.duration}")],
        )
    )

    # content note 505
    if data.content:
        record.add_ordered_field(
            Field(
                tag="505",
                indicators=["0", " "],
                subfields=[Subfield(code="a", value=data.content)],
            )
        )

    # 520 summary
    if data.desc:
        record.add_ordered_field(
            Field(
                tag="520",
                indicators=[" ", " "],
                subfields=[Subfield(code="a", value=f"{data.desc}.")],
            )
        )

    # 521 note
    record.add_ordered_field(
        Field(
            tag="521",
            indicators=[" ", " "],
            subfields=[Subfield(code="a", value=data.age)],
        )
    )

    # 655 genre
    record.add_ordered_field(
        Field(
            tag="655",
            indicators=[" ", "7"],
            subfields=[
                Subfield(code="a", value="Board games."),
                Subfield(code="2", value="lcgft"),
            ],
        )
    )

    # 856 fields (link to project)
    record.add_ordered_field(
        Field(
            tag="856",
            indicators=["4", " "],
            subfields=[
                Subfield(
                    code="u", value="https://www.bklynlibrary.org/boardgamelibrary"
                ),
                Subfield(code="z", value="Board Game Library website"),
            ],
        )
    )

    # 960 item field
    for barcode in data.central_barcodes:
        field = create_item_field("02abg", barcode, data.price, status_code)
        record.add_ordered_field(field)

    for barcode in data.crown_barcodes:
        field = create_item_field("30abg", barcode, data.price, status_code)
        record.add_ordered_field(field)

    for barcode in data.bushwick_barcodes:
        field = create_item_field("29abg", barcode, data.price, status_code)
        record.add_ordered_field(field)

    for barcode in data.mckinley_barcodes:
        field = create_item_field("67abg", barcode, data.price, status_code)
        record.add_ordered_field(field)

    for barcode in data.newutrecht_barcodes:
        field = create_item_field("51abg", barcode, data.price, status_code)
        record.add_ordered_field(field)

    for barcode in data.windsor_barcodes:
        field = create_item_field("77abg", barcode, data.price, status_code)
        record.add_ordered_field(field)

    for barcode in data.adams_st_barcodes:
        field = create_item_field("88abg", barcode, data.price, status_code)
        record.add_ordered_field(field)

    # 949 command line
    if suppressed is True:
        opac_display_command = "b3=n"
    else:
        opac_display_command = ""
    record.add_ordered_field(
        Field(
            tag="949",
            indicators=[" ", " "],
            subfields=[Subfield(code="a", value=f"*b2=o;{opac_display_command}")],
        )
    )

    return record
