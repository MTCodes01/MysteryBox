"""
Image validation and compression service.
"""
import io
import logging
import uuid
from pathlib import Path

from PIL import Image, UnidentifiedImageError

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_BYTES = 20 * 1024 * 1024  # 20 MB
MAX_DIMENSION = 2000
QUALITY = 85

UPLOADS_DIR = Path(__file__).parent.parent / "uploads"


def get_upload_dir() -> Path:
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    return UPLOADS_DIR


def validate_and_save(raw_bytes: bytes, original_filename: str) -> tuple[str, str]:
    """
    Validate the image, compress/resize if needed, and save to disk.

    Returns:
        (stored_filename, extension)  e.g. ("abc123.jpg", ".jpg")

    Raises:
        ValueError on invalid input.
    """
    if len(raw_bytes) > MAX_BYTES:
        raise ValueError("File exceeds 20 MB limit.")

    suffix = Path(original_filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {suffix}")

    # Validate via Pillow (catches faked extensions)
    try:
        img = Image.open(io.BytesIO(raw_bytes))
        img.verify()          # raises on corrupt
        img = Image.open(io.BytesIO(raw_bytes))   # re-open after verify
    except (UnidentifiedImageError, Exception) as exc:
        raise ValueError(f"Invalid image: {exc}") from exc

    # Normalise format
    fmt_map = {".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG", ".webp": "WEBP"}
    save_fmt = fmt_map.get(suffix, "JPEG")
    out_ext  = ".jpg" if suffix in (".jpg", ".jpeg") else suffix

    # Convert RGBA→RGB for JPEG
    if save_fmt == "JPEG" and img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Resize if too large
    if img.width > MAX_DIMENSION or img.height > MAX_DIMENSION:
        img.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Image.LANCZOS)
        logger.info("Resized image to %dx%d", img.width, img.height)

    # Save
    stored_name = uuid.uuid4().hex + out_ext
    dest = get_upload_dir() / stored_name

    save_kwargs: dict = {}
    if save_fmt == "JPEG":
        save_kwargs = {"quality": QUALITY, "optimize": True}
    elif save_fmt == "WEBP":
        save_kwargs = {"quality": QUALITY, "method": 4}

    img.save(dest, format=save_fmt, **save_kwargs)
    logger.info("Saved upload: %s (%d bytes)", stored_name, dest.stat().st_size)

    return stored_name, out_ext
