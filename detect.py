from threading import Thread
from picamera import PiCamera
from picamera.array import PiRGBArray
import re
import picar_4wd as fc
import time
import numpy as np
import sys
from PIL import Image
import argparse
import io
import cv2
from tflite_runtime.interpreter import Interpreter

def main():

	vs = PiVideoStream().start()
	time.sleep(2)

	while True:
		result = vs.see_sign()
		print(result)
		if result is True:
			fc.stop()
			time.sleep(5)
			print("Stopped for Stop Sign after detecting object")
			vs.reset_stop()
			
			
def load_labels(path):
	with open(path, 'r', encoding='utf-8') as f:
    		lines = f.readlines()
    		labels = {}
    		for row_number, content in enumerate(lines):
    			pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
    			if len(pair) == 2 and pair[0].strip().isdigit():
    				labels[int(pair[0])] = pair[1].strip()
    			else:
    				labels[row_number] = pair[0].strip()
	return labels




def set_input_tensor(interpreter, image):
	tensor_index = interpreter.get_input_details()[0]['index']
	input_tensor = interpreter.tensor(tensor_index)()[0]
	input_tensor[:, :] = image
	
def get_output_tensor(interpreter, index):
	output_details = interpreter.get_output_details()[index]
	tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
	return tensor


def detect_objects(interpreter, image, threshold):
	set_input_tensor(interpreter, image)
	interpreter.invoke()
	classes = get_output_tensor(interpreter, 1)
	scores = get_output_tensor(interpreter, 2)
	count = int(get_output_tensor(interpreter, 3))
	results = False
	for i in range(count):
		if scores[i] >= threshold:
			if classes[i] == 12:
				results = True
	return results


def annotate_objects(annotator, results, labels):
	for obj in results:
		ymin, xmin, ymax, xmax = obj['bounding_box']
		xmin = int(xmin * CAMERA_WIDTH)
		xmax = int(xmax * CAMERA_WIDTH)
		ymin = int(ymin * CAMERA_HEIGHT)
		ymax = int(ymax * CAMERA_HEIGHT)
		# Overlay the box, label, and score on the camera preview
		annotator.bounding_box([xmin, ymin, xmax, ymax])
		annotator.text([xmin, ymin], '%s\n%.2f' % (labels[obj['class_id']], obj['score']))

class PiVideoStream:
	def __init__(self, resolution=(640, 480), framerate=30, **kwargs):
		# initialize the camera
		self.camera = PiCamera()
		
		# set camera parameters
		self.camera.resolution = resolution
		self.camera.framerate = framerate		
		self.saw_sign = False
		self.labels = load_labels('coco_labels.txt')
		self.interpreter = Interpreter('detect.tflite')
		self.interpreter.allocate_tensors()
		_, self.input_height, self.input_width, _ = self.interpreter.get_input_details()[0]['shape']
		
		# set optional camera parameters (refer to PiCamera docs)
		for (arg, value) in kwargs.items():
			setattr(self.camera, arg, value)
		# initialize the stream
		self.rawCapture = PiRGBArray(self.camera, size=resolution)
		self.stream = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)

		# initialize the frame and the variable used to indicate
		# if the thread should be stopped
		self.frame = None
		self.stopped = False
   


	def update(self):
		# keep looping infinitely until the thread is stopped
		for f in self.stream:
		# grab the frame from the stream and clear the stream in
		# preparation for the next frame
			self.frame = f.array
			cv2.imwrite('color_img.jpg', self.frame)
			image = Image.fromarray(self.frame).convert('RGB').resize((self.input_width, self.input_height), Image.ANTIALIAS)
			self.results = detect_objects(self.interpreter, image, 0.4)
			
			if self.results is True:
				self.saw_sign = True
				print("saw a stop sign and updated to true!!")
			#stop sign
			self.rawCapture.truncate(0)
			
			# if the thread indicator variable is set, stop the thread
			# and resource camera resources
			
			if self.stopped:
				self.stream.close()
				self.rawCapture.close()
				self.camera.close()
				return

	def read(self):
	# return the frame most recently read
		return self.frame

	def see_sign(self):
		return self.saw_sign

	def reset_stop(self):
	# return the frame most recently read
		self.saw_sign = False

	def stop(self):
	# indicate that the thread should be stopped
		self.stopped = True
   
	def start(self):
		t = Thread(target = self.update)
		t.daemon = True
		t.start()
		return self

if __name__ == "__main__":
	try:
		main()
	finally:
		print("yolo")
		fc.stop()
      