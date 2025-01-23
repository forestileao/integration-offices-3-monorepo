import RPi.GPIO as GPIO
import time

# Define the servo pin
servo_pin = 0  # Change to the actual GPIO pin used

# Set up GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(servo_pin, GPIO.OUT)

# Set up PWM (50Hz frequency for servos)
pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz
pwm.start(0)  # Start with 0% duty cycle

def set_servo_angle(angle):
    """Set the servo to a specific angle (0 to 180 degrees)."""
    duty_cycle = (angle / 18.0) + 2.5  # Convert angle to duty cycle
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)  # Allow servo time to move
    pwm.ChangeDutyCycle(0)  # Stop sending signal to avoid jitter

try:
    set_servo_angle(0)
    time.sleep(0.5)
    set_servo_angle(50)
    time.sleep(0.5)

except KeyboardInterrupt:
    print("Stopping.")
finally:
    pwm.stop()
    GPIO.cleanup()

