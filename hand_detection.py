import numpy as np
import cv2 as cv

#change the ip to 0 if you are using a webcame connected to pc
cap = cv.VideoCapture("https://192.168.0.11:8080/video")
IMAGE_DIM = 800, 800

#rgb skin values, colors outside this range will be removed
lower_skin = np.array([75,16,0])
upper_skin = np.array([233,203,255])

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

cv.namedWindow('Masked')
cv.createTrackbar('Upper Red', 'Masked', upper_skin[0], 255, uRedUpper)
cv.createTrackbar('Upper Blue', 'Masked', upper_skin[1], 255, uBlueUpper)
cv.createTrackbar('Upper Green', 'Masked', upper_skin[2], 255, uGreenUpper)
cv.createTrackbar('Lower Red', 'Masked', lower_skin[0], 255, uRedLower)
cv.createTrackbar('Lower Blue', 'Masked', lower_skin[1], 255, uBlueLower)
cv.createTrackbar('Lower Green', 'Masked', lower_skin[2], 255, uGreenLower)

while(True):

    #reads and resizes image
    _, img = cap.read()
    img = cv.resize(img, IMAGE_DIM)
    img = cv.blur(img, (3,3))

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
        #outlines max contour in res and draws rectangle
        cv.drawContours(res, [max_contour],-1, (0, 255, 0), 3)
        x,y,w,h = cv.boundingRect(max_contour)
        cv.rectangle(res, (x,y), (x+w, y+h), (255,0,0), 3)

    else:
        print("contours: none")
    

    #cv.imshow('Image', img)
    cv.imshow('Masked', res)
    cv.imshow('Black/White', res_bw)

    #press key to stop program
    if cv.waitKey(1) & 0xFF == ord('f'):
        break

cv.destroyAllWindows


