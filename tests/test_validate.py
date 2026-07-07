from bagel.validate import validate_csv, validate_headings, validate_timestamps


def test_validate_headings(mock_valid_metadata):
    valid_headings = validate_headings("temp/metadata.csv")
    assert valid_headings is True


def test_validate_headings_errors(mock_invalid_metadata):
    valid_headings = validate_headings("temp/metadata.csv")
    assert valid_headings is False


def test_validate_timestamps(mock_valid_metadata):
    valid_timestamps = validate_timestamps("temp/metadata.csv")
    assert valid_timestamps is True


def test_validate_timestamp_errors(mock_invalid_metadata):
    valid_timestamps = validate_timestamps("temp/metadata.csv")
    assert valid_timestamps is False


def test_validate_csv(mock_valid_metadata):
    valid_csv = validate_csv("temp/metadata.csv")
    assert valid_csv is True


def test_validate_csv_errors(mock_invalid_metadata):
    valid_csv = validate_csv("temp/metadata.csv")
    assert valid_csv is False
