from time import sleep
import RPi.GPIO as GPIO
from rpi_hardware_pwm import HardwarePWM

MOTOR_PWM = 13
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
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_EN1, GPIO.OUT)
GPIO.setup(MOTOR_EN2, GPIO.OUT)
GPIO.output(MOTOR_EN1, GPIO.LOW)
GPIO.output(MOTOR_EN2, GPIO.LOW)


#---Software PWM---#
GPIO.setup(SERVO_PIN, GPIO.OUT)
motor_pwm_sw = GPIO.PWM(MOTOR_PWM, MOTOR_HZ)
motor_pwm_sw.start(0)

# forward for 2 sec at 50% duty
GPIO.output(MOTOR_EN1, GPIO.LOW)
GPIO.output(MOTOR_EN2, GPIO.HIGH)
motor_pwm_sw.ChangeDutyCycle(50)
sleep(2)
motor_pwm_sw.ChangeDutyCycle(0)

# reverse for 2 sec at 25% duty
GPIO.output(MOTOR_EN1, GPIO.HIGH)
GPIO.output(MOTOR_EN2, GPIO.LOW)
motor_pwm_sw.ChangeDutyCycle(25)
sleep(2)
motor_pwm_sw.ChangeDutyCycle(0)

# stop and end PWM
GPIO.output(MOTOR_EN1, GPIO.LOW)
GPIO.output(MOTOR_EN2, GPIO.LOW)
motor_pwm_sw.stop()


#---Hardware PWM---#
# ch0 is pin 12 | ch1 is pin 13
motor_pwm_hw = HardwarePWM(pwm_channel=1, hz=MOTOR_HZ)
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

# ensure all pins are reset
GPIO.cleanup()