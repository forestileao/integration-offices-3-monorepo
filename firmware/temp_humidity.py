from RPi import GPIO
from SDL_Pi_HDC1080 import SDL_Pi_HDC1080
from multiplexer import Multiplexer
from time import sleep

class TempHumidity:
  def __init__(self, chambers=[], multiplexer = None) -> None:
    self.multiplexer = multiplexer
    self.chambers = chambers

    for chamber in chambers:
      channel = chamber['tempMuxChannel']
      self.multiplexer.select_channel(channel)
      break

    sleep(0.2)

    self.hdc1080 = SDL_Pi_HDC1080()

    for chamber in chambers:
      GPIO.setup(chamber['heaterPin'], GPIO.OUT)
      GPIO.output(chamber['heaterPin'], GPIO.LOW)
      GPIO.setup(chamber['peltierPin'], GPIO.OUT)
      GPIO.output(chamber['peltierPin'], GPIO.LOW)


  def read_temperature(self, chamber_id):
    sleep(0.2)
    if self.multiplexer:
      for chamber in self.chambers:
        if chamber['id'] == chamber_id:
          channel = chamber['tempMuxChannel']
          self.multiplexer.select_channel(channel)

    return self.hdc1080.readTemperature()


  def read_humidity(self, chamber_id):
    sleep(0.2)
    if self.multiplexer:
      for chamber in self.chambers:
        if chamber['id'] == chamber_id:
          channel = chamber['tempMuxChannel']
          self.multiplexer.select_channel(channel)

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

if __name__ == '__main__':
  chambers = [
    {
      'id': '90617ba4-ee9b-488f-82bc-cbe8b43aac67',
      'whitePin': 17,
      'ledPin': 27,
      'pumpPin': 18,
      'heaterPin': 22,
      'peltierPin': 4,
      'chamberLocation': 1200,
      'waterLevelChannel': 0,
      'soilMoistureChannel': 1,
      'ledLightsActivated': False,
      'tempMuxChannel': 0,
      'fanPin': 24,
      'parameters': {
        "temperatureRange": "17",
        "soilMoistureLowerLimit": 60,
        "photoCaptureFrequency": "60",
        "id": "b231822f-5e74-41ea-9678-0c61404fe6dd",
        "lightingRoutine": "07:40/18:20",
        "ventilationSchedule": "10:00/11:00"
      }
    },
    {
      'id': '7ce04bef-2212-4a9b-8262-ed659cd124ab',
      'whitePin': 22,
      'ledPin': 23,
      'pumpPin': 24,
      'heaterPin': 25,
      'peltierPin': 8,
      'chamberLocation': 4200,
      'waterLevelChannel': 2,
      'soilMoistureChannel': 3,
      'ledLightsActivated': False,
      'tempMuxChannel': 1,
      'fanPin': 9,
      'parameters': {
        "temperatureRange": "28",
        "soilMoistureLowerLimit": 60,
        "photoCaptureFrequency": "60",
        "id": "1e43809c-0daa-413f-ab18-988ef80e4af6",
        "lightingRoutine": "07:40/18:20",
        "ventilationSchedule": "10:00/11:00"
        }
    },
  ]
  multiplexer = Multiplexer()
  temp = TempHumidity(chambers, multiplexer=multiplexer)


  for chamber in chambers:
    print(f"Temperature: {temp.read_temperature(chamber['id'])}")
    print(f"Humidity: {temp.read_humidity(chamber['id'])}")

    temp.turn_on_peltier(chamber['id'])
    sleep(2)
    temp.turn_off_peltier(chamber['id'])
