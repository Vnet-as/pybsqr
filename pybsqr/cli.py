import argparse
import sys

from .xml import get_generator


def main(args: argparse.Namespace):
    if args.xml_file:
        with open(args.xml_file, "r") as f:
            xml = f.read()
    else:
        xml = sys.stdin.read()
    generator = get_generator(xml)
    generator.xml_to_fields()
    code = generator.generate_code()
    if args.code:
        print(code)
        return
    qr = generator.generate_qr(frame=args.frame)
    if not args.output:
        sys.stdout.buffer.write(qr.read())
    else:
        with open(args.output, "wb") as f:
            f.write(qr.read())


def run():
    parser = argparse.ArgumentParser(
        prog="pybsqr", description="Tool for generating BySquare images from XML"
    )
    parser.add_argument("-o", "--output", required=False)
    parser.add_argument(
        "--code", action="store_true", help="Shows generated code as text"
    )
    parser.add_argument(
        "--no-frame",
        dest="frame",
        action="store_false",
        default=True,
        help="No BySquare frame around QR",
    )
    parser.add_argument("xml_file", metavar="XML_FILE", nargs="?")
    args = parser.parse_args()
    main(args)
