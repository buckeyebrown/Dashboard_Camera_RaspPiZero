import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(15, GPIO.OUT)
GPIO.setwarnings(False)
var=1

while var==1:
	GPIO.output(15, True)
	time.sleep(1)
