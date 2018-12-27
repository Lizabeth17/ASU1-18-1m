import cv2
import numpy as np

paths = []
#paths.append('1.jpg')
#paths.append('2.jpg')
#paths.append('3.jpg')
#paths.append('4.jpg')
#paths.append('5.jpg')
#paths.append('6.jpg')
#paths.append('7.jpg')
#paths.append('8.jpg')
#paths.append('9.jpg')
#paths.append('10.jpg')
#paths.append('11.jpg')
#paths.append('12.jpg')
#paths.append('13.jpg')
#paths.append('14.jpg')
#paths.append('15.jpg')
#paths.append('cp1.jpg')
#paths.append('cp2.jpg')


for path in paths:
    img = cv2.imread(path)

    height, width = img.shape[:2]
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

    h_plane, s_plane, v_plane = cv2.split(hsv) #делим на каналы
    h_min_val, h_max_val, h_min_loc, h_max_loc = cv2.minMaxLoc(h_plane) #макс и мин у h канала
    s_min_val, s_max_val, s_min_loc, s_max_loc = cv2.minMaxLoc(s_plane) #макс и мин у s канала
    v_min_val, v_max_val, v_min_loc, v_max_loc = cv2.minMaxLoc(v_plane) #макс и мин у v канала

    print(str(h_min_val) + ', ' + str(h_max_val))
    print(str(s_min_val) + ', ' + str(s_max_val))
    print(str(v_min_val) + ', ' + str(v_max_val))
               
    Hmin = 0
    Hmax = 256
    Smin = 0
    Smax = 256
    Vmin = 0
    Vmax = 256
    h_range = cv2.inRange(h_plane, Hmin, Hmax)
    s_range = cv2.inRange(s_plane, Smin, Smax)
    v_range = cv2.inRange(v_plane, Vmin, Vmax)
    def myTrackbarHmin(pos):
        global Hmin
        global h_range
        Hmin = pos
        h_range = cv2.inRange(h_plane, Hmin, Hmax)

    def myTrackbarHmax(pos):
        global Hmax
        global h_range
        Hmax = pos
        h_range = cv2.inRange(h_plane, Hmin, Hmax)

    def myTrackbarSmin(pos):
        global Smin
        global s_range
        Smin = pos
        s_range = cv2.inRange(s_plane, Smin, Smax)

    def myTrackbarSmax(pos):
        global Smax
        global s_range
        Smax = pos
        s_range = cv2.inRange(s_plane, Smin, Smax)

    def myTrackbarVmin(pos):
        global Vmin
        global v_range
        Vmin = pos
        v_range = cv2.inRange(v_plane, Vmin, Vmax)

    def myTrackbarVmax(pos):
        global Vmax
        global v_range
        Vmax = pos
        v_range = cv2.inRange(v_plane, Vmin, Vmax)

    cv2.namedWindow('h_range',flags=cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('s_range',flags=cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('v_range',flags=cv2.WINDOW_AUTOSIZE)

    cv2.createTrackbar('Hmin', 'h_range', int(h_min_val), int(256), myTrackbarHmin)
    cv2.createTrackbar('Hmax', 'h_range', int(h_max_val), int(256), myTrackbarHmax)
    cv2.createTrackbar('Smin', 's_range', int(s_min_val), int(256), myTrackbarSmin)
    cv2.createTrackbar('Smax', 's_range', int(s_max_val), int(256), myTrackbarSmax)
    cv2.createTrackbar('Vmin', 'v_range', int(v_min_val), int(256), myTrackbarVmin)
    cv2.createTrackbar('Vmax', 'v_range', int(v_max_val), int(256), myTrackbarVmax)

    while(1):
        cv2.imshow('original', img)
        cv2.imshow('hsv', hsv)
        #cv2.imshow('h_plane', h_plane)
        #cv2.imshow('s_plane', s_plane)
        #cv2.imshow('v_plane', v_plane)

        cv2.imshow('h_range', h_range)
        cv2.imshow('s_range', cv2.bitwise_not(s_range))
        cv2.imshow('v_range', cv2.bitwise_not(v_range))

        hsv_and = cv2.bitwise_and(hsv, hsv, mask = h_range)
        hsv_and = cv2.bitwise_and(hsv_and, hsv_and, mask = cv2.bitwise_not(s_range))
        hsv_and = cv2.bitwise_and(hsv_and, hsv_and, mask = cv2.bitwise_not(v_range))
        cv2.imshow('AND', hsv_and)
        
        if cv2.waitKey(20) & 0xFF == 27:
            break    
    cv2.destroyAllWindows()

    #выделение контуром на оригинале
    gray = cv2.cvtColor(hsv_and, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 200, 300)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    _, countours, hierarchy = cv2.findContours( closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
    for c in countours:
        x,y,w,h=cv2.boundingRect(c)
        img=cv2.rectangle(img,(x,y),(x+w+5,y+h+5),(0,255,0),2)
    while(1):
        cv2.imshow('and_tresh', closed)
        cv2.imshow('original with contour', img)

        if cv2.waitKey(20) & 0xFF == 27:
            break    
    cv2.destroyAllWindows()

    #записываем в файл
    with open('datas.txt', 'a') as fl:
        print(path, file=fl)
        print('h:' + str(Hmin) + '-' + str(Hmax), file=fl)
        print('s:' + str(Smin) + '-' + str(Smax), file=fl)
        print('v:' + str(Vmin) + '-' + str(Vmax), file=fl)
        print('*', file=fl)
