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


def test_game_record(stub_row):
    today = datetime.datetime.strftime(
        datetime.datetime.now(tz=datetime.timezone.utc), "%Y%m%d"
    )
    rec = game_record(
        stub_row, control_number="bkl-bgm-0000001", suppressed=False, status_code="g"
    )
    assert isinstance(rec, Record)
    assert rec.leader == "00000crm a2200000M  4500"
    assert today in rec["005"].data


def test_game_record_missing_pub_data(stub_row):
    stub_row = stub_row._replace(
        pub_place="",
        publisher="",
        pub_date="",
    )
    rec = game_record(
        stub_row, control_number="bkl-bgm-0000001", suppressed=False, status_code="g"
    )
    assert "[Place of publication not identified]: " in rec["264"].value()
    assert "[publisher not identified], " in rec["264"].value()
    assert "[date of publication not identified]" in rec["264"].value()


@pytest.mark.parametrize(
    "pub_place, publisher, pub_date, expected",
    [
        ("Foo", "Bar", "2025", "Foo: Bar, 2025"),
        (
            "Foo",
            None,
            None,
            "Foo: [publisher not identified], [date of publication not identified]",
        ),
        ("Foo", "Bar", None, "Foo: Bar, [date of publication not identified]"),
        ("Foo", None, "2025", "Foo: [publisher not identified], 2025"),
        (
            None,
            None,
            None,
            "[Place of publication not identified]: [publisher not identified], [date of publication not identified]",  # noqa: E501
        ),
    ],
)
def test_game_record_pub_data_variants(
    stub_row, pub_place, publisher, pub_date, expected
):
    stub_row = stub_row._replace(
        pub_place=pub_place,
        publisher=publisher,
        pub_date=pub_date,
    )
    rec = game_record(
        stub_row, control_number="bkl-bgm-0000001", suppressed=True, status_code="g"
    )
    assert expected in rec["264"].value()


def test_game_record_missing_title(stub_row):
    with pytest.raises(ValueError) as exc:
        stub_row = stub_row._replace(
            processing="completed",
            title=None,
        )
        game_record(
            stub_row,
            control_number="bkl-bgm-0000001",
            suppressed=False,
            status_code="g",
        )
    assert "Missing title data" in str(exc.value)


@pytest.mark.parametrize(
    "title, subtitle, author, expected_str, expected_bytes",
    [
        ("Foo", "bar", "baz", "Foo: bar/ baz", "00\x1faFoo:\x1fbbar/\x1fcbaz\x1e"),
        ("Foo", None, None, "Foo", "00\x1faFoo\x1e"),
        ("Foo", "bar", None, "Foo: bar", "00\x1faFoo:\x1fbbar\x1e"),
        ("Foo", None, "baz", "Foo/ baz", "00\x1faFoo/\x1fcbaz\x1e"),
    ],
)
def test_game_record_title_variants(
    stub_row, title, subtitle, author, expected_str, expected_bytes
):
    stub_row = stub_row._replace(
        title=title,
        subtitle=subtitle,
        author=author,
    )
    rec = game_record(
        stub_row, control_number="bkl-bgm-0000001", suppressed=True, status_code="g"
    )
    assert expected_str in rec["245"].value()
    assert rec["245"].as_marc21(encoding="utf-8") == bytes(
        expected_bytes, encoding="utf-8"
    )


def test_game_record_unsuppressed(stub_row):
    rec = game_record(
        stub_row, control_number="bkl-bgm-0000001", suppressed=True, status_code="g"
    )
    assert "b3=n" in rec["949"].value()
