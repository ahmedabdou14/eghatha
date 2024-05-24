import base64
import io
import random
from PIL import Image

_TL = 40, 28
_BR = 38, 40


def gen_location() -> tuple[float, float]:
    return random.uniform(_TL[0], _BR[0]), random.uniform(_TL[1], _BR[1])


def get_mid_location() -> tuple[float, float]:
    return (_TL[0] + _BR[0]) / 2, (_TL[1] + _BR[1]) / 2


def img_to_base64(image_file: io.BytesIO) -> str:
    """Converts an image file to a base64 string."""
    buffered = io.BytesIO()
    with Image.open(image_file) as image:
        image.save(buffered, format="JPEG")
    return f"data:image/jpeg;base64,{base64.b64encode(buffered.getvalue()).decode()}"


def base64_to_img(base64_str: str) -> Image.Image:
    """Converts a base64 string to an image."""
    return Image.open(io.BytesIO(base64.b64decode(base64_str.split(",")[1])))


def priority_color(priority: int) -> str:
    return ["lightred", "blue", "orange", "purple", "red"][priority - 1]
