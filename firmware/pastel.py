import smbus
import time
import sys

channel_array=[0b00000001,0b00000010,0b00000100,0b00001000,0b00010000,0b00100000,0b01000000,0b10000000]

def I2C_setup(multiplexer,i2c_channel_setup):
    bus = smbus.SMBus(1)
    bus.write_byte(multiplexer,channel_array[i2c_channel_setup])
    time.sleep(0.3)
    print("TCA9548A I2C channel status:", bin(bus.read_byte(multiplexer)))


import smbus
import time

bus = smbus.SMBus(1)

def scan_i2c_bus():
    print("Scanning I2C bus for devices...")
    for address in range(0, 128):
        try:
            bus.read_byte(address)
            print(f"Found device at address 0x{address:02X}")
        except:
            pass

scan_i2c_bus()


def reset_multiplexer(multiplexer):
    bus = smbus.SMBus(1)
    bus.write_byte(multiplexer, 0x00)
    time.sleep(0.3)
    print("Multiplexer reset")

reset_multiplexer(0x70)

I2C_setup(0x70,5)
