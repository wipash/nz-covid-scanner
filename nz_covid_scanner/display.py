import pygame
from PIL import Image
from pygame.locals import *
from nz_covid_scanner.images import (
    load_images,
    HOLMES_IMAGE,
    BG_IMAGE_NORMAL,
    BG_IMAGE_SUCCESS,
    BG_IMAGE_FAIL,
)
from nz_covid_scanner.fonts import ROBOTO_REGULAR_FONT


class Display:
    def __init__(self):
        pygame.mouse.set_visible(False)

        dim_x, dim_y = pygame.display.list_modes()[0]  # (480, 320)

        self.images = load_images()
        self.logo_x, self.logo_y = self.images[HOLMES_IMAGE].get_rect().size

        self.screen = pygame.display.set_mode((dim_x, dim_y), FULLSCREEN)
        self.screen.fill("black")

        self.bg_normal = pygame.Surface((dim_x, dim_y))
        self.bg_normal.blit(self.images[BG_IMAGE_NORMAL], (0, 0))
        self.bg_normal.blit(self.images[HOLMES_IMAGE], (20, 20))

        self.bg_success = pygame.Surface((dim_x, dim_y))
        self.bg_success.blit(self.images[BG_IMAGE_SUCCESS], (0, 0))
        self.bg_success.blit(self.images[HOLMES_IMAGE], (20, 20))

        self.bg_fail = pygame.Surface((dim_x, dim_y))
        self.bg_fail.blit(self.images[BG_IMAGE_FAIL], (0, 0))
        self.bg_fail.blit(self.images[HOLMES_IMAGE], (20, 20))

        self.system_message_surface_blank = pygame.Surface(
            (dim_x - 40, dim_y - self.logo_y - 60), SRCALPHA, 32
        )

        self.pass_subject_message_surface_blank = pygame.Surface(
            (dim_x - 40, dim_y - self.logo_y - 60), SRCALPHA, 32
        )

        self.system_message_font = pygame.font.Font(ROBOTO_REGULAR_FONT, 30)
        self.pass_subject_font = pygame.font.Font(ROBOTO_REGULAR_FONT, 30)

        self.reset()

    def reset(self):
        self.bg = self.bg_normal.copy()
        self.pass_subject_message_surface = (
            self.pass_subject_message_surface_blank.copy()
        )
        self.system_message_surface = self.system_message_surface_blank.copy()

    def update(self):
        draw_surface = self.bg.copy()
        draw_surface.blit(self.system_message_surface, (20, self.logo_y + 40))
        self.screen.blit(draw_surface, (0, 0))
        pygame.event.pump()
        pygame.display.update()

    def set_system_message(self, message=""):
        message_text = self.system_message_font.render(message, True, "black")
        self.system_message_surface = self.system_message_surface_blank.copy()
        self.system_message_surface.blit(message_text, (0, 0))

    def valid_pass(self, subject):
        self.bg = self.bg_success.copy()

        self.system_message_surface = self.system_message_surface_blank.copy()

        name_surf = self.pass_subject_font.render(
            f'{subject["givenName"]} {subject["familyName"]}', True, "black"
        )
        name_rect = name_surf.get_rect()
        dob_surf = self.pass_subject_font.render(subject["dob"], True, "black")
        dob_rect = dob_surf.get_rect()
        dob_rect.topleft = (0, name_rect.h + 5)

        self.system_message_surface.blit(name_surf, name_rect)
        self.system_message_surface.blit(dob_surf, dob_rect)

    def invalid_pass(self, message=None, subject=None):
        self.bg = self.bg_fail.copy()
        self.set_system_message("")
        if message:
            error_surf = self.pass_subject_font.render(message, True, "black", "red")
            error_rect = error_surf.get_rect()
            bigger_surf = pygame.Surface(error_rect.inflate(40, 10).size)
            bigger_surf.fill("red")
            bigger_surf.blit(
                error_surf, error_surf.get_rect(center=bigger_surf.get_rect().center)
            )
            self.system_message_surface.blit(bigger_surf, (0, 0))

    def quit(self):
        pygame.quit()
