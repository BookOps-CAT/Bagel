import pytest
import pandas as pd  # type: ignore
from bagel.download import URL


from bagel.ingest import (
    lower_first_letter,
    has_alphanumeric_last,
    remove_white_space_and_trailing_punctuation,
    remove_left_white_space,
    str2list,
)


def test_form_data_reader_headings():
    df = pd.read_csv(URL, usecols=range(0, 25))
    assert df.columns[0] == "Timestamp"
    assert df.columns[1] == "Processing"
    assert df.columns[2] == "Title proper"
    assert df.columns[3] == "Name of part / expansion"
    assert df.columns[4] == "Number of players"
    assert df.columns[5] == "Game duration"
    assert df.columns[6] == "Recommended age"
    assert df.columns[7] == "Central Library Barcodes"
    assert df.columns[8] == "Crown Heights Barcodes"
    assert df.columns[9] == "Bushwick Barcodes"
    assert df.columns[10] == "McKinley Park Barcodes"
    assert df.columns[11] == "New Utrecht Barcodes"
    assert df.columns[12] == "Windsor Terrace Barcodes"
    assert df.columns[13] == "Price"
    assert df.columns[14] == "Other titles"
    assert df.columns[15] == "Subtitle"
    assert df.columns[16] == "Authors/designers"
    assert df.columns[17] == "ISBN"
    assert df.columns[18] == "UPC"
    assert df.columns[19] == "Place of publication"
    assert df.columns[20] == "Publisher"
    assert df.columns[21] == "Date of publication"
    assert df.columns[22] == "Description/summary"
    assert df.columns[23] == "List of components"
    assert df.columns[24] == "Email Address"


def test_lower_first_letter():
    assert lower_first_letter("Python") == "python"


def test_lower_first_letter_with_empty_string():
    assert lower_first_letter("") == ""


def test_lower_first_letter_with_one_chr():
    assert lower_first_letter("A") == "a"


def test_lower_first_letter_with_integer():
    assert lower_first_letter(2)


def test_has_alphanumeric_last_poitive():
    assert has_alphanumeric_last("ABcD") is True


def test_has_alphanumeric_last_line_break():
    assert has_alphanumeric_last("ABcD\n") is False


def test_has_alphanumeric_last_period():
    assert has_alphanumeric_last("ABcD.") is False


def test_has_alphanumeric_last_empty_string():
    with pytest.raises(IndexError):
        has_alphanumeric_last("")


def test_has_alphanumeric_last_None():
    with pytest.raises(TypeError):
        has_alphanumeric_last(None)


def test_has_alphanumeric_last_empty():
    with pytest.raises(TypeError):
        has_alphanumeric_last()


def test_has_alphanumeric_white_space_in_the_middle():
    assert has_alphanumeric_last("Some title") is True


def test_remove_white_space_and_trailing_punctuation_one_period():
    assert remove_white_space_and_trailing_punctuation("Title.") == "Title"


def test_remove_white_space_and_trailing_punctuation_when_not_needed():
    assert remove_white_space_and_trailing_punctuation("Title") == "Title"


def test_remove_white_space_and_trailing_punctuation_with_line_break():
    assert remove_white_space_and_trailing_punctuation("Title\n") == "Title"


def test_remove_white_space_and_trailing_punctuation_with_multi_non_alphanumerics():
    assert remove_white_space_and_trailing_punctuation("Title . \n") == "Title"


def test_remove_white_space_and_trailing_punctuation_with_empty_string():
    assert remove_white_space_and_trailing_punctuation("") == ""


def test_remove_white_space_and_trailing_punctuation_with_None():
    assert remove_white_space_and_trailing_punctuation(None) == ""


def test_remove_white_space_and_trailing_punctuation_except_closing_parenthesis():
    assert (
        remove_white_space_and_trailing_punctuation("Some desc (details).")
        == "Some desc (details)"
    )


def test_remove_white_space_and_trailing_punctuation_except_exclamation_mark():
    assert (
        remove_white_space_and_trailing_punctuation("This is madness! ")
        == "This is madness!"
    )


def test_left_right_white_space():
    assert remove_left_white_space("  Some title") == "Some title"


def test_normalize_title_with_starting_white_space_and_ending_period():
    assert (
        remove_white_space_and_trailing_punctuation("  Some title.\n") == "Some title"
    )


def test_str2list():
    assert str2list("1;2;3;4;") == ["1", "2", "3", "4"]


def test_str2list_with_trailing_white_space():
    assert str2list("1  ;  2 ;3") == ["1", "2", "3"]


def test_str2list_with_one_element():
    assert str2list("1") == ["1"]
