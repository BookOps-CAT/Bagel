import pytest

from bagel.models import Row


@pytest.fixture
def stub_row() -> Row:
    return Row(
        processing="completed",
        title="Foo",
        title_part="Bar",
        players="2",
        duration="30 min",
        age="7+",
        central_barcodes=["34444000000000"],
        crown_barcodes=["34444111111111"],
        bushwick_barcodes=["34444222222222"],
        mckinley_barcodes=["34444333333333"],
        newutrecht_barcodes=["34444444444444"],
        windsor_barcodes=["34444555555555"],
        price="39.99",
        title_other=["Baz"],
        subtitle="Spam",
        author="Michel Lalet, Laurent Levi",
        isbn=["9781234567890"],
        upc=["123456789012"],
        pub_place="New York, NY",
        publisher="FooBar",
        pub_date="2024",
        desc="Description of game",
        content="1 gameboard",
        email="foobar@email.com",
        adams_st_barcodes=["34444666666666"],
        greenpoint_barcodes=["34444777777777"],
        dekalb_barcodes=["34444888888888"],
        clarendon_barcodes=["34444999999999"],
    )


@pytest.fixture
def mock_valid_metadata(mocker) -> None:
    data = """Timestamp,Processing,Title proper,Name of part / expansion,Number of players,Game duration,Recommended age,Central Library Barcodes,Crown Heights Barcodes,Bushwick Barcodes,McKinley Park Barcodes,New Utrecht Barcodes,Windsor Terrace Barcodes,Price,Other titles,Subtitle,Authors/designers,ISBN,UPC,Place of publication,Publisher,Date of publication,Description/summary,List of components,Email Address,Adams St. Barcodes,Greenpoint Barcodes,Dekalb Barcodes,Clarendon Barcodes\n1/1/2020 01:01:30,completed,Board Game 1,,2,30 mins,7+,,34444111111111,,,,,1.99,,,"Foo, Bar",,,,,,"Players play in turns","1 gameboard",fakeemail,,,,\n1/1/2020 01:02:30,completed,Board Game 2,,2,30 mins,7+,,34444222222222,,,,,1.99,,,"Foo, Bar",,,,,,"Players play in turns","1 gameboard",fakeemail,,,,\n1/1/2020 01:01:30,completed,Board Game 3,,2,30 mins,7+,,34444333333333,,,,,1.99,,,"Foo, Bar",,,,,,"Players play in turns","1 gameboard",fakeemail,,,,\n1/1/2020 01:01:30,completed,Board Game 4,,2,30 mins,7+,,34444444444444,,,,,1.99,,,"Foo, Bar",,,,,,"Players play in turns","1 gameboard",fakeemail,,,,\n1/1/2020 01:01:30,completed,Board Game 5,,2,30 mins,7+,,34444555555555,,,,,1.99,,,"Foo, Bar",,,,,,"Players play in turns","1 gameboard",fakeemail,,,,"""  # noqa: E501
    m = mocker.mock_open(read_data=data)
    mocker.patch("bagel.ingest.open", m)
    mocker.patch("bagel.validate.open", m)


@pytest.fixture
def mock_invalid_metadata(mocker) -> None:
    data = "Timestamp,Processing,Title proper\nFoo,Bar,Baz"
    m = mocker.mock_open(read_data=data)
    mocker.patch("bagel.ingest.open", m)
    mocker.patch("bagel.validate.open", m)


@pytest.fixture
def mock_empty_metadata(mocker) -> None:
    data = """Timestamp,Processing,Title proper,Name of part / expansion,Number of players,Game duration,Recommended age,Central Library Barcodes,Crown Heights Barcodes,Bushwick Barcodes,McKinley Park Barcodes,New Utrecht Barcodes,Windsor Terrace Barcodes,Price,Other titles,Subtitle,Authors/designers,ISBN,UPC,Place of publication,Publisher,Date of publication,Description/summary,List of components,Email Address,Adams St. Barcodes,Greenpoint Barcodes,Dekalb Barcodes,Clarendon Barcodes"""  # noqa: E501
    m = mocker.mock_open(read_data=data)
    mocker.patch("bagel.ingest.open", m)
    mocker.patch("bagel.validate.open", m)
