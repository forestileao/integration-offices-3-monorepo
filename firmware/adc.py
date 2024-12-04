import board
import time
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class AdcController:
    def __init__(self) -> None:
        # Initialize the I2C interface
        self.i2c = busio.I2C(board.SCL, board.SDA)

        # Create an ADS1115 object
        self.ads = ADS.ADS1115(self.i2c)

        # Define the analog input channel
        self.channel = AnalogIn(self.ads, ADS.P0)


    def read_value(self):
        return self.channel.value

    def read_voltage(self):
        return self.channel.voltage


if __name__ == "__main__":
    adc = AdcController()
    while True:
        print(f"ADC Value: {adc.read_value()}")
        print(f"Voltage: {adc.read_voltage()}")
        time.sleep(1)
