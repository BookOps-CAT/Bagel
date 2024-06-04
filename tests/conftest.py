import pytest
from bagel.ingest import Row


@pytest.fixture
def stub_row() -> Row:
    return Row(
        processing="completed",
        title="Foo",
        title_part="Bar",
        players="2",
        duration="30 min",
        age="7+",
        central_barcodes="34444000000000",
        crown_barcodes="34444111111111",
        bushwick_barcodes="34444222222222",
        mckinley_barcodes="34444333333333",
        newutrecht_barcodes="34444444444444",
        windsor_barcodes="34444555555555",
        price="39.99",
        title_other="Baz",
        subtitle="Spam",
        author="Michel Lalet, Laurent Levi",
        isbn="9781234567890",
        upc="123456789012",
        pub_place="New York, NY",
        publisher="FooBar",
        pub_date="2024",
        desc="Description of game",
        content="1 gameboard",
        email="foobar@email.com",
        adams_st_barcodes="34444666666666",
    )
