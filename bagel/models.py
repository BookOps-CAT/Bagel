from dataclasses import dataclass


@dataclass
class Row:
    processing: str
    title: str
    title_part: str
    players: str
    duration: str
    age: str
    central_barcodes: list[str]
    crown_barcodes: list[str]
    bushwick_barcodes: list[str]
    mckinley_barcodes: list[str]
    newutrecht_barcodes: list[str]
    windsor_barcodes: list[str]
    price: str
    title_other: list[str]
    subtitle: str
    author: str
    isbn: list[str]
    upc: list[str]
    pub_place: str
    publisher: str
    pub_date: str
    desc: str
    content: str
    email: str
    adams_st_barcodes: list[str]
    greenpoint_barcodes: list[str]
    dekalb_barcodes: list[str]
    clarendon_barcodes: list[str]
