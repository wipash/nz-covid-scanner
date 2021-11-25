from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import (
    proportional,
    CP437_FONT,
    TINY_FONT,
    SINCLAIR_FONT,
    LCD_FONT,
)


class LED:
    def __init__(self, font=CP437_FONT):
        matrixserial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(
            matrixserial,
            cascaded=4,
            block_orientation=-90,
            rotate=0,
            blocks_arranged_in_reverse_order=False,
        )
        self.font = font

    def write_text(self, writetext, proportional_font=False):
        font = proportional(self.font) if proportional_font else self.font
        with canvas(self.device) as draw:
            text(draw, (0, 0), writetext, fill="white", font=font)
