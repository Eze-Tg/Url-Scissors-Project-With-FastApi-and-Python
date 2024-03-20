# from keygen import create_random_key
from fastapi import Response
import qrcode


def generate_qrcode(short_url: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(short_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img_bytes = img.get_image()
    response = Response(content=img_bytes, media_type="image/png")
    return response