import picamera
import time
import os
import errno

with picamera.PiCamera() as camera:
	camera.start_preview()
	filelocation = "/home/pi/recorded_videos/"
	foldername = time.strftime("%Y%m%d") + "_videos/"
	
	directory_path = filelocation + foldername
	if not os.path.exists(directory_path):
		try:
			os.makedirs(directory_path)
		except OSError as error:
			if error.errno != errno.EEXIST:
				raise

	timestring = time.strftime("%Y%m%d-%H%M%S")
	filename = directory_path + "vid_" + timestring + ".h264"
	camera.start_recording(filename, format='h264', quality=35)
	minute_counter = 0
	while minute_counter < 360:
		camera.annotate_text = time.strftime("%H%M%S")
		camera.wait_recording(1)
		minute_counter += 1
	hour_counter = 1
	while hour_counter < 24:
		timestring = time.strftime("%Y%m%d-%H%M%S")
		filename = directory_path + "vid_" + timestring + ".h264"
		camera.split_recording(filename)
		minute_counter = 0
		while minute_counter < 360:
			camera.annotate_text = time.strftime("%H%M%S")
			camera.wait_recording(1)
			minute_counter += 1
	camera.stop_recording()
