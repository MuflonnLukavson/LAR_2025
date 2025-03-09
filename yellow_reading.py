# from robolab_turtlebot import Turtlebot, Rate, get_time

# from robolab_turtlebot import Turtlebot
import numpy as np
import cv2

# turtle = Turtlebot()

def clear_mask(mask, r, c, x_len, y_len):
    for i in range(y_len):
        for j in range(x_len):
            mask[r + i][c + j] = 0

def check_prop(x_len, y_len):
    return max(x_len,y_len)/min(x_len,y_len) > 2

def check_rect_circ(rect_wid, rect_len, circ_r):
    print (rect_len*rect_wid , np.pi * (circ_r**2))
    return 1.1 * rect_len*rect_wid > np.pi * (circ_r**2)


# img = turtle.get_rgb_image()
img = cv2.imread("ball_images\\58.png")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Creating sets for yellow color
lower_yellow = np.array([19, 80, 80])
upper_yellow = np.array([30, 255, 255])

# Masking yellow - where it is in bounds -> sets 1 
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)


cv2.imshow('mask',mask)
# Doing bitwise AND between img and mask -> getting yellow parts of the img
# yellow_regions = cv2.bitwise_and(img,img, mask= mask)
out = cv2.connectedComponentsWithStats(mask)
# print(out[0], "\n --next-- \n",out[2], "\n --next-- \n", out[3])
# Getting countours 

rem_out = []
for i in range(1, len(out[2])):
    c, r, x_len, y_len, area = out[2][i]
    if ( (area < 100) or (r + y_len < 100)):
        pass
        # print(out[2][i], "tutu")
        clear_mask(mask, r, c, x_len, y_len)
    elif ( check_prop(x_len, y_len)):
        print(out[2][i], c, r, "|", mask[r][c], out[1][r][c])
        clear_mask(mask, r, c, x_len, y_len)
    # elif ( check_rect_circle)
    else:
        # print(out[2][i], r, c, "|", mask[r][c], out[1][r][c])
        rem_out.append(out[2][i])
        pass
rem_out = rem_out[::-1]
print(rem_out, len(rem_out))

out = cv2.connectedComponentsWithStats(mask)

contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
# print(out[1][40], mask[40], out[2])
# Find the convex hull object for each contour
hull_list = []
for i in range(len(contours)):
    c, r, x_len, y_len, area = out[2][-i-1]
    print(out[2][i+1])
    hull = cv2.convexHull(contours[i])
    rect = cv2.minAreaRect(contours[i])
    rect_width, rect_length = rect[1]
    circ = cv2.minEnclosingCircle(contours[i])
    circ_r = circ[1]
    print(rect, circ)
    if check_rect_circ(rect_width, rect_length, circ_r):
        print("got it")
        hull_list.append(hull)
    else:
        clear_mask(mask, r, c, x_len, y_len)
        pass

# convex = cv2.convexityDefects(contours, hull_list)
# contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Filtering 
# Drawing countours
cv2.drawContours(img, contours, -1, (0,255,0), 3)
for i in range(len(hull_list)):
    color = (255, 0, 0)
    cv2.drawContours(img, hull_list, i, color)
    cv2.drawContours(mask, hull_list, i, color)
    # cv2.drawContours(mask, rect_list, i, color)

cv2.imshow('img',img)
cv2.imshow('mask2',mask)
# cv2.imshow('res',yellow_regions)
k = cv2.waitKey(5000) & 0xFF
 
cv2.destroyAllWindows()


# t = get_time()

# while get_time() - t < 10:
#     turtle.cmd_velocity(linear=0.1)
#     rate.sleep()