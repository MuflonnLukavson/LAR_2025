# from robolab_turtlebot import Turtlebot, Rate, get_time

# from robolab_turtlebot import Turtlebot
import numpy as np
import cv2
import image_seg as im
# turtle = Turtlebot()



# img = turtle.get_rgb_image()
def green_tube_segmentation(img):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    avg_bright = im.get_overall_bright(img)
    # Creating sets for green color

    print(avg_bright)
    if avg_bright < 120:
        lower_green = np.array([40, 50, 50])
        upper_green = np.array([70, 255, 255])
    else:
        lower_green = np.array([35, 80, 80])
        upper_green = np.array([85, 255, 255])

    # Masking green - where it is in bounds -> sets 1 
    mask = cv2.inRange(hsv, lower_green, upper_green)


    cv2.imshow('mask',mask)
    # Doing bitwise AND between img and mask -> getting green parts of the img
    # green_regions = cv2.bitwise_and(img,img, mask= mask)
    out = cv2.connectedComponentsWithStats(mask)
    # print(out[0], "\n --next-- \n",out[2], "\n --next-- \n", out[3])
    # Getting countours 

    rem_out = []
    for i in range(1, len(out[2])):
        c, r, x_len, y_len, area = out[2][i]
        if ( (area < 200) or (r + y_len < 100)):
            pass
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
        if (im.check_prop_tube(rect_length, rect_width)):
            print("proportions check: ",rect_length, rect_width)
            im.clear_mask(mask, r, c, x_len, y_len)
        else:
            hull_list.append(hull)



    # Filtering 
    # Drawing countours
    cv2.drawContours(img, contours, -1, (0,255,0), 3)
    for i in range(len(hull_list)):
        color = (255, 0, 0)
        cv2.drawContours(img, hull_list, i, color)
        cv2.drawContours(mask, hull_list, i, color)

    # print("brightness: ",avg_bright)
    # new_img_in = gamma_correction(img, 0.5)

    # avg_bright_new = get_overall_bright(new_img_in)
    # print("New brightness: ",avg_bright_new)


    cv2.imshow('img',img)
    cv2.imshow('mask2',mask)
    # cv2.imshow('new_im',new_img_in)
    # cv2.imshow('res',green_regions)
    k = cv2.waitKey(5000) & 0xFF
    
    cv2.destroyAllWindows()


##  ISSUES
# aligning tubes - 33! ,34, 35, 48, 50, 52
# fallen tubes 41 42, 43
# brightness - 43, 44, 45!, 46!, 47!, 48, 49, 50, 51, 52
#54
# false positives - 55
# too far - 58
if __name__ == '__main__':
    img = cv2.imread("ball_images\\48.png")

    green_tube_segmentation(img)
