# Segmentation of tubes of different colours

import numpy as np
import cv2
import image_seg as im
import objects as obj
import yellow_reading as bRead

def color_tube_segmentation(hsv, color, avg_bright, point_c):
    """
    Fucntion which segments tube according to selected color
    Firstly it is filtrated by color into mask, then small sized
    components are filtered out. Lastly the propotions are checked.

    Returns array of objects with defined atributes (see objects.py)
    """
    # Masking image 
    mask = im.masking_img(hsv,color, avg_bright)

    # Get stats of segmented components after color masking
    out = cv2.connectedComponentsWithStats(mask)

    # Removing components smaller than defined area or ones that are too high
    for i in range(1, len(out[2])):
        c, r, x_len, y_len, area = out[2][i]
        if ( (area < 800) or (r + y_len < 100)):
            pass
            im.clear_mask(mask, r, c, x_len, y_len)
        else:
            # rem_out.append(out[2][i])
            pass
    # rem_out = rem_out[::-1]

    # Getting stats of componets that are remaining
    out = cv2.connectedComponentsWithStats(mask)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    hull_list = []
    object_list = []
    # Find the convex hull object for each contour
    for i in range(len(contours)):
        c, r, x_len, y_len, area = out[2][-i-1]
        hull = cv2.convexHull(contours[i])
        rect = cv2.boundingRect(contours[i])
        rect_length, rect_width = rect[2], rect[3]
        print(rect)
        if not (im.is_tube(rect_length, rect_width)):
            im.clear_mask(mask, r, c, x_len, y_len)
        else:
            x,y  = out[3][-i-1]
            object_list.append(obj.Object(color, x, y, point_c))
            hull_list.append(hull)


    ## Creating windows with images
    # cv2.imshow('img',img)
    # cv2.imshow('mask2',mask)

    # k = cv2.waitKey(5000) & 0xFF
    
    # cv2.destroyAllWindows()
    return mask, object_list


def segment_all(img, point_c = []):
    """
    Funtion segments all possible colors and ball separatly. 
    On each color is called function for tube segmentation accroding to color.
    Afterwards the ball is segmented
    
    Returns array of objects with defined atributes (see objects.py)
    """
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    bright = im.get_overall_bright(hsv)
    colors = ["blue", "red", "green"]
    mask = []
    objects = []
    # goint threw colors
    for color in colors:
        new_mask, new_obj = color_tube_segmentation(hsv, color, bright, point_c)
        if len(mask) == 0:
            mask = new_mask
            objects = new_obj
        else:
            mask = mask + new_mask
            objects.extend(new_obj)
    mask_ball, ball = bRead.ball_segmentation(hsv, bright, point_c)
    
    if ball is not None:
        mask = mask + mask_ball
        objects.append(ball)



    ## Showing mask of the segmented image (does not work for windows <3)
    # cv2.imshow("img",img)
    # cv2.imshow('mask', mask)
    # k = cv2.waitKey(5000) & 0xFF
    
    # cv2.destroyAllWindows()
    return objects, mask

##  ISSUES
# aligning tubes - 33! ,34, 35, 48, 50, 52 - not a big problem
# fallen tubes - 42!, 43!, 44! - not a big problem
# brightness - 43, 44, 45!, 46!, 48!, 49, 50, 51, 52 - not a big problem

# false positives - 55 - could be problem
# too far - 58 - not a problem
# too close - 25 - is problem

## TODO
"""
- low brigthness for red
- issues with segmentetation
- linking to pointcloud
"""

if __name__ == '__main__':
    img = cv2.imread("ball_images\\40.png")
    
    segment_all(img, point_c= None)
