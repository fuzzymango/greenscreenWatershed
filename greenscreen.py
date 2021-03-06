import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('IS_DATA/greenscreen.jpg')
img_copy = np.copy(img)

matte_image = np.zeros(img.shape[:2], dtype=np.int32)

segments = np.zeros(img.shape, dtype=np.int8)

# Watershed doesn't work with only 2 segments?
# the 0th element is added as a buffer. The user can press 1 or 2 for FG and BG respectively
# the 0th element segment will never be used
colors = [(150,150,150), (255,255,255), (0, 0, 0)]


current_marker = 1
marks_updated = False
n_markers = 3 # 0 to 1


def mouse_callback(event, x, y, flags, param):
    global marks_updated 

    if event == cv2.EVENT_LBUTTONDOWN:
        
        # TRACKING FOR MARKERS
        cv2.circle(matte_image, (x, y), 10, (current_marker), -1)
        
        # DISPLAY ON USER IMAGE
        cv2.circle(img_copy, (x, y), 10, colors[current_marker], -1)
        marks_updated = True
        
        
cv2.namedWindow('Input Image')
cv2.setMouseCallback('Input Image', mouse_callback)

while True:
    
    # SHow the 2 windows
    cv2.imshow('WaterShed Segments', segments)
    cv2.imshow('Input Image', img_copy)
        
        
    # Close everything if Esc is pressed
    k = cv2.waitKey(1)

    if k == 27:
        break
        
    # Clear all colors and start over if 'c' is pressed
    elif k == ord('c'):
        img_copy = img.copy()
        matte_image = np.zeros(img.shape[0:2], dtype=np.int32)
        segments = np.zeros(img.shape,dtype=np.uint8)
        
    # If a number 0-9 is chosen index the color
    elif k > 0 and chr(k).isdigit():
        # chr converts to printable digit
        n = int(chr(k))
        if n == 1 or n == 2:
            current_marker = n
            
    # If we clicked somewhere, call the watershed algorithm on our chosen markers
    if marks_updated:
        matte_image_copy = matte_image.copy()
        cv2.watershed(img, matte_image_copy)
        
        segments = np.zeros(img.shape,dtype=np.uint8)
        
        for color_ind in range(n_markers):
            segments[matte_image_copy == (color_ind)] = colors[color_ind]
        
        marks_updated = False
        
cv2.destroyAllWindows()
