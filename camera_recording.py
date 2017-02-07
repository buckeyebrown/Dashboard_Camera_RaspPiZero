import picamera
import time

with picamera.PiCamera() as camera:
	camera.resolution = (640, 480)
	camera.start_preview()
	filelocation = "/home/pi/recorded_videos/"
	timestring = time.strftime("%Y%m%d-%H%M%S")
	filename = filelocation + "vid_" + timestring + ".h264"
	camera.start_recording(filename, format='h264', quality=40)
	camera.wait_recording(5)
	for i in range(2, 25):
		timestring = time.strftime("%Y%m%d-%H%M%S")
		filename = filelocation + "vid_" + timestring + ".h264"
		camera.split_recording(filename)
		camera.wait_recording(5)
	camera.stop_recording()
