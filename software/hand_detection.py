import numpy as np
import cv2 as cv
import queue
import fingers

#change the ip to 0 if you are using a webcame connected to pc
cap = cv.VideoCapture("https://192.168.0.11:8080/video")
IMAGE_DIM = 500, 500

#rgb skin values, colors outside this range will be removed
lower_skin = np.array([0,0,0])
upper_skin = np.array([190,125,190])

#variables used for counting the average fingers
finger_queue = []
finger_count_avg = 0

def uRedLower(value):
    lower_skin[0] = value
def uBlueLower(value):
    lower_skin[1] = value
def uGreenLower(value):
    lower_skin[2] = value
def uRedUpper(value):
    upper_skin[0] = value
def uBlueUpper(value):
    upper_skin[1] = value
def uGreenUpper(value):
    upper_skin[2] = value

res_window = cv.namedWindow('Debug')
cv.createTrackbar('Upper Red', 'Debug', upper_skin[0], 255, uRedUpper)
cv.createTrackbar('Upper Blue', 'Debug', upper_skin[1], 255, uBlueUpper)
cv.createTrackbar('Upper Green', 'Debug', upper_skin[2], 255, uGreenUpper)
cv.createTrackbar('Lower Red', 'Debug', lower_skin[0], 255, uRedLower)
cv.createTrackbar('Lower Blue', 'Debug', lower_skin[1], 255, uBlueLower)
cv.createTrackbar('Lower Green', 'Debug', lower_skin[2], 255, uGreenLower)

while(True):

    #reads and resizes image
    _, img = cap.read()
    img = cv.resize(img, IMAGE_DIM)
    img = cv.flip(img, 1)
    img = cv.blur(img, (5,5))

    #converts image rgb -> hsv and removes colors that are not in range
    hsv = cv.cvtColor(img, cv.COLOR_RGB2HSV)
    mask = cv.inRange(hsv, lower_skin, upper_skin)
    res = cv.bitwise_and(img, img, mask = mask)

    #converts hsv -> rgb -> grayscale then makes any color thats not black, white
    res_bw = cv.cvtColor(cv.cvtColor(res, cv.COLOR_HSV2RGB) , cv.COLOR_RGB2GRAY)
    _, res_bw = cv.threshold(res_bw, 1, 255, cv.THRESH_BINARY)

    #finds all the contours in the black and white image
    contours, _ = cv.findContours(res_bw, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    if(len(contours) > 0):
        #takes biggest contour
        max_contour = max(contours, key = cv.contourArea) 

        #makes b/w image completely black
        res_bw = np.zeros(IMAGE_DIM)

        #draws only max contour and makes fills in holes
        cv.drawContours(res_bw, [max_contour],-1, (255, 255, 255), -1)
        cv.drawContours(res, [max_contour],-1, (0, 255, 0), 3)

        #gets the current count of fingers and updates res with graphics
        finger_count, res = fingers.count(max_contour, res)

        #averages the number of fingers on screen for more reliable count and creates graphics
        finger_queue.append(finger_count)
        if(len(finger_queue) >= 10):
            finger_queue_len = len(finger_queue)
            finger_count_avg = 0
            for i in range(len(finger_queue)):
                finger_count_avg += finger_queue.pop(0)

            finger_count_avg = finger_count_avg / finger_queue_len + 1

        if(finger_count_avg > 1):
            cv.putText(res, "Fingers: " + str(round(finger_count_avg)), (50,50), cv.FONT_HERSHEY_SIMPLEX, .5, (0,200,200), 1, cv.LINE_AA)
        else:
             cv.putText(res, "No Open Fingers", (50,50), cv.FONT_HERSHEY_SIMPLEX, .5, (0,200,200), 1, cv.LINE_AA)


    else:
        #if there is no object on the screen
        #print("contours: none")
        pass
    
    #cv.imshow('Image', img)
    cv.imshow('Debug', res, )
    cv.imshow('Black/White', res_bw)

    #press key to stop program
    if cv.waitKey(1) & 0xFF == ord('f'):
        break

cv.destroyAllWindows


