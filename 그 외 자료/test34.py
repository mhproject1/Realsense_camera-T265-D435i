import cv2
import numpy as np

def cont():
    try:
        cap=cv2.VideoCapture(1)
    except:
        print('camera_errro')
        return

    while True:
        ret, frame = cap.read()
        
        if not ret:
            print('camera2_error')
            break

        dst = frame.copy()
        #cv2.imshow('frame', frame)
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #gray = cv2.equalizeHist(gray)
        #rects = detect(gray, debug=False)

        #height,width = frame.shape[:2]

        #for x1, y1, x2, y2 in rects:
        #    cv.rectangle(frame, (x1-10, 0), (x2+10, height), (0,0,0), -1)
            
        #cv2.imshow('frame1', frame1)

        test = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
        mask_hand = cv2.inRange(test, np.array([0,133,77]),np.array([255,173,127]))
        #cv2.imshow('mask_hand', mask_hand)
        #test = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #ret, thr = cv2.threshold(mask_hand, 127, 255, cv2.THRESH_BINARY_INV)
        #cv2.imshow('thr', thr)
        
        _, contours, hierachy=cv2.findContours(mask_hand, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        
        points1 = []
        result_cx = []
        result_cy = []
        
        for i in contours:
            M = cv2.moments(i)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                # set values as what you need in the situation
                cX, cY = 0, 0
                
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
            #cv2.drawContours(dst, [approx], 0, (0,255,0), 3)
            hull = cv2.convexHull(approx)
            for point in hull:
                if cy > point[0][1]:
                      points1.append(tuple(point[0])) 
            cv2.drawContours(dst, [hull], 0, (0,0,255),2)
            
        for point in points1:
            cv2.circle(dst, tuple(point), 15, [255, 0, 0], -1)
            
        cv2.imshow('dst', dst)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
            
    cap.release()
    cv2.destroyAllWindows()
    
cont()
