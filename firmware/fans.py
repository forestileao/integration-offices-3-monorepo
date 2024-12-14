import RPi.GPIO as GPIO


class FansController:
  def __init__(self, chambers):
    self.chambers = chambers

    for chamber in chambers:
      GPIO.setup(chamber['fanPin'], GPIO.OUT)
      GPIO.output(chamber['fanPin'], GPIO.LOW)


  def turnOnFan(self, chamber_id):
    for chamber in self.chambers:
      if chamber['id'] == chamber_id:
        GPIO.output(chamber['fanPin'], GPIO.HIGH)
        break

  def turnOffFan(self, chamber_id):
    for chamber in self.chambers:
      if chamber['id'] == chamber_id:
        GPIO.output(chamber['fanPin'], GPIO.LOW)
        break
