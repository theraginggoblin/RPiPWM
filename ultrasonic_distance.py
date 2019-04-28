import RPi.GPIO as GPIO
import time

trigger_pin = 7
echo_pin = 11
led_pin = 40

def pin_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(trigger_pin, GPIO.OUT)
    GPIO.output(trigger_pin, GPIO.LOW)
    GPIO.setup(echo_pin, GPIO.IN)
    GPIO.setup(led_pin, GPIO.OUT)
    GPIO.output(led_pin, GPIO.LOW)

def get_distance():
    GPIO.output(trigger_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, GPIO.LOW)

    start_time = 0
    end_time = 0

    while GPIO.input(echo_pin) == 0:
        start_time = time.time()
    while GPIO.input(echo_pin) == 1:
        end_time = time.time()

    duration = end_time - start_time

    return round(duration * 17150, 2)

pin_setup()
time.sleep(2)

pwm_led = GPIO.PWM(led_pin, 100)
pwm_led.start(0)

try:
    while 1:
        distance = get_distance()
        print('Distance %scm' % distance)

        pwm_led.ChangeDutyCycle(distance / 4)

        time.sleep(0.5)
except KeyboardInterrupt:
    pwm_led.stop()
    GPIO.cleanup()
