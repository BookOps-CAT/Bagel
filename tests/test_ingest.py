import itertools

import pytest

from bagel.ingest import form_data_reader, str2list, trim_string


def test_form_data_reader(mock_valid_metadata):
    data = form_data_reader("temp/metadata.csv")
    rows = []
    for row in itertools.islice(data, 5):
        rows.append(row.processing)
    assert rows == ["completed", "completed", "completed", "completed", "completed"]


def test_form_data_reader_empty_spreadsheet(mock_empty_metadata):
    data = form_data_reader("temp/metadata.csv")
    rows = []
    for row in data:
        rows.append(row)
    assert rows == []


@pytest.mark.parametrize(
    "input, output",
    [
        ("Title.", "Title"),
        ("Title", "Title"),
        ("Title\n", "Title"),
        ("Title , \n", "Title"),
        ("", ""),
        ("Title ;", "Title"),
        (None, ""),
        ("Some desc (details).", "Some desc (details)"),
        ("This is madness! ", "This is madness!"),
        ("  Some title.\n", "Some title"),
    ],
)
def test_trim_string(input, output):
    assert trim_string(input) == output


@pytest.mark.parametrize(
    "input, output",
    [("1;2;3;4;", ["1", "2", "3", "4"]), ("1  ;  2 ;3", ["1", "2", "3"]), ("1", ["1"])],
)
def test_str2list(input, output):
    assert str2list(input) == output
