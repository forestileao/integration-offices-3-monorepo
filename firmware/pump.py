import RPi.GPIO as GPIO

class PumpController:
    def __init__(self, chambers, frequency=1000):
        self.frequency = frequency
        self.chambers = chambers

        for chamber in chambers:
            GPIO.setup(chamber['pumpPin'], GPIO.OUT)
            chamber['pwm'] = GPIO.PWM(chamber["pumpPin"], self.frequency)

            # Set up PWM
            chamber['pwm'].start(0)  # Start PWM with a duty cycle of 0 (motor off)


    def set_pump_speed(self, chamber_id, duty_cycle):
        for chamber in self.chambers:
            if chamber['id'] == chamber_id:
                pwm = chamber['pwm']
                if 0 <= duty_cycle <= 100:
                    pwm.ChangeDutyCycle(duty_cycle)


# Example usage
if __name__ == "__main__":
    pump = PumpController(pump_pin=18)
    pump.run_demo()
