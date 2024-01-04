import cv2
import numpy as np


# Functin to get contours (shapes) in a frame
# -----------x----------------x--------------------x-----------------
def getContours(frame_dill,frame_copy):
    # function find coonotours (shapes) in an image,
    # cv2.RETR_EXTERNAL gets the extreme contours in an image (used in finding outer corners)
    # cv2.CHAIN_APPROX_NONE gets all the contours found (uncompressed)
    contours, hierarchy = cv2.findContours(frame_dill, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
  
    for cnt in contours:
        # Function finds the area os the contour (shape)
        area = cv2.contourArea(cnt)
        #print(area)

        if area>500:
            # Function draws the controus on the image
            # -1 means to draw all the contours
            #cv2.drawContours(frame_copy, cnt, -1, [255, 0, 255], 7)

            # Function finds the arc length of the contours (helps to finds cornors)
            # True indicates that the shape is closed
            arc_len = cv2.arcLength(cnt, True)
            #print(arc_len)

            # Function finds the cornor points in a contour
            # 0.02*arc_len is the resolution
            # True indicates that the shape is closed
            approx = cv2.approxPolyDP(cnt, 0.02*arc_len, True)
            #print(len(approx))
            obj_cornor = len(approx)

            GetBoundingBox(approx, obj_cornor, area)
# -----------x----------------x--------------------x-----------------
            


# Function to get boundingbox on the detected sahpes
# -----------x----------------x--------------------x-----------------
def GetBoundingBox(approx, obj_cornor, area): 
    x, y, w, h = cv2.boundingRect(approx)
    cv2.rectangle(frame_copy, (x, y), (x+w, y+h), [255,0,0], 3)

    if obj_cornor==3:
        Objtype = "Triangle"
    elif obj_cornor==4:
        # 15000 is the calibrated value
        if area>=15000:
            Objtype="rectangle"
        else:
            Objtype="Square"
    elif obj_cornor==5:
        Objtype="pentagone"
    elif obj_cornor==6:
        Objtype="hexagone"
    else:
        Objtype="circle"

    cv2.putText(frame_copy,  
                Objtype,  
                (x+w+20, y+20),  
                cv2.FONT_HERSHEY_COMPLEX, 0.7,
                (255, 0, 0),  
                2) 
# -----------x----------------x--------------------x-----------------



cap = cv2.VideoCapture(1)

while True:
    succcess, frame = cap.read()
    frame_copy = frame.copy()

    frame_blur = cv2.GaussianBlur(frame, (7,7), 1)
    frame_gray = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2GRAY)

    # Function takes input image and outputs an image containing only edges
    # 200, 200 are the calibrated Threshold values (get using trackbars)
    fram_canny = cv2.Canny(frame_gray, 200, 200)

    # To reduce the noice in canny frame
    kernal = np.ones([5,5])
    frame_dill = cv2.dilate(fram_canny, kernal, iterations=1)

    getContours(frame_dill,frame_copy)

    cv2.imshow("output", frame_copy)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

cap.release()
cv2.destroyAllWindows()
