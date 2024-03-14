from time import sleep
import RPi.GPIO as GPIO
from rpi_hardware_pwm import HardwarePWM

MOTOR_HZ = 1000
MOTOR_EN1 = 5
MOTOR_EN2 = 6

# for motor direction control with software GPIO
# EN pin combos
#   EN1 EN2 
#   0   0   -> stop
#   0   1   -> CW
#   1   0   -> CCW    
#   1   1   -> stop
def motor_dir_GPIO_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MOTOR_EN1, GPIO.OUT)
    GPIO.setup(MOTOR_EN2, GPIO.OUT)
    GPIO.output(MOTOR_EN1, GPIO.LOW)
    GPIO.output(MOTOR_EN2, GPIO.LOW)


#---Hardware PWM---#
# ch0 is pin 18 | ch1 is pin 19
motor_dir_GPIO_setup()
motor_pwm_hw = HardwarePWM(pwm_channel=0, hz=MOTOR_HZ)
motor_pwm_hw.start(0)

# forward for 2 sec at 50% duty
GPIO.output(MOTOR_EN1, GPIO.LOW)
GPIO.output(MOTOR_EN2, GPIO.HIGH)
motor_pwm_hw.change_duty_cycle(50)
sleep(2)
motor_pwm_hw.change_duty_cycle(0)

# reverse for 2 sec at 25% duty
GPIO.output(MOTOR_EN1, GPIO.HIGH)
GPIO.output(MOTOR_EN2, GPIO.LOW)
motor_pwm_hw.change_duty_cycle(25)
sleep(2)
motor_pwm_hw.change_duty_cycle(0)

# stop and end PWM
GPIO.output(MOTOR_EN1, GPIO.LOW)
GPIO.output(MOTOR_EN2, GPIO.LOW)
motor_pwm_hw.stop()
GPIO.cleanup()