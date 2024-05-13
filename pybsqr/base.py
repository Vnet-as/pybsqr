import base64
import binascii
import io
import lzma
import pathlib

from qrcode import QRCode


class BySquare:

    def __init__(self, xml=None):
        self._xml = xml
        self._fields = None
        self._code = None

    @property
    def xml(self):
        return self._xml

    @property
    def fields(self):
        return self._fields or self.xml_to_fields()

    @property
    def code(self):
        return self._code or self.generate_code()

    def _generate_code(self, fields: list[str], type_: int) -> str:
        fields_joined = "\t".join(map(lambda x: x.replace("\t", " "), map(str, fields)))

        checksum = binascii.crc32(fields_joined.encode()).to_bytes(4, "little")
        final_string = checksum + fields_joined.encode()

        compressed = lzma.compress(
            final_string,
            format=lzma.FORMAT_RAW,
            filters=[
                {"id": lzma.FILTER_LZMA1, "lc": 3, "lp": 0, "pb": 2, "dict_size": 2**17}
            ],
        )
        compressed_with_len = (
            bytes((type_, 0x00)) + len(final_string).to_bytes(2, "little") + compressed
        )

        code = base64.b32hexencode(compressed_with_len).decode().strip("=")

        return code

    def _generate_plain_png(self, code: str) -> io.BytesIO:
        buf = io.BytesIO()
        qr = QRCode()
        qr.add_data(code)
        img = qr.make_image()
        img.save(buf)
        buf.seek(0)
        return buf

    def _generate_framed_png(self, code: str, frame: str) -> io.BytesIO:
        from PIL import Image
        from qrcode.image.pil import PilImage

        buf = io.BytesIO()

        frame_img = Image.open(pathlib.Path(__file__).parent / f"frames/{frame}.png")
        qr = QRCode(image_factory=PilImage)
        qr.add_data(code)
        qr = qr.make_image(back_color="transparent")
        frame_img = frame_img.resize(
            (qr.height, round(qr.height * frame_img.height / frame_img.width))
        )
        qr = qr.convert("RGBA")
        qr.putdata(
            list(
                map(
                    lambda d: [255, 255, 255, 0] if d[:3] == [255, 255, 255] else d,
                    qr.getdata(),
                )
            )
        )
        frame_img.alpha_composite(qr)
        white_bg = Image.new('RGBA', frame_img.size, 'WHITE')
        frame_img = Image.alpha_composite(white_bg, frame_img)
        frame_img.save(buf, format="PNG")
        buf.seek(0)

        return buf

    def _generate_qr(self, code: str, frame=None, format="PNG"):
        if format == "PNG":
            if frame is None:
                img = self._generate_plain_png(code)
            else:
                img = self._generate_framed_png(code, frame)
        return img
