# Saving image as png file

from __future__ import print_function

import sys
import cv2
from robolab_turtlebot import Turtlebot

from imageio import imwrite

turtle = Turtlebot(rgb=True)
turtle.wait_for_rgb_image()
rgb = turtle.get_rgb_image()
img = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = 'capture_rgb.png'

print('Image saved as {}'.format(filename))
imwrite(filename, img)
