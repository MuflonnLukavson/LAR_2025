# from robolab_turtlebot import Turtlebot, Rate, get_time

# from robolab_turtlebot import Turtlebot
import numpy as np
import cv2
import image_seg as im
# turtle = Turtlebot()



# img = turtle.get_rgb_image()
def ball_segmentation(img):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    avg_bright = im.get_overall_bright(img)
    # Creating sets for yellow color

    if avg_bright < 120:
        lower_yellow = np.array([18, 50, 50])
        upper_yellow = np.array([30, 255, 255])
    else:
        lower_yellow = np.array([20, 80, 80])
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
        if ( (area < 500) or (r + y_len < 100)):
            pass
            im.clear_mask(mask, r, c, x_len, y_len)
        elif ( im.check_prop_circle(x_len, y_len)):
            print("proportions check: ",out[2][i], c, r, "|", mask[r][c], out[1][r][c])
            im.clear_mask(mask, r, c, x_len, y_len)
        else:
            rem_out.append(out[2][i])
            pass
    rem_out = rem_out[::-1]

    out = cv2.connectedComponentsWithStats(mask)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Find the convex hull object for each contour
    hull_list = []
    for i in range(len(contours)):
        c, r, x_len, y_len, area = out[2][-i-1]
        hull = cv2.convexHull(contours[i])
        rect = cv2.minAreaRect(contours[i])
        rect_width, rect_length = rect[1]
        circ = cv2.minEnclosingCircle(contours[i])
        circ_r = circ[1]
        if im.check_rect_circ(rect_width, rect_length, circ_r):
            hull_list.append(hull)
        else:
            im.clear_mask(mask, r, c, x_len, y_len)
            pass


    # Filtering 
    # Drawing countours
    cv2.drawContours(img, contours, -1, (0,255,0), 3)
    for i in range(len(hull_list)):
        color = (255, 0, 0)
        cv2.drawContours(img, hull_list, i, color)
        cv2.drawContours(mask, hull_list, i, color)

    cv2.imshow('img',img)
    cv2.imshow('mask2',mask)
    k = cv2.waitKey(5000) & 0xFF
    
    cv2.destroyAllWindows()


##  ISSUES
# Ball is too close to the robot - half of it is seen, cannot find it - 17, 18, 56
# Ball is behind a tube, its is halved on photo, so it is refused due to height and width ratio - 24, 32, 35, 43, 
# Sometimes there is distortion around the ball, it breaks its parameters of counters and it is refused due to being too much rectangle - 29, 55, 19
# If there is not enough light in the room, threshhold is fucked. --  lower_yellow = np.array([18, 50, 50]) this works for lower light level -58, 45, 46, 49, 

if __name__ == '__main__':
    img = cv2.imread("ball_images\\40.png")
    avg_bright = im.get_overall_bright(img)
    ball_segmentation(img)