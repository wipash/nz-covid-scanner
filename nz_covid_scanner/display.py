import pygame
from PIL import Image
from pygame.locals import *
from images import HOLMES_IMAGE, BG_IMAGE
from fonts import ROBOTO_REGULAR_FONT


class Display:
    def __init__(self):
        pygame.mouse.set_visible(False)

        dim_x, dim_y = pygame.display.list_modes()[0]  # (480, 320)

        self.images = self._load_images()
        self.logo_x, self.logo_y = self.images["holmes_image"].get_rect().size

        self.screen = pygame.display.set_mode((dim_x, dim_y), FULLSCREEN)
        self.screen.fill("black")

        self.display_surface = pygame.Surface((dim_x, dim_y))
        self.display_surface.blit(self.images["bg_image"], (0, 0))
        self.display_surface.blit(self.images["holmes_image"], (20, 20))

        self.system_message_surface_blank = pygame.Surface((dim_x - 40, dim_y - self.logo_y - 60), SRCALPHA, 32)

        self.system_message_surface = self.system_message_surface_blank.copy()

        self.system_message_font = pygame.font.Font(ROBOTO_REGULAR_FONT, 30)

    def _load_images(self):
        images = {}

        pil_bg_image = Image.open(BG_IMAGE).convert("RGB")
        images["bg_image"] = pygame.image.fromstring(
            pil_bg_image.tobytes(), pil_bg_image.size, pil_bg_image.mode
        )

        pil_holmes_image = Image.open(HOLMES_IMAGE)
        images["holmes_image"] = pygame.image.fromstring(
            pil_holmes_image.tobytes(), pil_holmes_image.size, pil_holmes_image.mode
        )

        return images

    def update(self):
        draw_surface = self.display_surface.copy()
        draw_surface.blit(self.system_message_surface, (20, self.logo_y + 40))
        self.screen.blit(draw_surface, (0,0))
        pygame.display.update()

    def set_system_message(self, message=""):
        message_text = self.system_message_font.render(message, True, "black")
        self.system_message_surface = self.system_message_surface_blank.copy()
        self.system_message_surface.blit(message_text, (0, 0))

    def valid_pass(self, subject):
        self.set_system_message("")


    def invalid_pass(self, subject = None):
        self.set_system_message("")

    def set_system_message(self, message):
        pass

    def quit(self):
        pygame.quit()
