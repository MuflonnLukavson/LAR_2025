## File with funcitons used for image segmentation
import cv2
import numpy as np

# color table [lower,higher] boundary for bright and dark conditions
color_table_bright = {
    "green" : [
        np.array([35, 80, 80]),
        np.array([85, 255, 255])
        ],
    "blue" : [
        np.array([78, 130, 80]),
        np.array([138, 255, 255])],
    "red" : [
        np.array([0, 100, 100]), 
        np.array([8, 255, 255]), 
        np.array([172,100,100]), 
        np.array([179,255,255])
        ],
}

color_table_dark = {
    "green" : [
        np.array([35, 50, 50]), 
        np.array([85, 255, 255])
        ],
    "blue" : [
        np.array([78, 130, 50]), 
        np.array([138, 255, 255])
        ],
    "red" : [
        np.array([0, 80, 65]), 
        np.array([8, 255, 255]), 
        np.array([172,80,65]), 
        np.array([179,255,255])
        ],
}


def get_overall_bright(hsv):
    """
    function returns overall brigthnes of image
    from HSV color space
    """
    # add up all the pixel values in V channel
    value = np.sum(hsv[:,:, 2])
    # multiply height and width
    pxl = hsv.shape[0] * hsv.shape[1]
    average_value = round(value/pxl,3)
    return average_value

def gamma_correction(img, gamma):
    """
    changes relative gamma of the image (0 - 2)
    """
    lookUpTable = np.empty((1,256), np.uint8)
    for i in range(256):
        lookUpTable[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
 
    res = cv2.LUT(img, lookUpTable)
    return res


def clear_mask(mask, r, c, x_len, y_len):
    """
    clearing mask
    should only be called if the item should not be segmented
    """
    for i in range(y_len):
        for j in range(x_len):
            mask[r + i][c + j] = 0

def is_tube(x_len, y_len):
    """
    bool value
    returns true if it is tube, else it returns false
    based on width and length parameters
    """
    return (max(x_len,y_len)/min(x_len,y_len, 1000) > 3 
            and max(x_len,y_len)/min(x_len,y_len, 1000) < 8)



def check_prop_circle(x_len, y_len):
    """
    checks if the item is circle shaped based on width and length
    return true if it is NOT
    """
    return max(x_len,y_len)/min(x_len,y_len) > 2

def check_rect_circ(rect_wid, rect_len, circ_r):
    """
    checks if the area of minimal enclosing circle
    is smaller than area of minimal enclosing rectangle
    returns true if it is
    """
    return 1.15 * rect_len*rect_wid > np.pi * (circ_r**2)

def masking_img(img, color, bright):
    """
    Function for masking the image based on color
    It makes color boundaries and returns mask of required color
    """
    if color != "red":
        if bright < 120:
            lower_bound, upper_bound = color_table_dark[color]
        else:
            lower_bound, upper_bound = color_table_bright[color]

        # Masking colour - where it is in bounds -> sets 1 
        full_mask = cv2.inRange(img, lower_bound, upper_bound)
        
    else:
        # lower boundary RED color range values; Hue (0 - 10)
        # upper boundary RED color range values; Hue (160 - 180)
        if bright < 120:
            lower1, upper1, lower2, upper2 = color_table_dark["red"]
        else:
            lower1, upper1, lower2, upper2 = color_table_bright["red"]
        lower_mask = cv2.inRange(img, lower1, upper1)
        upper_mask = cv2.inRange(img, lower2, upper2)
    
        full_mask = lower_mask + upper_mask

    return full_mask