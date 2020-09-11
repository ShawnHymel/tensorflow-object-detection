#!/usr/bin/env python3

# PyCam
#
# Script that streams video to new window. Press 'space' to save a still frame
# photo (saved in current directory). Press 'esc' to exit.
#
# You will need the following packages:
#  * opencv-contrib-python (tested with v4.1.0.25)
#
# Example call:
# python pycam.py
#
# Author: StackOverflow user derricw
# Modified by: Shawn Hymel
# Date: September 11, 2020
# License: CC BY-SA 4.0
# Original code:
# https://stackoverflow.com/questions/34588464/python-how-to-capture-image-from-webcam-on-click-using-opencv

import os
import cv2
import argparse

# Settings
file_prefix = "opencv_frame_"       # First part of filename for saved photos

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-r',
                    '--resolution',
                    action='store',
                    dest='resolution',
                    default="1280x720",
                    help="Desired camera resolution (WxH) in pixels. If the "
                            "camera does not support the resolution, errors "
                            "may occur.")
args = parser.parse_args()
res_w, res_h = args.resolution.split('x')
im_w, im_h = int(res_w), int(res_h)

# Print resolution
print("Using resolution: " + str(im_w) + "x" + str(im_h))

# Set up camera to start streaming video
cam = cv2.VideoCapture(0)
cam.set(3, im_w)
cam.set(4, im_h)
cv2.namedWindow("PyCam ('space': take photo, 'esc': exit)", cv2.WINDOW_NORMAL)

# Remember photo number
img_counter = 0

# Do not overwrite existing photos: start numbering after last one
while os.path.isfile(file_prefix + "{}.png".format(img_counter)):
    print(file_prefix + "{}.png".format(img_counter) + " exists--incrementing")
    img_counter += 1

# Main while loop
while True:

    # Get new frame, show in window
    ret, frame = cam.read()
    if not ret:
        print("Failed to grab frame")
        break
    cv2.imshow("PyCam ('space': take photo, 'esc': exit)", frame)

    # Handle key press
    k = cv2.waitKey(1)
    if k%256 == 27:
    
        # ESC pressed
        print("Escape hit, closing...")
        break
        
    elif k%256 == 32:
    
        # SPACE pressed
        img_name = file_prefix + "{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

# Cleanup
cam.release()
cv2.destroyAllWindows()
