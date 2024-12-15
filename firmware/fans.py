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
      pwm = GPIO.PWM(chamber['fanServoPin'], 50)
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
