from pyPS4Controller.controller import Controller
from time import sleep
import RPi.GPIO as GPIO
from rpi_harware_pwm import HardwarePWM

SERVO_PIN = 13
SERVO_HZ = 50 # 20ms

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        #--GPIO--#
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(SERVO_PIN, GPIO.OUT)
        #self.pwm = GPIO.PWM(SERVO_PIN, SERVO_HZ)
        #self.pwm.start(0)
        #--HardwarePWM--#
        self.pwm = HardwarePWM(pwm_channel=0, hz=SERVO_HZ, chip=0)
        self.pwm.start(0)

    def on_x_press(self):
       print("Hello world")

    def on_x_release(self):
       print("Goodbye world")

    def on_R3_left(self, value):
        prop_left = -value / 32786
        duty_percent = 7.5 - prop_left*5
        #self.pwm.ChangeDutyCycle(duty_percent)
        self.pwm.change_duty_cycle(duty_percent)

    def on_R3_right(self, value):
        prop_right = value / 32786
        duty_percent = 7.5 - prop_right*5
        #self.pwm.ChangeDutyCycle(duty_percent)
        self.pwm.change_duty_cycle(duty_percent)

    def on_R3_x_at_rest(self):
        self.pwm.change_duty_cycle(7.5)


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
# you can start listening before controller is paired, as long as you pair it within the timeout window
controller.listen(timeout=60)
