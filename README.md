# NZ Covid Scanner

Intended to be used with a serial QR code scanner connected to a Raspberry Pi. Detailed output via console, and visual output via a MAX7219 LED matrix.



### Install prereqs
```bash
# Enable SPI in raspi-config
sudo usermod -a -G spi,gpio,dialout your-username
sudo apt install build-essential gcc python3-dev python3-pip libfreetype6-dev libjpeg-dev libopenjp2-7 libtiff5 libffi-dev libssl-dev

poetry install
```

This project is based on the work of:
 - https://github.com/zendamacf/nz-vaccine-pass-verify
 - https://github.com/nz-covid-pass/python-nz-covid-pass
