import numpy as np
import cv2 as cv
import pyautogui
import queue
import sys

class HandDetection:

    #width and height of control window
    IMAGE_DIMENSIONS = 852, 480 

    def __init__(self, use_ip_webcam, webcam_ip, resolution_width, resolution_height, lower_hue, lower_saturation, lower_value, upper_hue, upper_saturation, upper_value, is_debug):

        self.webcam_ip = webcam_ip
        if(use_ip_webcam == 1):
            self.cap = cv.VideoCapture(self.webcam_ip)
        else:
            self.cap = cv.VideoCapture(0)

        self.resolution_width = resolution_width
        self.resolution_height = resolution_height

        #hsv skin values, colors outside this range will be removed
        self.lower_skin = np.array([lower_hue, lower_saturation, lower_value])
        self.upper_skin = np.array([upper_hue, upper_saturation, upper_value])

        self.is_debug = is_debug

        #got to round since we cant have decimals when writing lines to the screen
        self.IMAGE_BOUND_X = (int(self.IMAGE_DIMENSIONS[0]*(1/8)), int(self.IMAGE_DIMENSIONS[0]*(7/8)))
        self.IMAGE_BOUND_Y = (int(self.IMAGE_DIMENSIONS[1]*(1/8)), int(self.IMAGE_DIMENSIONS[1]*(3/4)))
        self.IMAGE_DISPLACEMENT_X = int(self.IMAGE_DIMENSIONS[0]*(1/8))
        self.IMAGE_DISPLACEMENT_Y = int(self.IMAGE_DIMENSIONS[1]*(1/8))
        self.IMAGE_DILATION = ((self.resolution_width/self.IMAGE_DIMENSIONS[0])/(6/8)), ((self.resolution_height/self.IMAGE_DIMENSIONS[1])/(5/8))
        print(self.IMAGE_DILATION)

    def count_fingers(self, hand_contour, res):
        #this does majortiy of the math regarding cursor placement and finger count

        #sets default cursor position to bottom left of screen
        cursor_pos_draw = (0, self.resolution_height)
        cursor_pos_real = (0, self.resolution_height)

        try:
            #creates contour around the hand, between each finger is a defect that we can get measurements of
            hand_contour_hull = cv.convexHull(hand_contour, returnPoints=False)
            if(len(hand_contour_hull) > 1):
                #we get the defects of the hull which is the area between our fingers
                hand_defects = cv.convexityDefects(hand_contour, hand_contour_hull)
                finger_count = 0

                #for every defect on the hand, we are using trig to check the angle. if it is less than 90 degrees we include that as a finger
                #start and end are the line between two finger tips and far is the point between the two fingers
                for i in range(hand_defects.shape[0]):
                    s,e,f,_ = hand_defects[i,0]
                    start = tuple(hand_contour[s][0])
                    end = tuple(hand_contour[e][0])
                    far = tuple(hand_contour[f][0])

                    #we look for the highest point on the hand and make that the picked cursor
                    if(cursor_pos_draw[1] > start[1]):
                        cursor_pos_draw = (start[0], start[1])
                        cursor_pos_real = (round((start[0]-self.IMAGE_DISPLACEMENT_X)*self.IMAGE_DILATION[0]), round((start[1]-self.IMAGE_DISPLACEMENT_Y)*self.IMAGE_DILATION[1]))

                        #if cursor goes out of bounds we correct it.
                        if(cursor_pos_real[0] < 0):
                            cursor_pos_real = (0, cursor_pos_real[1])
                        if(cursor_pos_real[1] < 0):
                            cursor_pos_real = (cursor_pos_real[0], 0)
                        if(cursor_pos_real[0] > self.resolution_width):
                            cursor_pos_real = (self.resolution_width, cursor_pos_real[1])
                        if(cursor_pos_real[1] > self.resolution_height):
                            cursor_pos_real = (cursor_pos_real[0], self.resolution_height)
                        print(cursor_pos_real)

                    #minimize the amount of math we do
                    side_a = np.sqrt((start[0]-end[0])**2 + (start[1]-end[1])**2)
                    if(side_a > 10):

                        #we use trig to solve for the angle between two fingers, if its less than n degrees it counts as the area between
                        #two fingers
                        side_b = np.sqrt((far[0]-end[0])**2 + (far[1]-end[1])**2)
                        side_c = np.sqrt((far[0]-start[0])**2 + (far[1]-start[1])**2)

                        theta = np.arccos((side_b**2 + side_c**2 - side_a**2)/(2*side_b*side_c))
                        theta = theta*(180/np.pi)

                        if(theta <= 90):
                            finger_count += 1

                            cv.circle(res,far,5,[0,0,255],-1)
                            cv.circle(res,cursor_pos_draw,5,[0,122,255],-1)
                            #cv.putText(res, str(theta), far, cv.FONT_HERSHEY_SIMPLEX, .5, (255,0,0), 1, cv.LINE_AA)
                            cv.line(res,start,end,[255,255,0],2)
                    
                return finger_count, res, cursor_pos_real
                    

        except Exception as e: 
            print(e)
            pass

        return 0, res, cursor_pos_real

    def run(self):

        cap = cv.VideoCapture(self.webcam_ip)
        #variables used for counting the average fingers
        finger_queue = []
        finger_count_avg = 0

        while(True):

            #reads and resizes image
            _, img = cap.read()
            img = cv.resize(img, self.IMAGE_DIMENSIONS)
            img = cv.flip(img, 1)
            img = cv.blur(img, (5,5))

            #converts image bgr -> hsv and removes colors that are not in range
            hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            mask = cv.inRange(hsv, self.lower_skin, self.upper_skin)
            res = cv.bitwise_and(img, img, mask = mask)

            #converts hsv -> bgr -> grayscale then makes any color thats not black, white
            res_bw = cv.cvtColor(cv.cvtColor(res, cv.COLOR_HSV2BGR) , cv.COLOR_BGR2GRAY)
            _, res_bw = cv.threshold(res_bw, 1, 255, cv.THRESH_BINARY)

            #finds all the contours in the black and white image
            contours, _ = cv.findContours(res_bw, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            
            if(len(contours) > 0):
                #takes biggest contour
                max_contour = max(contours, key = cv.contourArea) 

                #makes b/w image completely black (for some reason have to reverse dimensions)
                res_bw = np.zeros((self.IMAGE_DIMENSIONS[1], self.IMAGE_DIMENSIONS[0]))

                #draws only max contour and makes fills in holes
                cv.drawContours(res_bw, [max_contour],-1, (255, 255, 255), -1)
                cv.drawContours(res, [max_contour],-1, (0, 255, 0), 3)

                #gets the current count of fingers and updates res with graphics
                finger_count, res, cursor_pos = HandDetection.count_fingers(self, max_contour, res)

                cv.rectangle(res, (self.IMAGE_BOUND_X[0], self.IMAGE_BOUND_Y[0]), (self.IMAGE_BOUND_X[1], self.IMAGE_BOUND_Y[1]), (255, 255, 0), 1)
                if(finger_count >= 1):
                    try:
                        if(self.is_debug == 0):
                            pyautogui.moveTo((cursor_pos[0], cursor_pos[1]), _pause = False)
                        #todo fix out of bounds so that it doesnt make mouse get stuck
                    except:
                        pass
                    


                #averages the number of fingers on screen for more reliable count and creates graphics
                finger_queue.append(finger_count)
                if(len(finger_queue) >= 5):
                    finger_queue_len = len(finger_queue)
                    finger_count_avg = 0
                    for i in range(len(finger_queue)):
                        finger_count_avg += finger_queue.pop(0)

                    finger_count_avg = finger_count_avg / finger_queue_len 

                if(finger_count_avg > 1):
                    cv.putText(res, "Finger Openings: " + str(round(finger_count_avg)), (50,50), cv.FONT_HERSHEY_SIMPLEX, .5, (0,200,200), 1, cv.LINE_AA)
                else:
                    cv.putText(res, "No Open Fingers", (50,50), cv.FONT_HERSHEY_SIMPLEX, .5, (0,200,200), 1, cv.LINE_AA)


            else:
                #if there is no object on the screen
                #print("contours: none")
                pass
            
            #cv.imshow('Image', img)
            cv.imshow('Debug', res)
            cv.imshow('Black/White', res_bw)

            #press key to stop program
            if cv.waitKey(1) & 0xFF == ord('f'):
                break

        cv.destroyAllWindows()

