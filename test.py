from pyPS4Controller.controller import Controller
from time import sleep
import RPi.GPIO as GPIO

SERVO_PIN = 4
SERVO_HZ = 50 # 20ms

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SERVO_PIN, GPIO.OUT)
        self.pwm = GPIO.PWM(SERVO_PIN, SERVO_HZ)
        self.pwm.start(0)

    def on_x_press(self):
       print("Hello world")

    def on_x_release(self):
       print("Goodbye world")

    def on_L2_press(self, value):
        proportion = (32768 + value) / (32786*2)
        duty_percent = 2.5 + proportion*10
        print(duty_percent)
        self.pwm.ChangeDutyCycle(duty_percent)

    def on_L2_release(self):
        print("0")
        self.pwm.ChangeDutyCycle(2.5)


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
# you can start listening before controller is paired, as long as you pair it within the timeout window
controller.listen(timeout=60)
