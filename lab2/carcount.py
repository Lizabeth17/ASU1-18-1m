import cv2 as cv2
import numpy as np
import car 
import datetime

now = datetime.datetime.now()

reqs = []
reqs.append('cars12.mp4')
reqs.append('cars.mp4')
reqs.append('123car.mp4')

carcounts_manual = []
carcounts_manual.append(73) #до момента когда фура на левой полосе
carcounts_manual.append(51)
carcounts_manual.append(144)
cmi = 0

filenameres = 'result_' + now.strftime("%d-%m-%Y_%H-%M") + '.txt'
with open(filenameres, 'w') as flrs:
    for req in reqs:
        total = 0

        cap = cv2.VideoCapture(req) 

        print(" ", file=flrs)
        print("Video_" + str(cmi), file=flrs)
        print(req, file=flrs)
        
        w=cap.get(3)
        h=cap.get(4)
        frameArea=h*w 
        line_c=int(2*(h/5)) 
        up_limit=int(2*(h/5)) 
        down_limit=int(3*(h/5)) 
        pt3 =  [0, line_c] 
        pt4 =  [w, line_c] 
        pts = np.array([pt3,pt4], np.int32) 
        pt5 =  [0, up_limit] 
        pt6 =  [w, up_limit] 
        pts_L3 = np.array([pt5,pt6], np.int32) 
        pts_L3 = pts_L3.reshape((-1,1,2)) #не совсем понятно, можно попробовать закоментить
        pt7 =  [0, down_limit]
        pt8 =  [w, down_limit]
        pts_L4 = np.array([pt7,pt8], np.int32)
        pts_L4 = pts_L4.reshape((-1,1,2)) 
        backSub = cv2.createBackgroundSubtractorMOG2() 

        kernalOp = np.ones((3,3),np.uint8)
        kernalOp2 = np.ones((5,5),np.uint8)
        kernalCl = np.ones((11,11),np.uint8)

        font = cv2.FONT_HERSHEY_SIMPLEX 
        cars = [] 
        max_p_age = 3 
        pid = 1 
        pids = []
        
        while True: 
            ret, frame = cap.read()
            for i in cars:
                i.age_one() 

            if frame is None:
                break

            fgMask = backSub.apply(frame) 

            ret,imBin=cv2.threshold(fgMask,200,255,cv2.THRESH_TOZERO)

            mask=cv2.morphologyEx(imBin,cv2.MORPH_OPEN,kernalOp)

            mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernalCl)

            _, countours, hierarchy=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
            for c in countours: 
                area=cv2.contourArea(c)
                if area > 500: 
                    m=cv2.moments(c)
                    cx=int(m['m10']/m['m00'])
                    cy=int(m['m01']/m['m00'])
                    x,y,w,h=cv2.boundingRect(c)
                    
                    new=True
                    
                    if cy in range(up_limit-3,down_limit+3):
                        for i in cars: 
                            if abs(x - i.getX()) <= w and abs(y - i.getY()) <= h:
                                new = False
                                i.updateCoords(cx, cy) 
                                cv2.putText(frame, "ID: {} Num: {}".format(i.i, total), (i.getX(), i.getY()), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
                                
                                if (i.y in range(up_limit,down_limit)):
                                    
                                    if not(i.i in pids):
                                        total = total + 1 
                                        pids.append(i.i) 
                                        print(pids) 
                                
                                else:
                                    if (i.i in pids):
                                        print(pids) 
                                        print("Deleting: {}".format(i.i)) 
                                        pids.remove(i.i)
                                break 
                            if i.timedOut():
                                index=cars.index(i)
                                cars.pop(index)
                                if (i.i in pids):
                                    print(pids)
                                    print("Deleting: {}".format(i.i))
                                    pids.remove(i.i)
                                del i 
                        if new==True: 
                            p=car.Car(pid,cx,cy,max_p_age) 
                            cars.append(p) 
                            pid+=1
                           
                        cv2.circle(frame,(cx,cy),5,(0,0,255),-1) 
                        img=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2) 

            frame=cv2.polylines(frame,[pts_L3],False,(255,255,255),thickness=1) 
            frame=cv2.polylines(frame,[pts_L4],False,(255,255,255),thickness=1) 

            color_yellow = (0,255,255) 
            cv2.putText(frame, "Cars: {}".format(total), (20,20), cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)
            cv2.imshow('video', frame) 
            

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        #очищаем память
        cap.release()
        cv2.destroyAllWindows()

        print("Cars counted manually: {}".format(carcounts_manual[cmi]), file=flrs)
        print("Cars counted by program: {}".format(total), file=flrs)
        cmi+=1
