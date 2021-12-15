import serial


class Scanner:
    def __init__(self, dev="/dev/ttyACM0", baudrate=115200):
        self.dev = dev
        self.baudrate = baudrate

    def init_scanner(self):
        try:
            self.scanner = serial.Serial(self.dev, rtscts=True, dsrdtr=True, timeout=1)
            self.scanner.baudrate = self.baudrate
            return True
        except:
            return False

    def readline(self):
        return self.scanner.readline()

