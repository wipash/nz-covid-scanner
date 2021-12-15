from covidqr import CovidQR
from display import Display
import time
import pygame

# Delay for screen to reset to normal after displaying scan results
SCREEN_RESET_TIMEOUT = 5000


def run():
    from scanner import Scanner

    pygame.init()

    clock = pygame.time.Clock()

    main_loop = False

    display = Display()

    display.set_system_message("Loading")
    display.update()
    print("Loading")

    qr = CovidQR()
    scanner = Scanner()

    while not scanner.init_scanner():
        print("Couldn't load scanner")
        display.set_system_message("Couldn't load scanner")
        display.update()
        time.sleep(1)

    display.set_system_message("Ready to scan!")
    display.update()
    print("Ready")

    main_loop = True

    while main_loop:
        s = scanner.readline()
        if s:
            try:
                covid_pass = qr.decode_qr(s)
                subject = qr.validate_verifiable_claim(covid_pass["vc"])
                display.valid_pass(subject)
                pygame.time.set_timer(pygame.USEREVENT, SCREEN_RESET_TIMEOUT, 1)
                print("-----= Valid Pass =-----")
                print(f'Name: {subject["givenName"]} {subject["familyName"]}')
                print(f'DOB:  {subject["dob"]}')
                print("------------------------")
            except Exception as e:
                display.invalid_pass(message=str(e))
                pygame.time.set_timer(pygame.USEREVENT, SCREEN_RESET_TIMEOUT, 1)
                print(e)
        for e in pygame.event.get():
            if e.type == pygame.USEREVENT:
                print("Reset display")
                display.reset()
            if e.type == pygame.QUIT:
                main_loop = False

        display.update()
        clock.tick(30)


if __name__ == "__main__":
    run()
