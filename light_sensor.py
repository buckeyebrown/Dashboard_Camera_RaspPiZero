# Python code to read the light sensor values, translate to night or day

import smbus
import time
import sys

# Get I2C bus
bus = smbus.SMBus(1)

#Get user input for how many iterations
var = raw_input("How many iterations: ")
count = 0
while (count < var):
    #TSL2561 Address = 0x39 (41 in decimal)
    #Select control register, 0x00, with command register, 0x80
    #   0x03 is Power ON Mode
    bus.write_byte_data(0x29, 0x00 | 0x80, 0x03)

    #Select timing register, 0x01, with command register, 0x80
    #   0x02    Nominal Integration Time = 402ms
    bus.write_byte_data(0x29, 0x01 | 0x80, 0x02)

    # Sleep for a second
    time.sleep(1)

    #Read data back from 0x0C with command register, 0x80, 2 bytes
    # ch0 LSB, ch0 MSB
    full_spectrum_data = bus.read_i2c_block_data(0x29, 0x0C | 0x80, 2)

    # Full spectrum = IR + Visible

    #Read data back from 0x0E with command register, 0x80, 2 bytes
    # ch1 LSB, ch1 MSB
    infrared_data = bus.read_i2c_block_data(0x29, 0x0E | 0x80, 2)

    #Convert the data
    full_spectrum_val = full_spectrum_data[1] * 256 + full_spectrum_data[0]
    infrared_val = infrared_data[1] * 256 + infrared_data[0]
    visible_spectrum_val = full_spectrum_val - infrared_val

    #Print data to screen
    print "Iteration: %d." %(count + 1)
    print "Full Spectrum Light (IR + Visibile) : %d lux" %full_spectrum_val
    print "Infrared Value : %d lux" %infrared_val
    print "Visibile Spectrum Light : %d lux" %visible_spectrum_val
    isItNight = isItNightTime(visible_spectrum_val)
    print

    #Sleep for 9 seconds before next iteration
    sleep(9)
    count = count + 1


def isItNightTime(visible_spectrum_val):
    nightTime = False
    minDayTimeLux = 250
    if (visible_spectrum_val < minDayTimeLux):
        nightTime = True
        print "It is Night Time! Activating Camera Night Mode."
    else:
        print "It is Day Time! Activating Camera Day Mode."

    return nightTime