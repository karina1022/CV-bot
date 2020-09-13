from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import time
import numpy as np
#import picamera
import cv2

from PIL import Image
from tflite_runtime.interpreter import Interpreter

def load_labels(path):
  with open(path, 'r') as f:
    return {i: line.strip() for i, line in enumerate(f.readlines())}


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
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model', help='File path of .tflite file.', required=True)
  parser.add_argument(
      '--labels', help='File path of labels file.', required=True)
  args = parser.parse_args()

  labels = load_labels(args.labels)

  interpreter = Interpreter(args.model)
  interpreter.allocate_tensors()
  _, height, width, _ = interpreter.get_input_details()[0]['shape']

  #with picamera.PiCamera(resolution=(640, 480), framerate=30) as camera:
    #camera.start_preview()

  cap = cv2.VideoCapture(0)
  #擷取畫面 寬度 設定為512
  cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
  #擷取畫面 高度 設定為512
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

  key_detect = 0
  times=1
  while (key_detect==0):
    ret,image_src =cap.read()

    image=cv2.resize(image_src,(224,224))

    start_time = time.time()
    results = classify_image(interpreter, image)
    elapsed_ms = (time.time() - start_time) * 1000
    label_id, prob = results[0]

    print(labels[label_id])

    cv2.imshow('Detecting....',image_src)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      key_detect = 1

  cap.release()
  cv2.destroyAllWindows()

if __name__ == '__main__':
  main()
