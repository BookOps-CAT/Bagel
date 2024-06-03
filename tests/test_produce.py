import datetime
import pytest
from pymarc import Record, Field, Subfield, MARCReader
from bagel.produce import (
    create_item_field,
    generate_controlNo,
    check_article,
    save2marc,
    game_record,
)
from bagel.ingest import Row


@pytest.mark.parametrize(
    "item_data",
    [
        ["02abg", "34444123456789", "1.00", "-"],
        ["30abg", "34444111111111", "1.00", "-"],
        ["29abg", "34444000000000", "1.00", "-"],
    ],
)
def test_create_item_field(item_data):
    item = create_item_field(
        shelfcode=item_data[0],
        barcode=item_data[1],
        price=item_data[2],
        status_code=item_data[3],
    )
    assert isinstance(item, Field)
    assert item.get_subfields("i", "l", "p", "q", "t", "r", "s") == [
        item_data[1],
        item_data[0],
        item_data[2],
        "11",
        "53",
        "i",
        item_data[3],
    ]


@pytest.mark.parametrize(
    "sequence_num, control_num", [(1, "0000001"), (20, "0000020"), (300, "0000300")]
)
def test_generate_controlNo(sequence_num, control_num):
    control_no = generate_controlNo(sequence_num)
    assert control_no == f"bkl-bgm-{control_num}"


@pytest.mark.parametrize(
    "title, chars", [("The Foo", "4"), ("A Bar", "2"), ("An ", "3")]
)
def test_check_article(title, chars):
    ind2 = check_article(title)
    assert ind2 == chars


def test_save2marc(tmpdir):
    record = Record()
    record.leader = "00000crm a2200000M  4500"
    record.add_field(
        Field(tag="001", data="b123456789"),
        Field(tag="008", data="240603n        xxu               vneng d"),
        Field(
            tag="245",
            indicators=["0", "0"],
            subfields=[Subfield(code="a", value="Foo")],
        ),
    )
    save2marc(record, f"{tmpdir}/test.mrc")
    record_ids = []
    reader = MARCReader(open(f"{tmpdir}/test.mrc", "rb"))
    for record in reader:
        record_ids.append(record["001"].data)
    assert len(record_ids) == 1


def test_game_record():
    today = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")
    data = Row(
        processing="completed",
        title="Abalone",
        title_part="",
        players="2",
        duration="30 min",
        age="7+",
        central_barcodes="",
        crown_barcodes="34444938440625",
        bushwick_barcodes="",
        mckinley_barcodes="",
        newutrecht_barcodes="",
        windsor_barcodes="",
        price="39.99",
        title_other="",
        subtitle="",
        author="Michel Lalet, Laurent Levi",
        isbn="",
        upc="",
        pub_place="",
        publisher="",
        pub_date="",
        desc="Players play in turns moving one, two or three marbles at a time. Three push one, three push two, two push one. When pushing one marble at the end of a row, all marbles will move to the next available space simultaneously. Be the first to force a total of six of the opponents marbles off the board. (From back of box)",  # noqa: E501
        content="1 gameboard, 14 white marbles, 14 black marbles, rulebook",
        email="",
        adams_st_barcodes="",
    )
    rec = game_record(
        data, control_number="bkl-bgm-0000001", suppressed=False, status_code="g"
    )
    assert isinstance(rec, Record)
    assert rec.leader == "00000crm a2200000M  4500"
    assert today in rec["005"].data
