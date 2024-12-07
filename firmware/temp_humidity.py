from RPi import GPIO
from SDL_Pi_HDC1080 import SDL_Pi_HDC1080


class TempHumidity:
  def __init__(self, chambers) -> None:
    self.chambers = chambers
    self.hdc1080 = SDL_Pi_HDC1080()

    for chamber in chambers:
      GPIO.setup(chamber['heaterPin'], GPIO.OUT)
      GPIO.output(chamber['heaterPin'], GPIO.LOW)
      GPIO.setup(chamber['peltierPin'], GPIO.OUT)
      GPIO.output(chamber['peltierPin'], GPIO.LOW)


  def read_temperature(self, chamber_id):
    return self.hdc1080.readTemperature()


  def read_humidity(self, chamber_id):
    return self.hdc1080.readHumidity()

  def turn_on_heater(self, chamber_id):
    for chamber in self.chambers:
      if chamber['id'] == chamber_id:
        GPIO.output(chamber['heaterPin'], GPIO.HIGH)

  def turn_off_heater(self, chamber_id):
    for chamber in self.chambers:
      if chamber['id'] == chamber_id:
        GPIO.output(chamber['heaterPin'], GPIO.LOW)

  def turn_on_peltier(self, chamber_id):
    for chamber in self.chambers:
      if chamber['id'] == chamber_id:
        GPIO.output(chamber['peltierPin'], GPIO.HIGH)

  def turn_off_peltier(self, chamber_id):
    for chamber in self.chambers:
      if chamber['id'] == chamber_id:
        GPIO.output(chamber['peltierPin'], GPIO.LOW)
