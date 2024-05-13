import pathlib

from lxml import etree, objectify

from .invoice import InvoiceBySquare
from .pay import PayBySquare


def load_schema() -> etree.XMLSchema:
    schema_path = pathlib.Path(__file__).parent / "bysquare.xsd"
    with open(schema_path, "r") as f:
        return etree.XMLSchema(file=f)


def makeparser():
    schema = load_schema()
    return objectify.makeparser(schema=schema)


def get_generator(xml):
    parser = makeparser()
    data = objectify.fromstring(xml, parser)
    if data.tag.endswith("Pay"):
        return PayBySquare(data)
    elif data.tag.endswith("Invoice"):
        return InvoiceBySquare(data)
