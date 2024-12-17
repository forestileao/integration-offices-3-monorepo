import RPi.GPIO as GPIO
from time import sleep


class FansController:
  def __init__(self, chambers):
    self.chambers = chambers
    self.pwms = {}

    for chamber in chambers:
      GPIO.setup(chamber['fanPin'], GPIO.OUT)
      GPIO.output(chamber['fanPin'], GPIO.LOW)
      GPIO.setup(chamber['fanServoPin'], GPIO.OUT)
      pwm = GPIO.PWM(chamber['fanServoPin'], 25)
      pwm.start(0)
      self.pwms[chamber['id']] = pwm


  def turnOnFan(self, chamber_id):
    for chamber in self.chambers:
      if chamber['id'] == chamber_id:
        GPIO.output(chamber['fanPin'], GPIO.HIGH)
        pwm = self.pwms[chamber_id]
        pwm.ChangeDutyCycle(2.5)
        sleep(1)
        pwm.ChangeDutyCycle(0)
        break

  def turnOffFan(self, chamber_id):
    for chamber in self.chambers:
      if chamber['id'] == chamber_id:
        GPIO.output(chamber['fanPin'], GPIO.LOW)
        pwm = self.pwms[chamber_id]
        pwm.ChangeDutyCycle(12.5)
        sleep(1)
        pwm.ChangeDutyCycle(0)
        break

if __name__ == '__main__':
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    chambers = [
    {
      'id': '90617ba4-ee9b-488f-82bc-cbe8b43aac67',
      'whitePin': 21,
      'ledPin': 15,
      'pumpPin': 18,
      'heaterPin': 22,
      'peltierPin': 4,
      'chamberLocation': 4200,
      'waterLevelChannel': 0,
      'soilMoistureChannel': 1,
      'ledLightsActivated': False,
      'tempMuxChannel': 0,
      'fanPin': 24,
      'fanServoPin': 25,
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
      'whitePin': 20,
      'ledPin': 14,
      'pumpPin': 24,
      'heaterPin': 25,
      'peltierPin': 8,
      'chamberLocation': 1200,
      'waterLevelChannel': 2,
      'soilMoistureChannel': 3,
      'ledLightsActivated': False,
      'tempMuxChannel': 1,
      'fanPin': 9,
      'fanServoPin': 11,
      'parameters': {
        "temperatureRange": "28",
        "soilMoistureLowerLimit": 60,
        "photoCaptureFrequency": "60",
        "id": "1e43809c-0daa-413f-ab18-988ef80e4af6",
        "lightingRoutine": "07:40/18:20",
        "ventilationSchedule": "10:00/11:00"
        }
    },]
    
    fans = FansController(chambers)
    while True:
      
      #fans.turnOnFan(chambers[0]['id'])
      fans.turnOnFan(chambers[1]['id'])
      sleep(3)
      #fans.turnOffFan(chambers[0]['id'])
      fans.turnOffFan(chambers[1]['id'])
    
      sleep(3)

