import RPi.GPIO as GPIO
import time
from time import sleep

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
        self.delay_time = delay_time_microseconds / 1000000  # Convert to seconds for `time.sleep`

        GPIO.setup(self.x_dir_pin, GPIO.OUT)
        GPIO.setup(self.x_step_pin, GPIO.OUT)
        GPIO.setup(self.y_dir_pin, GPIO.OUT)
        GPIO.setup(self.y_step_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.setup(self.end1_pin, GPIO.IN,  pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.end2_pin, GPIO.IN,  pull_up_down=GPIO.PUD_DOWN)

        # Disanlr when idle motor driver
        GPIO.output(self.enable_pin, GPIO.HIGH)

    def move_to_initial_position(self):
        GPIO.output(self.x_dir_pin, True)
        GPIO.output(self.y_dir_pin, False)
        GPIO.output(self.enable_pin, GPIO.LOW)

        while not self.check_end1():
            GPIO.output(self.x_step_pin, GPIO.HIGH)
            time.sleep(self.delay_time)
            GPIO.output(self.y_step_pin, GPIO.HIGH)
            time.sleep(self.delay_time)
            GPIO.output(self.x_step_pin, GPIO.LOW)
            time.sleep(self.delay_time)
            GPIO.output(self.y_step_pin, GPIO.LOW)
            time.sleep(self.delay_time)


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
        is_move_right = not x_dir and not y_dir

        GPIO.output(self.enable_pin, GPIO.LOW)

        for _ in range(steps):

            if is_move_down and self.check_end1():
                print("End1 reached")
                break

            if is_move_right and self.check_end2():
                print("End2 reached")
                break

            GPIO.output(self.x_step_pin, GPIO.HIGH)
            time.sleep(self.delay_time)
            GPIO.output(self.y_step_pin, GPIO.HIGH)
            time.sleep(self.delay_time)
            GPIO.output(self.x_step_pin, GPIO.LOW)
            time.sleep(self.delay_time)
            GPIO.output(self.y_step_pin, GPIO.LOW)
            time.sleep(self.delay_time)
        GPIO.output(self.enable_pin, GPIO.HIGH)

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
        GPIO.output(self.enable_pin, GPIO.HIGH)

    def check_end1(self):
        result = GPIO.input(self.end1_pin)

        if result == GPIO.HIGH:
            sleep(300 / 1_000_000)
            result = GPIO.input(self.end1_pin)
        return result == GPIO.HIGH

    def check_end2(self):
        result = GPIO.input(self.end2_pin)
        if result == GPIO.HIGH:
            sleep(300 / 1_000_000)
            result = GPIO.input(self.end2_pin)
        return result == GPIO.HIGH

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    sc = StepperController(5,6,7,8,9,16,26)

    # go to initial position
    sc.move_to_initial_position()
    sleep(2)
    sc.move_up(1200)
    sleep(4)
    sc.move_up(3000)
    sleep(4)
    sc.move_to_initial_position()

    try:
        while True:
            usr_in = input("[w]Cima\n[s]Baixo\n[a]Esquerda\n[d]Direita\n")
            if usr_in == 'w':
                sc.move_up(200)
            elif usr_in == 's':
                sc.move_down(200)
            elif usr_in == 'a':
                sc.move_left(200)
            elif usr_in == 'd':
                sc.move_right(200)
            elif usr_in == 'i':
                sc.move_to_initial_position()
    except KeyboardInterrupt:
        sc.cleanup()
        print("Exiting...")
        exit(0)
