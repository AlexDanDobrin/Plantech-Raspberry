import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

class MoistureSensor:
    min_value = 21000 # sau arbitrar 1.07 V
    max_value = 65480 # sau 3.3 V

    def __init__(self):
        # spi bus
        self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

        # cs is chip select
        self.cs = digitalio.DigitalInOut(board.D5)

        # mcp object
        self.mcp = MCP.MCP3008(self.spi, self.cs)

        # analog input channel on pin 0 from the humidity sensor
        self.chan = AnalogIn(self.mcp, MCP.P0)

    def get_measurement(self):
        # Cand este complet uscat ADC este 65480 si voltajul este 3.3 V
        # Cand este complet umed ADC este 21000 si voltajul este 1.28 V
        raw_percentage = (1 - (self.chan.value - self.min_value) / (self.max_value - self.min_value)) * 100
        percentage = round(raw_percentage, 2)
        return percentage

   