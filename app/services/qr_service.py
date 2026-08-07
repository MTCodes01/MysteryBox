"""
QR code generation service.

Generates a base64-encoded PNG QR code pointing to /join/<token>.
"""
import base64
import io
import logging
import uuid

import qrcode
from qrcode.image.pil import PilImage

logger = logging.getLogger(__name__)


def generate_token() -> str:
    """Return a fresh URL-safe token."""
    return uuid.uuid4().hex


def make_qr_base64(join_url: str) -> str:
    """
    Generate a QR code for the given URL and return it as a base64 data-URI.
    """
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(join_url)
    qr.make(fit=True)

    img: PilImage = qr.make_image(fill_color="#0f172a", back_color="#f8fafc")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    b64 = base64.b64encode(buf.read()).decode()
    return f"data:image/png;base64,{b64}"
