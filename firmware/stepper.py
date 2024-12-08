import RPi.GPIO as GPIO
import time

class StepperController:
    def __init__(self, x_dir_pin, x_step_pin, y_dir_pin, y_step_pin, enable_pin, end1_pin, end2_pin, delay_time_microseconds=300):
        """
        Initialize the stepper motor controller.

        :param x_dir_pin: GPIO pin for X-axis direction control.
        :param x_step_pin: GPIO pin for X-axis step control.
        :param y_dir_pin: GPIO pin for Y-axis direction control.
        :param y_step_pin: GPIO pin for Y-axis step control.
        :param enable_pin: GPIO pin to enable/disable the motor driver.
        :param delay_time_microseconds: Delay time between steps in microseconds.
        """
        self.x_dir_pin = x_dir_pin
        self.x_step_pin = x_step_pin
        self.y_dir_pin = y_dir_pin
        self.y_step_pin = y_step_pin
        self.enable_pin = enable_pin
        self.end1_pin = end1_pin
        self.end2_pin = end2_pin
        self.delay_time = delay_time_microseconds / 1_000_000  # Convert to seconds for `time.sleep`

        GPIO.setup(self.x_dir_pin, GPIO.OUT)
        GPIO.setup(self.x_step_pin, GPIO.OUT)
        GPIO.setup(self.y_dir_pin, GPIO.OUT)
        GPIO.setup(self.y_step_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.setup(self.end1_pin, GPIO.IN)
        GPIO.setup(self.end2_pin, GPIO.IN)

        # Enable motor driver
        GPIO.output(self.enable_pin, GPIO.LOW)

    def move_steps(self, x_dir, y_dir, steps):
        """
        Move the stepper motor a specified number of steps.

        :param x_dir: Direction for X-axis (True for forward, False for backward).
        :param y_dir: Direction for Y-axis (True for forward, False for backward).
        :param steps: Number of steps to move.
        """
        GPIO.output(self.x_dir_pin, x_dir)
        GPIO.output(self.y_dir_pin, y_dir)
        is_move_down = x_dir and not y_dir
        is_move_left = x_dir and y_dir

        for _ in range(steps):

            if is_move_down and self.check_end1():
                print("End1 reached")
                break

            if is_move_left and self.check_end2():
                print("End2 reached")
                break

            GPIO.output(self.x_step_pin, GPIO.HIGH)
            GPIO.output(self.y_step_pin, GPIO.HIGH)
            time.sleep(self.delay_time)
            GPIO.output(self.x_step_pin, GPIO.LOW)
            GPIO.output(self.y_step_pin, GPIO.LOW)
            time.sleep(self.delay_time)

    def move_up(self, steps):
        print(f"Moving up with {steps} steps.")
        self.move_steps(False, True, steps)

    def move_down(self, steps):
        print(f"Moving down with {steps} steps.")
        self.move_steps(True, False, steps)

    def move_left(self, steps):
        print(f"Moving left with {steps} steps.")
        self.move_steps(True, True, steps)

    def move_right(self, steps):
        print(f"Moving right with {steps} steps.")
        self.move_steps(False, False, steps)

    def cleanup(self):
        """
        Clean up GPIO settings.
        """
        GPIO.cleanup()

    def check_end1(self):
        return GPIO.input(self.end1_pin) == GPIO.HIGH

    def check_end2(self):
        return GPIO.input(self.end2_pin) == GPIO.HIGH
