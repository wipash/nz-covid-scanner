# NZ Covid Scanner

Intended to be used with a serial QR code scanner connected to a Raspberry Pi. Detailed output via console, and visual output via a MAX7219 LED matrix.


### For Raspberry Pi 4 with Waveshare 3.5" screen
```bash
## Build display driver
cd ~
git clone https://github.com/juj/fbcp-ili9341.git
mkdir -p ~/fbcp-ili9341/build
cd ~/fbcp-ili9341/build
cmake -DWAVESHARE35B_ILI9486=ON -DSPI_BUS_CLOCK_DIVISOR=30 -DARMV8A=ON -DSTATISTICS=0 ..
make -j

## Configure boot config.txt
sudo vim /boot/config.txt
# Add:
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=87
hdmi_cvt=480 320 60 1 0 0 0

# Replace
dtoverlay=vc4-kms-v3d
# with
dtoverlay=vc4-fkms-v3d

## Set driver to start on boot
sudo vim /etc/rc.local
# Add:
sudo /home/pi/fbcp-ili9341/build/fbcp-ili9341 &
```


### Install prereqs
```bash
# Enable SPI in raspi-config
sudo usermod -a -G spi,gpio,dialout your-username
sudo apt install build-essential gcc python3-dev python3-pip libfreetype6-dev libjpeg-dev libopenjp2-7 libtiff5 libffi-dev libssl-dev

curl -sSL https://install.python-poetry.org | python3 -

poetry install
```

This project is based on the work of:
 - https://github.com/zendamacf/nz-vaccine-pass-verify
 - https://github.com/nz-covid-pass/python-nz-covid-pass
