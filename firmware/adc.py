import board
import time
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from multiplexer import Multiplexer

class AdcController:
    def __init__(self, multiplexer) -> None:
        self.multiplexer = multiplexer

        self.multiplexer.select_channel(2)

        # Create an ADS1115 object
        self.ads = ADS.ADS1115(self.multiplexer.bus)

        # Define the analog input channel
        self.channels = [
            AnalogIn(self.ads, ADS.P0),
            AnalogIn(self.ads, ADS.P1),
            AnalogIn(self.ads, ADS.P2),
            AnalogIn(self.ads, ADS.P3),
        ]

    def read_value(self, channel):
        self.multiplexer.select_channel(2)
        return self.channels[channel].value

    def read_voltage(self, channel):
        self.multiplexer.select_channel(2)
        return self.channels[channel].voltage

if __name__ == "__main__":
    multiplexer = Multiplexer()
    adc = AdcController(multiplexer)
    while True:
        print(f"ADC Value: {adc.read_value(1)}")
        print(f"Voltage: {adc.read_voltage(1)}")
        time.sleep(1)

# soil moisture
# min: 31198 # seco
# max 15000 # molhado
