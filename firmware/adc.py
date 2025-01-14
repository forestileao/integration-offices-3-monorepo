import board
import time
from time import sleep
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from multiplexer import Multiplexer

class AdcController:
    def __init__(self, i2cBus = None) -> None:
        # Create an ADS1115 object
        self.ads = ADS.ADS1115(busio.I2C(board.SCL, board.SDA) if i2cBus is None else i2cBus)

        # Define the analog input channel
        self.channels = [
            AnalogIn(self.ads, ADS.P0),
            AnalogIn(self.ads, ADS.P1),
            AnalogIn(self.ads, ADS.P2),
            AnalogIn(self.ads, ADS.P3),
        ]

    def read_value(self, channel):
        while True:
            time.sleep(0.1)
            try:
                return self.channels[channel].value
            except:
                print("Error reading ADC value on channel", channel)

    def read_voltage(self, channel):
        return self.channels[channel].voltage

if __name__ == "__main__":
    sleep(2)
    multi = Multiplexer()
    sleep(2)
    print('started multiplexer')
    multi.select_channel(2)

    print('selected channel')

    adc = AdcController(multi.bus)

    print('initialized bus')

    for i in range(0, 2, 1):
        print('reading value in channel ' + str(i))
        print(f"ADC Value: {adc.read_value(i)}")
        print(f"Voltage: {adc.read_voltage(i)}")
        time.sleep(1)

# soil moisture
# min: 31198 # seco
# max 15000 # molhado
