import cv2
import numpy as np

def showres(path, nr):
    #path = 'cp2.jpg'
    #nr = [119.54516542, 158.39392331, 25.24073269, 255.20738587, 1.37893195, 240.86778279]

    img = cv2.imread(path)
    img = cv2.resize(img, (650, 485), interpolation = cv2.INTER_CUBIC)

    hsv = np.zeros((650, 485,3), np.uint8)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h_plane = np.zeros((650, 485,1), np.uint8)
    v_plane = np.zeros((650, 485,1), np.uint8)
    s_plane = np.zeros((650, 485,1), np.uint8)
    h_range = np.zeros((650, 485,1), np.uint8)
    v_range = np.zeros((650, 485,1), np.uint8)
    s_range = np.zeros((650, 485,1), np.uint8)
    hsv_and = np.zeros((650, 485,1), np.uint8)

    h_plane, s_plane, v_plane = cv2.split(hsv)

    Hmin = round(nr[0])
    Hmax = round(nr[1])
    Smin = round(nr[2])
    Smax = round(nr[3])
    Vmin = round(nr[4])
    Vmax = round(nr[5])
    if Hmin < 0:
        Hmin = 0
    if Smin < 0:
        Smin = 0
    if Vmin < 0:
        Vmin = 0
    if Hmax > 255:
        Hmax = 255
    if Smax > 255:
        Smax = 255
    if Vmax > 255:
        Vmax = 255
    h_range = cv2.inRange(h_plane, Hmin, Hmax)
    s_range = cv2.inRange(s_plane, Smin, Smax)
    v_range = cv2.inRange(v_plane, Vmin, Vmax)

    hsv_and = cv2.bitwise_and(hsv, hsv, mask = h_range)
    hsv_and = cv2.bitwise_and(hsv_and, hsv_and, mask = cv2.bitwise_not(s_range))
    hsv_and = cv2.bitwise_and(hsv_and, hsv_and, mask = cv2.bitwise_not(v_range))

    gray = cv2.cvtColor(hsv_and, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 200, 300)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    _, countours, hierarchy = cv2.findContours( closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
    for c in countours:
        x,y,w,h=cv2.boundingRect(c)
        img=cv2.rectangle(img,(x,y),(x+w+5,y+h+5),(0,255,0),2)

    return img

    #while(1):
    #    cv2.imshow('sad', img)
    #    if cv2.waitKey(20) & 0xFF == 27:
    #        break    
    #cv2.destroyAllWindows()
