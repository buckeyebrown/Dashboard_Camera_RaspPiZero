import RPi.GPIO as GPIO
import time
import picamera

while (True):
	with picamera.PiCamera() as camera:
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(18,GPIO.OUT)
		print 'LED ON'
		GPIO.output(18, GPIO.HIGH)
		camera.start_preview()
		time.sleep(10)
		print 'LED off'
		GPIO.output(18,GPIO.LOW)
		time.sleep(10)
