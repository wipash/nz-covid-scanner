from covidqr import CovidQR
from display import Display
import time
import pygame


def run():
    from scanner import Scanner
    pygame.init()


    main_loop = False

    display = Display()
    qr = CovidQR()
    scanner = Scanner()

    while (not scanner.init_scanner()):
        print("Couldn't load scanner")
        display.set_system_message("Couldn't load scanner")
        display.update()
        time.sleep(1)

    main_loop = True

    display.set_system_message("Ready to scan!")

    while main_loop:
        s = scanner.readline()
        if s:
            try:
                covid_pass = qr.decode_qr(s)
                subject = qr.validate_verifiable_claim(covid_pass["vc"])
                print("-----= Valid Pass =-----")
                print(f'Name: {subject["givenName"]} {subject["familyName"]}')
                print(f'DOB:  {subject["dob"]}')
                print("------------------------")
            except Exception as e:
                print(e)
        display.update()


if __name__ == "__main__":
    run()
