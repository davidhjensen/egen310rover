from pyPS4Controller.controller import Controller
from time import sleep
import RPi.GPIO as GPIO
from rpi_hardware_pwm import HardwarePWM

SERVO_PIN = 12
SERVO_HZ = 50 # 20ms

MOTOR_PWM = 13
MOTOR_EN1 = 5
MOTOR_EN2 = 6

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

        #--GPIO--#
        # for motor direction control with software PWM
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(MOTOR_EN1, GPIO.OUT)
        GPIO.setup(MOTOR_EN2, GPIO.OUT)
        GPIO.output(MOTOR_EN1, GPIO.HIGH)
        GPIO.output(MOTOR_EN2, GPIO.LOW)

        GPIO.setup(SERVO_PIN, GPIO.OUT)
        self.servo_pwm = GPIO.PWM(SERVO_PIN, SERVO_HZ)
        self.servo_pwm.start(0)

        GPIO.setup(MOTOR_PWM, GPIO.OUT)
        self.motor_pwm = GPIO.PWM(MOTOR_PWM, 1000)
        self.motor_pwm.start(0)

        #--HardwarePWM--#
        #self.servo_pwm = HardwarePWM(pwm_channel=1, hz=SERVO_HZ, chip=0)
        #self.servo_pwm.start(0)
        '''
        self.motor_pwm = HardwarePWM(pwm_channel=1, hz=1000, chip=0)
        self.motor_pwm.start(0)
        '''

    def on_R3_left(self, value):
        prop_left = -value / 32786
        duty_percent = 7.5 - prop_left*5
        self.servo_pwm.ChangeDutyCycle(duty_percent)
        #self.servo_pwm.change_duty_cycle(duty_percent)

    def on_R3_right(self, value):
        prop_right = value / 32786
        duty_percent = 7.5 + prop_right*5
        self.servo_pwm.ChangeDutyCycle(duty_percent)
        #self.servo_pwm.change_duty_cycle(duty_percent)

    def on_R3_x_at_rest(self):
        self.servo_pwm.ChangeDutyCycle(7.5)
        #self.servo_pwm.change_duty_cycle(7.5)

    def on_R3_up(self, value):
        prop_left = -value / 32786
        duty_percent = prop_left*50
        print(duty_percent)
        #self.motor_pwm.change_duty_cycle(duty_percent)
        self.motor_pwm.ChangeDutyCycle(duty_percent)

    def on_R3_y_at_rest(self):
        self.motor_pwm.ChangeDutyCycle(0)

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
# you can start listening before controller is paired, as long as you pair it within the timeout window
controller.listen(timeout=60)
