import numpy as np
import cv2 as cv

def count(hand_contour, res):
        
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

                #we use trig to solve for the angle between two fingers, if its less than n degrees it counts as the area between
                #two fingers
                side_a = np.sqrt((start[0]-end[0])**2 + (start[1]-end[1])**2)
                side_b = np.sqrt((far[0]-end[0])**2 + (far[1]-end[1])**2)
                side_c = np.sqrt((far[0]-start[0])**2 + (far[1]-start[1])**2)

                theta = np.arccos((side_b**2 + side_c**2 - side_a**2)/(2*side_b*side_c))
                theta = theta*(180/np.pi)

                if(theta <= 90):
                    finger_count += 1

                    cv.circle(res,far,5,[0,0,255],-1)
                    #cv.putText(res, str(theta), far, cv.FONT_HERSHEY_SIMPLEX, .5, (255,0,0), 1, cv.LINE_AA)
                    #cv.line(res,start,end,[255,255,0],2)
                

            return finger_count, res
                

    except:
        pass

    return 0, res
