import RPi.GPIO as GPIO
from time import sleep


class Servo:
    def __init__(self, pin):
        """Initialize the Servo with a given GPIO pin."""
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)  # 50 Hz for servo
        self.pwm.start(0)  # Start with 0% duty cycle
        self.current_angle = None

    def set_angle(self, angle):
        if angle == self.current_angle:
            return

        self.current_angle = angle

        """Move the servo to the specified angle (0-180 degrees)."""
        duty_cycle = (angle / 18.0) + 2.5  # Convert angle to duty cycle
        self.pwm.ChangeDutyCycle(duty_cycle)
        sleep(0.5)  # Allow servo time to move
        self.pwm.ChangeDutyCycle(0)  # Stop sending signal to avoid jitter

    def cleanup(self):
        """Stop the servo and clean up GPIO."""
        self.pwm.stop()
        GPIO.cleanup()


class FansController:
  def __init__(self, chambers):
    self.chambers = chambers
    self.pwms = {}

    for chamber in chambers:
      GPIO.setup(chamber['fanPin'], GPIO.OUT)
      GPIO.output(chamber['fanPin'], GPIO.LOW)
      GPIO.setup(chamber['externalFanPin'], GPIO.OUT)
      GPIO.output(chamber['externalFanPin'], GPIO.LOW)
      GPIO.setup(chamber['fanServoPin'], GPIO.OUT)
      pwm = Servo(chamber['fanServoPin'])
      self.pwms[chamber['id']] = pwm


  def turnOnFan(self, chamber_id):
    for chamber in self.chambers:
      if chamber['id'] == chamber_id:
        GPIO.output(chamber['fanPin'], GPIO.HIGH)
        pwm = self.pwms[chamber_id]
        pwm.set_angle(50)
        break

  def turnOffFan(self, chamber_id):
    for chamber in self.chambers:
      if chamber['id'] == chamber_id:
        GPIO.output(chamber['fanPin'], GPIO.LOW)
        pwm = self.pwms[chamber_id]
        pwm.set_angle(0)
        break

  def turnOnExternalFan(self, chamber_id):
    for chamber in self.chambers:
       if chamber['id'] == chamber_id:
         GPIO.output(chamber['externalFanPin'], GPIO.HIGH)
         break

  def turnOffExternalFan(self, chamber_id):
    for chamber in self.chambers:
       if chamber['id'] == chamber_id:
         GPIO.output(chamber['externalFanPin'], GPIO.LOW)
         break

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    chambers = [
    {
      'id': 'c2edaa38-b3e6-426f-9d0f-6abffe007bf2',
      'whitePin': 21,
      'ledPin': 15,
      'pumpPin': 24,
      'heaterPin': 13,
      'peltierPin': 4,
      'chamberLocation': 4200,
      'waterLevelChannel': 2,
      'soilMoistureChannel': 0,
      'ledLightsActivated': False,
      'tempMuxChannel': 1,
      'fanPin': 23,
      'fanServoPin': 11,
      'externalFanPin': 22,
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
      'id': 'd9db68f0-e7c9-4135-bf96-a9f6ef568fea',
      'whitePin': 14,
      'ledPin': 20,
      'pumpPin': 18,
      'heaterPin': 19,
      'peltierPin': 17,
      'chamberLocation': 1200,
      'waterLevelChannel': 3,
      'soilMoistureChannel': 1,
      'ledLightsActivated': False,
      'tempMuxChannel': 0,
      'fanPin': 10,
      'fanServoPin': 25,
      'externalFanPin': 27,
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

    fans = FansController(chambers)
    while True:
      print('abrido')
      fans.turnOnFan(chambers[0]['id'])
      fans.turnOnFan(chambers[1]['id'])
      sleep(3)
      print('fechando')
      fans.turnOffFan(chambers[0]['id'])
      fans.turnOffFan(chambers[1]['id'])
      sleep(3)
