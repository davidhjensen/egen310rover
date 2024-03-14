from time import sleep
import RPi.GPIO as GPIO

# ONLY set this to pin 12 or 13 - 18 and 19 reserved for hardware PWM
SERVO_PWM = 13
SERVO_HZ = 50

#---Software PWM---#
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PWM, GPIO.OUT)
motor_pwm_sw = GPIO.PWM(SERVO_PWM, SERVO_HZ)

# set to center
motor_pwm_sw.start(7.5)
sleep(1)

# move to extremes
motor_pwm_sw.start(2.5)
sleep(1)
motor_pwm_sw.start(12.5)
sleep(2)

# center
motor_pwm_sw.start(7.5)
sleep(1)

GPIO.cleanup()
