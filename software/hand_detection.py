import logging
import queue
import sys
from tkinter.constants import END

import cv2 as cv
import numpy as np
import pyautogui

logger = logging.getLogger(__name__)
pyautogui.FAILSAFE = False


class HandDetection:

    # width and height of control window
    IMAGE_DIMENSIONS = 852, 480
    movement_queue = [(0,0)]*5
    left_clicked = False
    right_clicked = False

    def __init__(
        self,
        use_ip_webcam: int,
        webcam_ip: str,
        resolution_width: int,
        resolution_height: int,
        lower_hue: int,
        lower_saturation: int,
        lower_value: int,
        upper_hue: int,
        upper_saturation: int,
        upper_value: int,
        is_debug: int,
    ):
        self.webcam_ip = webcam_ip
        if use_ip_webcam:
            self.cap = cv.VideoCapture(self.webcam_ip) #ip webcam connect
        else:
            self.cap = cv.VideoCapture(0) #integrated webcam connect

        self.resolution_width = resolution_width
        self.resolution_height = resolution_height

        # hsv skin values, colors outside this range will be removed
        self.lower_skin = np.array([lower_hue, lower_saturation, lower_value])
        self.upper_skin = np.array([upper_hue, upper_saturation, upper_value])

        self.is_debug = is_debug

        #this is all the math dealing with boundaries and dialation of cursor movement on the input
        #bounds set the area on the image in which the cursor can move
        self.IMAGE_BOUND_X = (
            int(self.IMAGE_DIMENSIONS[0] * (1 / 8)),
            int(self.IMAGE_DIMENSIONS[0] * (7 / 8)),
        )
        self.IMAGE_BOUND_Y = (
            int(self.IMAGE_DIMENSIONS[1] * (1 / 8)),
            int(self.IMAGE_DIMENSIONS[1] * (5 / 8)),
        )
        #displacement pushes the cursor forward to account for the boundaries imposed in the opencv window
        self.IMAGE_DISPLACEMENT_X = int(self.IMAGE_DIMENSIONS[0] * (1 / 8))
        self.IMAGE_DISPLACEMENT_Y = int(self.IMAGE_DIMENSIONS[1] * (1 / 8))
        #dilation gets the resolution of opencv window to screen so that it can dilate the cursor positions from window to screen
        self.IMAGE_DILATION = (
            (self.resolution_width / self.IMAGE_DIMENSIONS[0]) / (6 / 8)
        ), ((self.resolution_height / self.IMAGE_DIMENSIONS[1]) / (4 / 8))

    def count_fingers(self, hand_contour, res):
        """
        this does majortiy of the math regarding cursor placement and finger count
        """

        # sets default cursor position to bottom left of screen
        cursor_pos_draw = (0, self.resolution_height)
        cursor_pos_real = (0, self.resolution_height)

        try:
            # creates contour around the hand, between each finger is a defect that we can get measurements of
            hand_contour_hull = cv.convexHull(hand_contour, returnPoints=False)
            if len(hand_contour_hull) > 1:
                # we get the defects of the hull which is the area between our fingers
                hand_defects = cv.convexityDefects(hand_contour, hand_contour_hull)
                finger_count = 0
                #variable to keep track of fingers coords to be made into cursor coords
                #reason we only do this once is because we only select with two fingers up/ one defect
                #if there is more than 1 we do not care
                select_fingers = [(0,0)]*2
                # for every defect on the hand, we are using trig to check the angle. if it is less than 90 degrees we include that as a finger
                # start and end are the line between two finger tips and far is the point between the two fingers
                for i in range(hand_defects.shape[0]):
                    s, e, f, _ = hand_defects[i, 0]
                    start = tuple(hand_contour[s][0])
                    end = tuple(hand_contour[e][0])
                    far = tuple(hand_contour[f][0])

                    # minimize the amount of math we do
                    side_a = np.sqrt(
                        (start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2
                    )
                    if side_a > 10:

                        # we use trig to solve for the angle between two fingers, if its less than n degrees it counts as the area between
                        # two fingers
                        side_b = np.sqrt(
                            (far[0] - end[0]) ** 2 + (far[1] - end[1]) ** 2
                        )
                        side_c = np.sqrt(
                            (far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2
                        )

                        theta = np.arccos(
                            (side_b ** 2 + side_c ** 2 - side_a ** 2)
                            / (2 * side_b * side_c)
                        )
                        theta = theta * (180 / np.pi)

                        if theta <= 90:
                            finger_count += 1
                            select_fingers = (start, end)

                            cv.circle(res, far, 5, [0, 0, 255], -1)
                            cv.line(res, start, end, [255, 255, 0], 2)

                # we look for the highest point on the hand and make that the picked cursor
                
                cursor_pos_draw, cursor_pos_real = HandDetection.cursorPointCalculation(self, select_fingers)

                cv.circle(res, cursor_pos_draw, 5, [0, 122, 255], -1)

                return finger_count, res, cursor_pos_real

        except:
            logger.exception("failure on count_fingers")

        return 0, res, cursor_pos_real

    def run(self):

        cap = cv.VideoCapture(self.webcam_ip)
        # variables used for counting the average fingers
        finger_queue = []
        finger_count_avg = 0

        while True:

            # reads and resizes image
            _, img = cap.read()
            img = cv.resize(img, self.IMAGE_DIMENSIONS)
            img = cv.flip(img, 1)
            img = cv.GaussianBlur(img, (5, 5), 0)

            # converts image bgr -> hsv and removes colors that are not in range
            hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            mask = cv.inRange(hsv, self.lower_skin, self.upper_skin)
            res = cv.bitwise_and(img, img, mask=mask)

            # converts hsv -> bgr -> grayscale then makes any color thats not black, white
            res_bw = cv.cvtColor(cv.cvtColor(res, cv.COLOR_HSV2BGR), cv.COLOR_BGR2GRAY)
            _, res_bw = cv.threshold(res_bw, 1, 255, cv.THRESH_BINARY)

            # finds all the contours in the black and white image
            contours, _ = cv.findContours(res_bw, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            
            # makes b/w image completely black (for some reason have to reverse dimensions)
            res_bw = np.zeros((self.IMAGE_DIMENSIONS[1], self.IMAGE_DIMENSIONS[0]))

            # takes biggest contour, but if it cant get max, when it has nothing, it will make an empty list
            try:
                max_contour = max(contours, key=cv.contourArea)
            except:
                max_contour = []

            #if theres more than one contour and the largest contour is atleast 5000 units then we take it in
            if (len(contours) > 0 and max_contour != [] and cv.contourArea(max_contour) > 5000):
                
                # draws only max contour and makes fills in holes
                cv.drawContours(res_bw, [max_contour], -1, (255, 255, 255), -1)
                cv.drawContours(res, [max_contour], -1, (0, 255, 0), 3)

                # gets the current count of fingers and updates res with graphics
                finger_count, res, cursor_pos = HandDetection.count_fingers(
                    self, max_contour, res
                )

                cv.rectangle(
                    res,
                    (self.IMAGE_BOUND_X[0], self.IMAGE_BOUND_Y[0]),
                    (self.IMAGE_BOUND_X[1], self.IMAGE_BOUND_Y[1]),
                    (255, 255, 0),
                    1,
                )

                # averages the number of fingers on screen for more reliable count and creates graphics
                finger_queue.append(finger_count)
                if len(finger_queue) >= 5:
                    finger_count_avg = sum(finger_queue) / len(finger_queue)
                    finger_queue.clear()

                HandDetection.mouseInteraction(self, cursor_pos, finger_count_avg)

                if finger_count_avg > 0:
                    cv.putText(
                        res,
                        f"Finger Openings: {round(finger_count_avg)}",
                        (50, 50),
                        cv.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 200, 200),
                        1,
                        cv.LINE_AA,
                    )
                else:
                    cv.putText(
                        res,
                        "No Open Fingers",
                        (50, 50),
                        cv.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 200, 200),
                        1,
                        cv.LINE_AA,
                    )

            else:
                # if there is no object on the screen
                pass

            # cv.imshow('Image', img)
            cv.imshow("Debug", res)
            cv.imshow("Black/White", res_bw)

            # press key to stop program
            if cv.waitKey(1) & 0xFF == ord("f"):
                break

        cv.destroyAllWindows()

    def mouseInteraction(self, cursor_pos, finger_count):
        #function deals with movement, leftclick, and rightclicking with the program
        try:
            if self.is_debug == 0:
                if(finger_count == 1 ):
                    #we need a slightly delayed movement so that moving fingers to left click does not move the cursor
                    self.movement_queue.insert(0, cursor_pos[0:2])
                    delayed_cursor_pos = self.movement_queue.pop()
                    current_cursor_pos = pyautogui.position()

                    #if you want smoother movement you can change how many pixels it will skip
                    if(abs(delayed_cursor_pos[0]-current_cursor_pos[0]) > 1 and abs(delayed_cursor_pos[0]-current_cursor_pos[0]) > 1):
                        pyautogui.moveTo(
                            (delayed_cursor_pos), _pause=False
                        )

                    self.left_clicked = False
                    self.right_clicked = False

                elif(finger_count == 2 and self.left_clicked == False):
                    pyautogui.leftClick()
                    self.left_clicked = True
                
                elif(finger_count == 4 and self.right_clicked == False):
                    pyautogui.rightClick()
                    self.right_clicked = True

        except:
            logger.exception("hand cursor failure")

    def cursorPointCalculation(self, points):
        
        cursor_pos_draw = (round((points[0][0]+points[1][0])/2), round((points[0][1]+points[1][1])/2))
        cursor_pos_real = (
            round(
                (cursor_pos_draw[0] - self.IMAGE_DISPLACEMENT_X)
                * self.IMAGE_DILATION[0]
            ),
            round(
                (cursor_pos_draw[1] - self.IMAGE_DISPLACEMENT_Y)
                * self.IMAGE_DILATION[1]
            ),
        )

        # if cursor goes out of bounds we correct it.
        if cursor_pos_real[0] < 0:
            cursor_pos_real = (0, cursor_pos_real[1])
        if cursor_pos_real[1] < 0:
            cursor_pos_real = (cursor_pos_real[0], 0)
        if cursor_pos_real[0] > self.resolution_width:
            cursor_pos_real = (
                self.resolution_width,
                cursor_pos_real[1],
            )
        if cursor_pos_real[1] > self.resolution_height:
            cursor_pos_real = (
                    cursor_pos_real[0],
                self.resolution_height,
            )
        
        return cursor_pos_draw, cursor_pos_real