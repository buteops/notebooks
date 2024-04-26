#!/usr/bin/env python3

import cv2
import sys

# source = cv2.VideoCapture(0)

# win_name = 'Camera Preview'
# cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

# while cv2.waitKey(1) != 27:  # Escape
#     has_frame, frame = source.read()
#     if not has_frame:
#         break
#     cv2.imshow(win_name, frame)

# source.release()
# cv2.destroyWindow(win_name)


num_cameras = 10  # Adjust this number based on the maximum expected number of cameras
for i in range(num_cameras):
    cap = cv2.VideoCapture(i)
    if not cap.isOpened():
        print(f"No camera detected at index {i}")
    else:
        print(f"Camera detected at index {i}")