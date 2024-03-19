import board
import adafruit_ahtx0

sensor = adafruit_ahtx0.AHTx0(board.I2C())

print("Current Temperature: %.2f%cF" % ((32+1.8*self.sensor.temperature), 248))
print("Current Relative Humidity: %.2f%%" % self.sensor.relative_humidity)
