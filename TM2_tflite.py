from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
sys.path.append("/usr/lib/python3/dist-packages")

import io
import time
import numpy as np
#import picamera

from PIL import Image
from tflite_runtime.interpreter import Interpreter
from line import line_bot
from config import *
from args import load_args
from OpenCV import *

def set_input_tensor(interpreter, image):
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image


def classify_image(interpreter, image, top_k=1):
  """Returns a sorted array of classification results."""
  set_input_tensor(interpreter, image)
  interpreter.invoke()
  output_details = interpreter.get_output_details()[0]
  output = np.squeeze(interpreter.get_tensor(output_details['index']))

  # If the model is quantized (uint8 data), then dequantize the results
  if output_details['dtype'] == np.uint8:
    scale, zero_point = output_details['quantization']
    output = scale * (output - zero_point)

  ordered = np.argpartition(-output, top_k)
  return [(i, output[i]) for i in ordered[:top_k]]

    
def main():
  args, labels = load_args()
  interpreter = Interpreter(args.model)
  interpreter.allocate_tensors()
  _, height, width, _ = interpreter.get_input_details()[0]['shape']

  #with picamera.PiCamera(resolution=(640, 480), framerate=30) as camera:
    #camera.start_preview()
  
  cap = set_cap()
  
  times=1
  old_labels = ""
  frame_count = 0
  diff_frame_count = 0

  while True:
    
    image = read_cap(cap)

    start_time = time.time()
    results = classify_image(interpreter, image)
    elapsed_ms = (time.time() - start_time) * 1000
    label_id, prob = results[0]
    

    if frame_count == 0:
        old_labels = labels[label_id]
    
    if old_labels != labels[label_id]:
        diff_frame_count = diff_frame_count+1

    else:
        diff_frame_count = 0
    
    if diff_frame_count>=THRESHOLD:
        line_bot("this is "+ labels[label_id])
        old_labels = labels[label_id]
        diff_frame_count = 0
        
    frame_count = frame_count + 1

    print("diff_frame_count:"+str(diff_frame_count) +" tensor id:" + labels[label_id] + " and old id: " + str(old_labels))

  close_cap()
if __name__ == '__main__':
  main()
