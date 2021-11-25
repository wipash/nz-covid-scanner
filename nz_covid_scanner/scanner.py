import serial


class Scanner:
    def __init__(self, dev="/dev/ttyACM0", baudrate=115200):
        self.scanner = serial.Serial(dev, rtscts=True, dsrdtr=True, timeout=10)
        self.scanner.baudrate = baudrate
