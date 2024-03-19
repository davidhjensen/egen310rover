import board
import adafruit_ahtx0

sensor = adafruit_ahtx0.AHTx0(board.I2C())

print("Current Temperature: %.2f\u00B0F" % ((32+1.8*sensor.temperature)))
print("Current Relative Humidity: %.2f%%" % sensor.relative_humidity)
