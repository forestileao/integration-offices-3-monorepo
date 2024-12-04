import RPi.GPIO as GPIO
from lamp import LampsManager
from temp_humidity import TempHumidity
from pump import PumpController
from stepper import StepperController
from adc import AdcController
from .http import HttpApi

GPIO.setmode(GPIO.BCM)


chambers = [
    {
      'id': 'asdkasdjasd',
      'whitePin': 17,
      'ledPin': 27,
      'pumpPin': 18,
      'chamberLocation': 20
    },
    {
      'id': 'asdkasdjasd',
      'whitePin': 22,
      'ledPin': 23,
      'pumpPin': 24,
      'chamberLocation': 200
    },
]

EN=9

# Direction pin
X_DIR=5
Y_DIR=7

# Step pin
X_STP=6
Y_STP=8


class Firmware:

  def __init__(self):
    self.lamps_manager = LampsManager(chambers)
    self.temp_humidity = TempHumidity()
    self.pump_controller = PumpController(chambers)
    self.stepper = StepperController(X_DIR, X_STP, Y_DIR, Y_STP, EN)
    self.adc = AdcController()
    self.api = HttpApi()

  def take_photo(self, chamber_id):
      """Take a photo with the camera."""
      # Simulating camera control logic here (to be replaced with actual control code)
      img_bin = b'fake_binary_data'  # Replace with actual image data
      return img_bin


  def sendPhoto(self, chamber_id, img_bin):
      """Send photo to server."""
      response = requests.post(base_url + '/photo/' + chamber_id, files={'file': img_bin})
      return response.status_code


  def control_lights(self, parameters):
      """Control the lights based on the lighting schedule."""
      global lights_state
      if my_schedule in parameters['lightingSchedule'] and lights_state == 'off':
          lights_state = 'on'
          print("Turning lights on...")
          # Actual code to turn on lights
      elif my_schedule not in parameters['lightingSchedule'] and lights_state == 'on':
          lights_state = 'off'
          print("Turning lights off...")
          # Actual code to turn off lights


  def control_temperature(self, parameters):
      """Control temperature (turn on heating or cooling)."""
      global heating_resistor, peltier

      if temperature < parameters['temperature'] and heating_resistor == 'off':
          heating_resistor = 'on'
          print("Turning heating resistor on...")
          # Actual code to turn on heating resistor
      elif temperature > parameters['temperature'] and peltier == 'off':
          peltier = 'on'
          print("Turning peltier on...")
          # Actual code to turn on peltier
      elif temperature > parameters['temperature'] and heating_resistor == 'on':
          heating_resistor = 'off'
          print("Turning heating resistor off...")
          # Actual code to turn off heating resistor


  def control_soil_moisture(self, parameters):
      """Control soil moisture."""
      if soil_moisture < parameters['soil_moisture']:
          print("Watering the plant...")
          # Actual code to water the plant


def main():

    firmware = Firmware()

    while True:
        for chamber in chambers:
            chamber_id = chamber['id']
            parameters = getParameters(chamber_id)  # Get the parameters for the chamber

            # Control lights based on schedule
            control_lights(parameters)

            # Control temperature
            control_temperature(parameters)

            # Control soil moisture
            control_soil_moisture(parameters)

            # Send metrics periodically
            if is_send_metrics_time:
                sendMetrics(chamber_id)

            # Send photo periodically
            if is_send_photo_time:
                img_bin = take_photo(chamber_id)
                sendPhoto(chamber_id, img_bin)

            # Sleep to avoid tight loop, adjust the sleep time as needed
            sleep(10)  # Adjust sleep time (10 seconds) for the loop


if __name__ == '__main__':
    main()
