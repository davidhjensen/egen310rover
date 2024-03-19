import board
import adafruit_ahtx0

sensor = adafruit_ahtx0.AHTx0(board.I2C())

print("Temperature: %.2f degC\nHumidity: %.2f%%" % (sensor.temperature, sensor.relative_humidity))
