from pyPS4Controller.controller import Controller
from time import sleep
import RPi.GPIO as GPIO
from rpi_hardware_pwm import HardwarePWM
import board
import adafruit_ahtx0

SERVO_PIN = 19
SERVO_HZ = 50 # 20ms

MOTOR_PWM = 18
MOTOR_HZ = 1000
MOTOR_EN1 = 5
MOTOR_EN2 = 6

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

        #--GPIO--#
        # for motor direction control with software PWM
        # EN pin combos
        #   EN1 EN2 
        #   0   0   -> stop
        #   0   1   -> CW
        #   1   0   -> CCW    
        #   1   1   -> stop
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(MOTOR_EN1, GPIO.OUT)
        GPIO.setup(MOTOR_EN2, GPIO.OUT)
        GPIO.output(MOTOR_EN1, GPIO.LOW)
        GPIO.output(MOTOR_EN2, GPIO.LOW)
        # -1 for backward, 0 for stop, 1 for forward
        self.motor_state = 0

        #---Hardware PWM---#
        # Motor and servo control
        # ch0 is pin 18 | ch1 is pin 19
        # DO NOT USE these pins with GPIO - will need to reboot to enable again
        self.motor_pwm_hw = HardwarePWM(pwm_channel=0, hz=MOTOR_HZ)
        self.motor_pwm_hw.start(0)
        self.servo_pwm_hw = HardwarePWM(pwm_channel=1, hz=SERVO_HZ)
        self.servo_pwm_hw.start(7.5)

        #---Sensor Setup---#
        self.sensor = adafruit_ahtx0.AHTx0(board.I2C())

    def on_playstation_button_press(self):
        print("Exiting...")
        controller.stop = True
    
    def on_x_press(self):
        print("Current Temperature: %.2f\u00B0F" % ((32+1.8*self.sensor.temperature)))
    
    def on_circle_press(self):
        print("Current Relative Humidity: %.2f%%" % self.sensor.relative_humidity)
    
    def on_R3_left(self, value):
        prop_left = -value / 32786
        duty_percent = 7.5 - (prop_left**2)*5
        self.servo_pwm_hw.change_duty_cycle(duty_percent)

    def on_R3_right(self, value):
        prop_right = value / 32786
        duty_percent = 7.5 + (prop_right**2)*5
        self.servo_pwm_hw.change_duty_cycle(duty_percent)
        self.servo_pwm_hw.change_duty_cycle(duty_percent)

    def on_R3_x_at_rest(self):
        self.servo_pwm_hw.change_duty_cycle(7.5)


    def on_L3_up(self, value):
        prop_left = -value / 32786
        duty_percent = prop_left*60

        if self.motor_state != 1:
            GPIO.output(MOTOR_EN1, GPIO.LOW)
            GPIO.output(MOTOR_EN2, GPIO.HIGH)
            self.motor_state = 1

        self.motor_pwm_hw.change_duty_cycle(duty_percent)

    def on_L3_down(self, value):
        prop_left = value / 32786
        duty_percent = prop_left*40

        if self.motor_state != -1:
            GPIO.output(MOTOR_EN1, GPIO.HIGH)
            GPIO.output(MOTOR_EN2, GPIO.LOW)
            self.motor_state = -1
            
        self.motor_pwm_hw.change_duty_cycle(duty_percent)

    def on_L3_y_at_rest(self):
        if self.motor_state != 0:
            GPIO.output(MOTOR_EN1, GPIO.LOW)
            GPIO.output(MOTOR_EN2, GPIO.LOW)
            self.motor_state = 0

        self.motor_pwm_hw.change_duty_cycle(0)

try:
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    # you can start listening before controller is paired, as long as you pair it within the timeout window
    controller.listen(timeout=60)

finally:
    print("Cleaning up GPIO pins")
    GPIO.cleanup()
