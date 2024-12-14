import busio
import board
import time

I2C_BUS = 1  # Usually 1 for Raspberry Pi
PCA9548A_ADDRESS = 0x70  # Default address of PCA9548A

class Multiplexer:
  def __init__(self):
    self.bus = busio.I2C(board.SCL, board.SDA)

  def select_channel(self, channel):
    # Write a byte to the PCA9548A to enable the desired channel
    while not self.bus.try_lock():  # Ensure the I2C bus is available
        pass
    try:
        self.bus.writeto(PCA9548A_ADDRESS, bytes([1 << channel]))
        time.sleep(0.1)  # Short delay to ensure channel switching
    finally:
        self.bus.unlock()
