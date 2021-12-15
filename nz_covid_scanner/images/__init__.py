from pygame import image as Pygimage
from PIL import Image
from pathlib import Path

BG_IMAGE_NORMAL = "bg_image_normal"
BG_IMAGE_SUCCESS = "bg_image_success"
BG_IMAGE_FAIL = "bg_image_fail"
HOLMES_IMAGE = "holmes_image"


def load_images():
    images = {}

    pil_image = Image.open(
        Path(__file__).parent.joinpath("covidstripes.png").absolute()
    ).convert("RGB")
    images[BG_IMAGE_NORMAL] = Pygimage.fromstring(
        pil_image.tobytes(), pil_image.size, pil_image.mode
    )

    pil_image = Image.open(
        Path(__file__).parent.joinpath("covidstripes_green.png").absolute()
    ).convert("RGB")
    images[BG_IMAGE_SUCCESS] = Pygimage.fromstring(
        pil_image.tobytes(), pil_image.size, pil_image.mode
    )

    pil_image = Image.open(
        Path(__file__).parent.joinpath("covidstripes_red.png").absolute()
    ).convert("RGB")
    images[BG_IMAGE_FAIL] = Pygimage.fromstring(
        pil_image.tobytes(), pil_image.size, pil_image.mode
    )

    pil_holmes_image = Image.open(
        Path(__file__).parent.joinpath("holmes.png").absolute()
    )
    images[HOLMES_IMAGE] = Pygimage.fromstring(
        pil_holmes_image.tobytes(), pil_holmes_image.size, pil_holmes_image.mode
    )

    return images
