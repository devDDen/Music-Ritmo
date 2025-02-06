from PIL import Image
from io import BytesIO

from mutagen.mp3 import MP3
from mutagen.flac import FLAC

from . import database as db

MAX_COVER_PREVIEW_SIZE = 128
DEFAULT_COVER_PREVIEW_PATH = "./resources/default_cover_preview.jpg"
DEFAULT_COVER_PATH = "./resources/default_cover.jpg"


def bytes_to_image(image_bytes: bytes) -> Image.Image:
    return Image.open(BytesIO(image_bytes))


def image_to_bytes(image: Image.Image) -> bytes:
    buf = BytesIO()
    image.save(buf, format=image.format)
    return buf.getvalue()

def get_default_cover():
    return Image.open(DEFAULT_COVER_PATH)

def get_cover_preview(image_bytes: bytes | None) -> tuple[bytes | None, str]:
    if image_bytes is None:
        image = Image.open(DEFAULT_COVER_PREVIEW_PATH)
        return image_to_bytes(image), image.format.lower()
    
    image = bytes_to_image(image_bytes)
    width, height = image.size
    if width <= MAX_COVER_PREVIEW_SIZE and height <= MAX_COVER_PREVIEW_SIZE:
        return image_bytes, image.format.lower()
    
    image.thumbnail((MAX_COVER_PREVIEW_SIZE, MAX_COVER_PREVIEW_SIZE))
    return image_to_bytes(image), image.format.lower()


def get_cover_from_mp3(audio_file_mp3: MP3) -> bytes | None:
    tags = audio_file_mp3.tags
    if tags is not None and "APIC:3.jpeg" in tags:
        return tags["APIC:3.jpeg"].data
    return None


def get_cover_from_flac(audio_file_flac: FLAC) -> bytes | None:
    return audio_file_flac.pictures[0].data if len(audio_file_flac.pictures) > 0 else None

def get_cover_art(track: db.Track) -> bytes | None:
    if track.type == "audio/mpeg":
        return get_cover_from_mp3(MP3(track.file_path))
    elif track.type == "audio/flac":
        return get_cover_from_flac(FLAC(track.file_path))
    else:
        return None
