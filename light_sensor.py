#!/usr/bin/python

import time
import Adafruit_GPIO.I2C as Adafruit_I2C

class TSL2561:
	i2c = None

	def __init__(self, address=0x39, debug=0, pause=0.8):
		self.i2c = Adafruit_I2C.Device(address, busnum=1)
