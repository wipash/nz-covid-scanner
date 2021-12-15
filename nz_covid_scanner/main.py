from covidqr import CovidQR
from display import Display
import time
import pygame

# Delay for screen to reset to normal after displaying scan results
SCREEN_RESET_TIMEOUT = 5 * 1000

# Delay for getting new keys from MoH
UPDATE_KEYS_TIMEOUT = 1 * 60 * 60 * 1000


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
    try:
        display.set_system_message("Updating keys from MoH")
        display.update()
        qr.get_latest_keys()
    except Exception as e:
        display.set_system_message("Error updating keys")
        display.update()
        pygame.time.wait(10000)

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

    reset_event = pygame.USEREVENT + 1
    update_keys_event = pygame.USEREVENT + 2

    pygame.time.set_timer(update_keys_event, UPDATE_KEYS_TIMEOUT)

    while main_loop:
        s = scanner.readline()
        if s:
            try:
                covid_pass = qr.decode_qr(s)
                subject = qr.validate_verifiable_claim(covid_pass["vc"])
                display.valid_pass(subject)
                pygame.time.set_timer(reset_event, SCREEN_RESET_TIMEOUT, 1)
                print("-----= Valid Pass =-----")
                print(f'Name: {subject["givenName"]} {subject["familyName"]}')
                print(f'DOB:  {subject["dob"]}')
                print("------------------------")
            except Exception as e:
                display.invalid_pass(message=str(e))
                pygame.time.set_timer(reset_event, SCREEN_RESET_TIMEOUT, 1)
                print(e)
        for e in pygame.event.get():
            if e.type == reset_event:
                print("Reset display")
                display.reset()
            if e.type == update_keys_event:
                try:
                    qr.get_latest_keys()
                except Exception as e:
                    display.set_system_message("Error updating keys")
                    display.update()
                    pygame.time.wait(10000)
            if e.type == pygame.QUIT:
                main_loop = False

        display.update()
        clock.tick(30)


if __name__ == "__main__":
    run()
