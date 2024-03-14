from time import sleep
import RPi.GPIO as GPIO
from rpi_hardware_pwm import HardwarePWM

SERVO_HZ = 50
# Servo takes duty cycle between 2.5 and 12.5 with 7.5 being middle

#---Hardware PWM---#
# ch0 is pin 18 | ch1 is pin 19
# DO NOT USE these pins with GPIO - will need to reboot to enable again
servo_pwm_hw = HardwarePWM(pwm_channel=1, hz=SERVO_HZ)

# set to center
servo_pwm_hw.start(7.5)
sleep(1)

# move to extremes
servo_pwm_hw.start(2.5)
sleep(1)
servo_pwm_hw.start(12.5)
sleep(2)

# center
servo_pwm_hw.start(7.5)
sleep(1)