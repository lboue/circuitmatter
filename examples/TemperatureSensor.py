"""Simple Temperature sensor."""

import circuitmatter as cm
from circuitmatter.device_types.lighting import on_off
from circuitmatter.device_types.sensor import temperature_sensor

import time
import board
from adafruit_bme280 import basic as adafruit_bme280

# Create sensor object, using the board's default I2C bus.
i2c = board.I2C()  # uses board.SCL and board.SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)

class LED(on_off.OnOffLight):
    def __init__(self, name, led):
        super().__init__(name)
        self._led = led

    def on(self, session):
        self._led.value = True

    def off(self, session):
        self._led.value = False

    def get_temp(self, session):
        return ((bme280.temperature)*100)


class TempSensorTest(temperature_sensor.TemperatureSensor):
    def __init__(self, name):
        super().__init__(name)
        self._temp = (bme280.temperature)*100


matter = cm.CircuitMatter(state_filename="test_data/device_state.json")
#led = LED("led1", digitalio.DigitalInOut(board.D13))
print(bme280.temperature)
tempSensor = TempSensorTest("TempSensor")
print(tempSensor._temp)

#matter.add_device(led)
matter.add_device(tempSensor)

while True:
    matter.process_packets()
