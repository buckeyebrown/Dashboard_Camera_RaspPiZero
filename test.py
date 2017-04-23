import picamera
import time
import os
import errno
import sys
import RPi.GPIO as GPIO
import smbus
import logging
import pytz
from subprocess import call, Popen
from astral import Astral
from datetime import datetime

#Start the Raspberry Pi Camera
def startRaspCamera():
    turnOffIRLED()
    with picamera.PiCamera() as camera:
        #camera.start_preview()
        directory_path = getDirectoryPath()
        checkIfDirectoryExistsOrCreate(directory_path)
        filename = createFileName(directory_path)
        startRecording(filename, directory_path, camera)

    return

#Get the directory path for the videos being saved
def getDirectoryPath():
    filelocation = "/home/pi/recorded_videos/"
    foldername = time.strftime("%Y%m%d") + "_videos/"
    directory_path = filelocation + foldername

    return directory_path

def checkIfDirectoryExistsOrCreate(directory_path):
    if not os.path.exists(directory_path):
        try:
            original_mask = os.umask(0)
            print "the original mask is: "
            print original_mask
            print ""
            os.makedirs(directory_path, mode=0777)
        except OSError as error:
            if error.errno != errno.EEXIST:
                raise
        finally:
            os.umask(original_mask)

    return

def createFileName(directory_path):
    timestring = time.strftime("%Y%m%d-%H%M%S")
    filename = directory_path + "vid_" + timestring + ".h264"

    return filename

def startRecording(filename, directory_path, camera):
    camera.start_recording(filename, format='h264', quality=35)
    recordForADay(directory_path, camera)

    return

def recordForAnHour(camera):
    isItNight = checkIfNightSunset() 
    nightDayCheck(isItNight, camera)
    minute_counter = 0
    secondsInAnHour= 15
    #3600 is default value
    secondsInFifteenMinutes = 5
    #900 is default value

    while minute_counter < secondsInAnHour:
        #Check if it's night time every 15 minutes
        if ((minute_counter % secondsInFifteenMinutes) == 0):
            isItNight = checkIfNightSunset()
            nightDayCheck(isItNight, camera)
        camera.annotate_text = time.strftime("%H%M%S")
        camera.wait_recording(1)
        minute_counter += 1

    return

def recordForADay(directory_path, camera):
    logger = createLogger()
    recordForAnHour(camera)
    hour_counter = 1
    hoursInADay = 24

    for filename in camera.record_sequence([
        'clip01.h264', 'clip02.h264', 'clip03.h264'
    ]):
        print('Recording to %s' % filename)
        camera.wait_recording(10)
        command = 'MP4Box -add {0} {1}.mp4'.format(filename, filename)
        conv = Popen(command, shell=True)


    #while hour_counter < hoursInADay:
    #    splitVideoIntoHours(directory_path, camera)
    #    recordForAnHour(camera)
    camera.stop_recording()

    return

def splitVideoIntoHours(directory_path, camera):
    timestring = time.strftime("%H%M%S")

    filename = directory_path + "vid_" + timestring
    filename_1 = filename + ".h264"
    camera.split_recording(filename_1)
    command = 'MP4Box -add {0}.h264 {1}.mp4'.format(filename, filename)
    camera.wait_recording(1)
    camera.stop_recording()
    conv = Popen(command, shell=True)
    return

def checkIfNightSunset():
    city_name = 'Columbus'
    a = Astral()
    a.solar_depression = 'civil'
    city = a[city_name]
    isItNight = False
    now = datetime.now(pytz.utc)
    sun = city.sun(date=now, local=True)
    print sun['dusk']
    if now >= sun['sunset'] or now <= sun['sunrise']:
    	isItNight = True
	print "nighttime"
    else:
	print "daytime"
    return isItNight

def isItNightTime(visible_spectrum_val):
    nightTime = False
    minDayTimeLux = 100
    if (visible_spectrum_val < minDayTimeLux):
        nightTime = True
        print "It is Night Time! Activating Camera Night Mode."
    else:
        print "It is Day Time! Activating Camera Day Mode."

    return nightTime

# Turn on Infrared LED when Night
def turnLEDOnOrOff(isItNight):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarning(False)
    GPIO.setup(18, GPIO.OUT)
    if (isItNight == True):
        GPIO.output(18, GPIO.HIGH)
    else:
        GPIO.output(18, GPIO.LOW)

    return

def obtainLightSensorReading():
    logger = createLogger()
    # Get I2C bus
    bus = smbus.SMBus(1)

    # TSL2561 Address = 0x29
    # Select control register, 0x00, with command register, 0x80
    #   0x03 is Power ON Mode
    bus.write_byte_data(0x29, 0x00 | 0x80, 0x03)

    # Select timing register, 0x01, with command register, 0x80
    #   0x02    Nominal Integration Time = 402ms
    bus.write_byte_data(0x29, 0x01 | 0x80, 0x02)

    # Sleep for 0.5 seconds
    time.sleep(0.5)


    # Read data back from 0x0C with command register, 0x80, 2 bytes
    # ch0 LSB, ch0 MSB
    full_spectrum_data = bus.read_i2c_block_data(0x29, 0x0C | 0x80, 2)

    # Full spectrum = IR + Visible

    # Read data back from 0x0E with command register, 0x80, 2 bytes
    # ch1 LSB, ch1 MSB
    infrared_data = bus.read_i2c_block_data(0x29, 0x0E | 0x80, 2)

    # Convert the data
    full_spectrum_val = full_spectrum_data[1] * 256 + full_spectrum_data[0]
    infrared_val = infrared_data[1] * 256 + infrared_data[0]
    visible_spectrum_val = full_spectrum_val - infrared_val

    # Print data to screen
    print "Full Spectrum Light (IR + Visibile) : %d lux" % full_spectrum_val
    logger.info("Full Spectrum Light (IR + Visibile) : %d lux" % full_spectrum_val)
    print "Infrared Value : %d lux" % infrared_val
    logger.info("Infrared Value : %d lux" % infrared_val)
    print "Visibile Spectrum Light : %d lux" % visible_spectrum_val
    logger.info("Visibile Spectrum Light : %d lux" % visible_spectrum_val)
    isItNight = isItNightTime(visible_spectrum_val)
    print

    return isItNight

def nightDayCheck(isItNight, camera):
    if (isItNight):
        setSystemToNightMode(camera)
    else:
        setSystemToDayMode(camera)

    return

def setSystemToNightMode(camera):
    turnOnIRLED()
    camera.exposure_mode = 'night'

    return

def setSystemToDayMode(camera):
    turnOffIRLED()
    camera.exposure_mode = 'auto'

    return

#Turn off LED on pin 18
def turnOffIRLED():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)
    print 'LED off'
    GPIO.output(18, GPIO.LOW)

    return

#Turn on LED on pin 18
def turnOnIRLED():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)
    print 'LED on'
    GPIO.output(18, GPIO.HIGH)

    return

def createLogger():
    logger = logging.getLogger(__name__)
    filename = 'logs/' + time.strftime("%Y%m%d-%H%M") + '_camera_app.log'
    hdlr = logging.FileHandler(filename)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)

    return logger

startRaspCamera()








