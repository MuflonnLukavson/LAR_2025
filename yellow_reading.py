from robolab_turtlebot import Turtlebot, Rate, get_time

from robolab_turtlebot import Turtlebot
import numpy as np
import cv2

turtle = Turtlebot()

img = turtle.get_rgb_image()

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Creating sets for yellow color
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])

# Masking yellow - where it is in bounds -> sets 1 
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

# Doing bitwise AND between img and mask -> getting yellow parts of the img
yellow_regions = cv2.bitwise_and(img,img, mask= mask)
out = cv2.connectedComponentsWithStats(mask)

# Getting countours 
contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
# contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Drawing countours
cv2.drawContours(img, contours, -1, (0,255,0), 3)


cv2.imshow('img',img)
cv2.imshow('mask',mask)
cv2.imshow('res',yellow_regions)
k = cv2.waitKey(5) & 0xFF
 
cv2.destroyAllWindows()


# t = get_time()

# while get_time() - t < 10:
#     turtle.cmd_velocity(linear=0.1)
#     rate.sleep()