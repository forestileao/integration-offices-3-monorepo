import RPi.GPIO as GPIO
from lamp import LampsManager
from temp_humidity import TempHumidity
from pump import PumpController
from stepper import StepperController
from adc import AdcController
from http_api import HttpApi
from photo import CameraController
from timer_pkg import Timer
from multiplexer import Multiplexer
from fans import FansController

from time import sleep
import datetime

GPIO.setmode(GPIO.BCM)


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

EN=9

# Direction pin
X_DIR=5
Y_DIR=7

# Step pin
X_STP=6
Y_STP=8

END1=10
END2=11


class Firmware:

  def __init__(self):
    self.multiplexer = Multiplexer()
    self.lamps_manager = LampsManager(chambers)
    self.temp_humidity = TempHumidity(chambers, self.multiplexer)
    self.pump_controller = PumpController(chambers)
    self.stepper = StepperController(X_DIR, X_STP, Y_DIR, Y_STP, EN, END1, END2)
    self.adc = AdcController(self.multiplexer)
    self.api = HttpApi()
    self.camera = CameraController()
    self.current_location = 0
    self.stepper.move_to_initial_position()
    self.fans_controller = FansController(chambers)


  def get_parameters(self, chamber_id):
    return self.api.get_parameters(chamber_id)


  def get_chamber(chamber_id):
    for chamber in chambers:
      if chamber['id'] == chamber_id:
        return chamber
    return None

  def take_photo(self, chamber_id):
    chamber = self.get_chamber(chamber_id)

    led_status = chamber['ledLightsActivated']

    self.lamps_manager.turnOffLedLamp(chamber_id)
    sleep(0.1)
    self.lamps_manager.turnOnWhiteLamp(chamber_id)
    img_bin = self.camera.capture_image()
    self.lamps_manager.turnOffWhiteLamp(chamber_id)
    sleep(0.1)

    if led_status:
      self.lamps_manager.turnOnLedLamp(chamber_id)

    return img_bin


  def sendPhoto(self, chamber_id, img_bin):
    if self.api.send_photo(chamber_id, img_bin):
        print("Photo sent successfully")
    else:
        print("Failed to send photo")


  def control_lights(self, chamber_Id, parameters):
      # Get current time as a datetime object
      current_time = datetime.now().time()

      # Parse the lighting routine times
      lighting_routine_lower_time = datetime.strptime(parameters['lightingRoutine'].split('/')[0], '%H:%M').time()
      lighting_routine_upper_time = datetime.strptime(parameters['lightingRoutine'].split('/')[1], '%H:%M').time()

      # Check if current time falls within the lighting routine
      if lighting_routine_lower_time <= current_time <= lighting_routine_upper_time:
          self.lamps_manager.turnOnLedLamp(chamber_Id)
          print("Turning on LED lamp for chamber:", chamber_Id)
          for chamber in chambers:
              if chamber['id'] == chamber_Id:
                  chamber['ledLightsActivated'] = True
      else:
          self.lamps_manager.turnOffLedLamp(chamber_Id)
          print("Turning off LED lamp for chamber:", chamber_Id)
          for chamber in chambers:
              if chamber['id'] == chamber_Id:
                  chamber['ledLightsActivated'] = False


  def control_ventilation(self, chamber_id, parameters):
    # Get current time as a datetime object
    current_time = datetime.now().time()

    # Parse the ventilation schedule times
    ventilation_schedule_lower_time = datetime.strptime(parameters['ventilationSchedule'].split('/')[0], '%H:%M').time()
    ventilation_schedule_upper_time = datetime.strptime(parameters['ventilationSchedule'].split('/')[1], '%H:%M').time()

    # Check if current time fallsstrptime within the ventilation schedule
    if ventilation_schedule_lower_time <= current_time <= ventilation_schedule_upper_time:
        self.fans_controller.turnOnFan(chamber_id)
        print("Turning on fan for chamber:", chamber_id)
    else:
        self.fans_controller.turnOffFan(chamber_id)
        print("Turning off fan for chamber:", chamber_id)

  def control_temperature(self, chamber_id, parameters):
    temperature = self.temp_humidity.read_temperature(chamber_id)
    print("Temperature for chamber", chamber_id, temperature)

    if temperature < int(parameters['temperatureRange']):
        self.temp_humidity.turn_on_heater(chamber_id)
        self.temp_humidity.turn_off_peltier(chamber_id)
        print("Turning on heater for chamber: ", chamber_id)
    elif temperature > int(parameters['temperatureRange']):
        self.temp_humidity.turn_off_heater(chamber_id)
        self.temp_humidity.turn_on_peltier(chamber_id)
        print("Turning on peltier for chamber: ", chamber_id)
    else:
        self.temp_humidity.turn_off_heater(chamber_id)
        self.temp_humidity.turn_off_peltier(chamber_id)
        print("Turning off heater and peltier for chamber: ", chamber_id)

  def control_soil_moisture(self, chamber_id, parameters):
      """Control soil moisture."""
      chamber = self.get_chamber(chamber_id)
      channel = chamber['soilMoistureChannel']
      soil_moisture = self.adc.read_value(channel)
      desired_soil_moisture = int(parameters['soilMoistureLowerLimit'])

      if soil_moisture < desired_soil_moisture:
          print("Turning on pump for chamber: ", chamber_id)
          self.pump_controller.set_pump_speed(chamber_id, 50)
          sleep(3)
          print("Turning off pump for chamber: ", chamber_id)
          self.pump_controller.set_pump_speed(chamber_id, 0)

  def send_metrics(self, chamber_id):
    temperature = self.temp_humidity.read_temperature(chamber_id)
    humidity = self.temp_humidity.read_humidity(chamber_id)

    chamber = self.get_chamber(chamber_id)

    soil_moisture = self.adc.read_value(chamber['soilMoistureChannel'])
    water_level = self.adc.read_value(chamber['waterLevelChannel'])

    soil_moisture = ((700 - soil_moisture)/500) * 100
    water_level = ((700 - water_level)/500) * 100

    if self.api.send_metrics(chamber_id, soil_moisture, temperature, humidity, water_level):
        print("Metrics sent successfully")
    else:
        print("Failed to send metrics")

  def move_camera(self, chamber_id):
    chamber = self.get_chamber(chamber_id)
    chamber_location = chamber['chamberLocation']

    if chamber_location > self.current_location:
      self.stepper.move_up(chamber_location - self.current_location)
    elif chamber_location < self.current_location:
      self.stepper.move_down(self.current_location - chamber_location)

    self.current_location = chamber_location

def main():

    firmware = Firmware()
    photoTimer = Timer()
    metricsTimer = Timer()
    photoTimer.start()
    metricsTimer.start()

    while True:
        for chamber in chambers:
            chamber_id = chamber['id']
            chamber['parameters'] = firmware.get_parameters(chamber_id)

            # Control lights based on schedule
            firmware.control_lights(chamber_id, parameters=chamber['parameters'])

            # Control temperature
            firmware.control_temperature(chamber_id, parameters=chamber['parameters'])

            # Control ventilation
            firmware.control_ventilation(chamber_id, parameters=chamber['parameters'])

            # Control soil moisture
            firmware.control_soil_moisture(chamber_id, parameters=chamber['parameters'])

            # Send metrics periodically
            if metricsTimer.elapsed_time() > 60:
                firmware.sendMetrics(chamber_id)
                metricsTimer.reset()

            if int(chamber['parameters']['photoCaptureFrequency']) > 0 and photoTimer.elapsed_time() / 60 > int(chamber['parameters']['photoCaptureFrequency']):
                firmware.move_camera(chamber_id)
                img_bin = firmware.take_photo(chamber_id)
                firmware.sendPhoto(chamber_id, img_bin)
                photoTimer.reset()

            # Sleep to avoid tight loop, adjust the sleep time as needed
            sleep(10)  # Adjust sleep time (10 seconds) for the loop


if __name__ == '__main__':
    main()
