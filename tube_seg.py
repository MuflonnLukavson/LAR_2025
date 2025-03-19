# Segmentation of tubes of different colours

import numpy as np
import cv2
import image_seg as im


def color_tube_segmentation(img, color, avg_bright):
    # color space conversion
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Masking image
    mask = im.masking_img(hsv,color, avg_bright)

    # cv2.imshow('mask',mask)

    # getting components and stats
    out = cv2.connectedComponentsWithStats(mask)


    rem_out = []
    for i in range(1, len(out[2])):
        c, r, x_len, y_len, area = out[2][i]
        if ( (area < 800) or (r + y_len < 100)):
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
        rect_length, rect_width = rect[1]
        if not (im.is_tube(rect_length, rect_width)):
            print("proportions check: ",rect_length, rect_width)
            im.clear_mask(mask, r, c, x_len, y_len)
        else:
            hull_list.append(hull)



    ## Drawing countours
    # cv2.drawContours(img, contours, -1, (0,255,0), 3)
    # for i in range(len(hull_list)):
    #     color = (255, 0, 0)
        # cv2.drawContours(img, hull_list, i, color)
        # cv2.drawContours(mask, hull_list, i, color)



    ## Creating windows with images
    # cv2.imshow('img',img)
    # cv2.imshow('mask2',mask)

    # k = cv2.waitKey(5000) & 0xFF
    
    # cv2.destroyAllWindows()
    return mask


def segment_all_tubes(img, bright):
    colors = ["blue", "red", "green"]
    mask = []
    for color in colors:
        new_mask = color_tube_segmentation(img, color, bright)
        if len(mask) == 0:
            mask = new_mask
        else:
            mask = mask + new_mask

    cv2.imshow("img",img)
    cv2.imshow('mask', mask)
    k = cv2.waitKey(5000) & 0xFF
    
    cv2.destroyAllWindows()

##  ISSUES
# aligning tubes - 33! ,34, 35, 48, 50, 52 - not a big problem
# fallen tubes - 42!, 43!, 44! - not a big problem
# brightness - 43, 44, 45!, 46!, 48!, 49, 50, 51, 52 - not a big problem

# false positives - 55 - could be problem
# too far - 58 - not a problem
# too close - 25 - is problem

## TODO
"""
- low brigthnes for red
- issues with segmentetation
- linking to pointcloud
"""

if __name__ == '__main__':
    img = cv2.imread("ball_images\\58.png")
    avg_bright = im.get_overall_bright(img)
    print(avg_bright)
    segment_all_tubes(img, avg_bright)
