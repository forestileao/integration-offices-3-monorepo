import RPi.GPIO as GPIO

class LampsManager:
  def __init__(self, chambers):
    for chamber in chambers:
      GPIO.setup(chamber['whitePin'], GPIO.OUT)
      GPIO.setup(chamber['ledPin'], GPIO.OUT)

    self.chambers = chambers


  def turnOnWhiteLamp(self, chamber_id):
    for chamber in self.chambers:
      if chamber['id'] == chamber_id:
        GPIO.output(chamber['whitePin'], GPIO.HIGH)
        break

  def turnOffWhiteLamp(self, chamber_id):
    for chamber in self.chambers:
      if chamber['id'] == chamber_id:
        GPIO.output(chamber['whitePin'], GPIO.LOW)
        break

  def turnOnLedLamp(self, chamber_id):
    for chamber in self.chambers:
      if chamber['id'] == chamber_id:
        GPIO.output(chamber['ledPin'], GPIO.HIGH)
        break

  def turnOffLedLamp(self, chamber_id):
    for chamber in self.chambers:
      if chamber['id'] == chamber_id:
        GPIO.output(chamber['ledPin'], GPIO.LOW)
        break
